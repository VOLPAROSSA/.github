import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("archive", Path(__file__).with_name("archive-retired-branches.py"))
archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)


class WorkflowGuards(unittest.TestCase):
    def test_only_explicit_branch_push_filters_are_admitted(self):
        for source in ("on:\n  push:\n    branches: [main]\n", "on:\n  push:\n    branches-ignore: [legacy]\n",
                       "on: workflow_dispatch\n", "on: [workflow_dispatch, pull_request]\n"):
            self.assertEqual(archive.workflow_trigger_issues(source), [])
        for source in ("on: push\n", "on: [push, pull_request]\n", "on:\n  push:\n",
                       "on:\n  push:\n    tags: [v*]\n", "on: [create]\n", "on: delete\n",
                       "on:\n  push:\n    branches: [main]\n    tags-ignore: [v*]\n", "jobs: {}\n"):
            self.assertTrue(archive.workflow_trigger_issues(source))

    def test_all_reserved_pages_repositories_are_excluded(self):
        self.assertEqual(len(archive.EXCLUDED), 8)
        self.assertFalse(set(archive.REPOS) & set(archive.EXCLUDED))

    def test_deletion_push_must_not_match_explicit_branch_list(self):
        source = "on:\n  push:\n    branches: [main, historical/trial]\n"
        self.assertEqual(archive.workflow_trigger_issues(source, "retired/topic"), [])
        self.assertTrue(archive.workflow_trigger_issues(source, "historical/trial"))

    def test_ignore_list_must_explicitly_exclude_deleted_branch(self):
        source = "on:\n  push:\n    branches-ignore: [retired/topic]\n"
        self.assertEqual(archive.workflow_trigger_issues(source, "retired/topic"), [])
        self.assertTrue(archive.workflow_trigger_issues(source, "other/topic"))

    def test_glob_or_unknown_branch_selector_blocks_archival(self):
        for pattern in ("'feature/**'", "'main*'", "'!retired/topic'", "'feature/+'", "'@(main|retired/topic)'"):
            source = f"on:\n  push:\n    branches: [{pattern}]\n"
            self.assertTrue(archive.workflow_trigger_issues(source, "retired/topic"))
        self.assertTrue(archive.workflow_trigger_issues("on:\n  push:\n    branches: main\n", "retired/topic"))
        self.assertTrue(archive.workflow_trigger_issues("on:\n  push:\n    branches: []\n", "retired/topic"))


class AtomicArchive(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.remote, self.local = self.root / "remote.git", self.root / "local"
        subprocess.run(["git", "init", "--bare", "--quiet", str(self.remote)], check=True)
        subprocess.run(["git", "init", "--quiet", str(self.local)], check=True)
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "one")
        self.first = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "two")
        self.second = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("push", str(self.remote), "HEAD:refs/heads/main", f"{self.first}:refs/heads/retired")
        self.tag = archive.ARCHIVE_PREFIX + "retired"

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        return archive.git(self.local, *args)

    def refs(self):
        return archive.remote_refs(self.local, str(self.remote), "refs/heads/retired", "refs/tags/" + self.tag)

    def test_tag_creation_and_branch_deletion_are_atomic(self):
        archive.archive_atomic(self.local, str(self.remote), "retired", self.first, self.tag)
        self.assertEqual(self.refs(), {"refs/tags/" + self.tag: self.first})

    def test_follow_tags_config_cannot_publish_an_unrelated_tag(self):
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "tag", "-a", "unrelated-release", self.first, "-m", "must remain local")
        self.git("config", "push.followTags", "true")
        archive.archive_atomic(self.local, str(self.remote), "retired", self.first, self.tag)
        self.assertEqual(archive.remote_refs(self.local, str(self.remote), "refs/tags/*"),
                         {"refs/tags/" + self.tag: self.first})

    def test_existing_archive_tag_is_never_overwritten(self):
        self.git("push", str(self.remote), f"{self.second}:refs/tags/{self.tag}")
        with self.assertRaises(RuntimeError):
            archive.archive_atomic(self.local, str(self.remote), "retired", self.first, self.tag)
        self.assertEqual(self.refs(), {"refs/heads/retired": self.first, "refs/tags/" + self.tag: self.second})

    def test_racing_branch_move_rejects_both_ref_updates(self):
        read = archive.remote_refs

        def racing_read(*args):
            observed = read(*args)
            subprocess.run(["git", "--git-dir", str(self.remote), "update-ref", "refs/heads/retired", self.second], check=True)
            return observed

        with patch.object(archive, "remote_refs", side_effect=racing_read):
            with self.assertRaises(RuntimeError):
                archive.archive_atomic(self.local, str(self.remote), "retired", self.first, self.tag)
        self.assertEqual(self.refs(), {"refs/heads/retired": self.second})

    def test_racing_tag_creation_rejects_both_ref_updates(self):
        read = archive.remote_refs

        def racing_read(*args):
            observed = read(*args)
            subprocess.run(["git", "--git-dir", str(self.remote), "update-ref", "refs/tags/" + self.tag, self.second], check=True)
            return observed

        with patch.object(archive, "remote_refs", side_effect=racing_read):
            with self.assertRaises(RuntimeError):
                archive.archive_atomic(self.local, str(self.remote), "retired", self.first, self.tag)
        self.assertEqual(self.refs(), {"refs/heads/retired": self.first, "refs/tags/" + self.tag: self.second})

    def test_no_atomic_capability_means_no_changes(self):
        subprocess.run(["git", "--git-dir", str(self.remote), "config", "receive.advertiseAtomic", "false"], check=True)
        with self.assertRaises(RuntimeError):
            archive.archive_atomic(self.local, str(self.remote), "retired", self.first, self.tag)
        self.assertEqual(self.refs(), {"refs/heads/retired": self.first})


if __name__ == "__main__":
    unittest.main()
