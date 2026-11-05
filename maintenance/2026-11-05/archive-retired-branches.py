#!/usr/bin/env python3
"""Archive unused VOLPAROSSA branches as tags; dry-run unless --apply is supplied."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import quote

import yaml  # PyYAML; safe BaseLoader only, no constructors or repository code.

ORG = "VOLPAROSSA"
REPOS = (".github", "volparossa", "volparossa-browser", "volparossa-code",
         "volparossa-cloud", "volparossa-image")
EXCLUDED = ("volparossa.github.io", "volparossa-mail", "volparossa-map", "volparossa-weather",
            "volparossa-studio", "volparossa-bank", "volparossa-citizen", "volparossa-chat")
ARCHIVE_PREFIX = "archive/2026-11-05/"


def api(endpoint, paginate=False):
    command = ["gh", "api", "--hostname", "github.com", endpoint]
    if paginate:
        command.append("--paginate")
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"gh exited {result.returncode}")
    if not paginate:
        return json.loads(result.stdout)
    remaining, pages = result.stdout.lstrip(), []
    decoder = json.JSONDecoder()
    while remaining:
        page, end = decoder.raw_decode(remaining)
        if not isinstance(page, list):
            raise ValueError("Expected paginated array")
        pages.extend(page)
        remaining = remaining[end:].lstrip()
    return pages


def referenced_branches(pulls, full_name):
    result = set()
    for pull in pulls:
        for side in ("head", "base"):
            value = pull[side]
            if (value.get("repo") or {}).get("full_name", "").lower() == full_name.lower():
                result.add(value["ref"])
    return result


def keep_reason(branch, default, references):
    if branch["name"] in ("main", "master", default):
        return "default/reserved branch"
    if branch.get("protected") is not False:
        return "protected or protection unknown"
    if branch["name"] in references:
        return "open PR head/base"
    return None


def workflow_trigger_issues(source, deleted_branch=None):
    if len(source.encode("utf-8")) > 2 * 1024 * 1024:
        return ["workflow exceeds inspection bound"]
    document = yaml.load(source, Loader=yaml.BaseLoader)
    if not isinstance(document, dict) or "on" not in document:
        return ["unrecognized workflow event definition"]
    events = document["on"]
    if isinstance(events, str):
        events = {events: None}
    elif isinstance(events, list) and all(isinstance(event, str) for event in events):
        events = {event: None for event in events}
    if not isinstance(events, dict):
        return ["unrecognized workflow event definition"]
    issues = []
    for event in ("create", "delete"):
        if event in events:
            issues.append(f"{event} event may run during archival")
    if "push" in events:
        push = events["push"]
        if (not isinstance(push, dict)
                or not ({"branches", "branches-ignore"} & push.keys())
                or {"tags", "tags-ignore"} & push.keys()):
            issues.append("push event is not exclusively branch-filtered")
        elif deleted_branch is not None:
            selectors = {key for key in ("branches", "branches-ignore") if key in push}
            if len(selectors) != 1:
                issues.append("ambiguous push branch filters")
            else:
                selector = next(iter(selectors))
                patterns = push[selector]
                if (not isinstance(patterns, list) or not patterns
                        or not all(isinstance(value, str) and value for value in patterns)):
                    issues.append("unrecognized push branch pattern list")
                elif any(any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/._-"
                             for character in value) for value in patterns):
                    issues.append("push branch glob requires manual review before branch deletion")
                elif ((selector == "branches" and deleted_branch in patterns)
                      or (selector == "branches-ignore" and deleted_branch not in patterns)):
                    # A ref deletion is also a push; path filters are not used as proof of exclusion.
                    issues.append("push event can match the deleted branch")
    return issues


def git(directory, *args, check=True):
    result = subprocess.run([
        "git", "-C", str(directory), "-c", "core.hooksPath=/dev/null",
        "-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential", *args,
    ], text=True, capture_output=True, check=False,
        env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git failed")
    return result


def inspect_workflows(directory, sha, deleted_branch=None):
    paths = git(directory, "ls-tree", "-r", "--name-only", "-z", sha, ".github/workflows").stdout.split("\0")
    result = []
    for path in paths:
        if path.count("/") != 2 or not path.endswith((".yml", ".yaml")):
            continue
        source = git(directory, "show", f"{sha}:{path}").stdout
        result.append({"path": path, "issues": workflow_trigger_issues(source, deleted_branch)})
    return result


def remote_refs(directory, remote, *refs):
    output = git(directory, "ls-remote", "--refs", remote, *refs).stdout
    return {line.split("\t", 1)[1]: line.split("\t", 1)[0]
            for line in output.splitlines() if line}


def archive_atomic(directory, remote, branch, sha, tag):
    head_ref, tag_ref = "refs/heads/" + branch, "refs/tags/" + tag
    observed = remote_refs(directory, remote, head_ref, tag_ref)
    if observed.get(head_ref) != sha:
        raise RuntimeError("Branch moved before atomic archive")
    if tag_ref in observed:
        raise RuntimeError("Archive tag already exists; refusing overwrite")
    # The remote must support atomic pushes: either both refs change, or neither does.
    # An empty expected tag value requires a new tag; the head lease requires exact SHA.
    git(directory, "push", "--atomic", "--porcelain", "--no-follow-tags", "--recurse-submodules=no",
        f"--force-with-lease={head_ref}:{sha}", f"--force-with-lease={tag_ref}:",
        remote, f"{sha}:{tag_ref}", f":{head_ref}")
    verified = remote_refs(directory, remote, head_ref, tag_ref)
    if verified.get(tag_ref) != sha or head_ref in verified:
        raise RuntimeError("Atomic archive receipt could not be verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repo", action="append", choices=REPOS)
    parser.add_argument("--from-report", type=Path,
                        help="limit apply to exact candidate SHAs from a reviewed dry-run report (required with --apply)")
    parser.add_argument("--source-root", type=Path,
                        help="reuse existing local repository objects read-only; otherwise fetch a temporary shallow copy")
    parser.add_argument("--report", type=Path, default=Path("volparossa-archive-preview.json"))
    args = parser.parse_args()
    if args.report.exists():
        parser.error("report already exists; choose a new path")
    if args.apply and args.from_report is None:
        parser.error("--apply requires --from-report with the reviewed dry-run report")
    reviewed = None
    if args.from_report is not None:
        plan = json.loads(args.from_report.read_text(encoding="utf-8"))
        if plan.get("apply") is not False or plan.get("errors") or plan.get("archive_prefix") != ARCHIVE_PREFIX:
            parser.error("source report must be an error-free dry-run with the same archive prefix")
        reviewed = {}
        for item in plan["branches"]:
            if item.get("action") != "candidate":
                continue
            if item["repository"] not in {f"{ORG}/{repo}" for repo in REPOS}:
                parser.error("source report contains an out-of-scope candidate")
            key = (item["repository"], item["branch"])
            if key in reviewed or item["archive_tag"] != ARCHIVE_PREFIX + item["branch"]:
                parser.error("duplicate or inconsistent source candidate")
            reviewed[key] = item["sha"]
    os.umask(0o077)
    report = {"captured_at": dt.datetime.now(dt.timezone.utc).isoformat(), "apply": args.apply,
              "archive_prefix": ARCHIVE_PREFIX, "excluded_repositories": EXCLUDED,
              "repositories": [], "branches": [], "errors": []}

    def save():
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    save()
    try:
        for repo in args.repo or REPOS:
            if repo not in REPOS or repo in EXCLUDED:
                raise RuntimeError(f"Repository is outside archival scope: {repo}")
            full_name = f"{ORG}/{repo}"
            endpoint = f"repos/{full_name}"
            remote = f"https://github.com/{full_name}.git"
            print(f"CHECK {full_name}", file=sys.stderr, flush=True)
            settings = api(endpoint)
            if settings["archived"]:
                continue
            default = settings["default_branch"]
            main_branch = api(f"{endpoint}/branches/{quote(default, safe='')}")
            main_sha = main_branch["commit"]["sha"]
            pulls = api(f"{endpoint}/pulls?state=open&per_page=100", paginate=True)
            references = referenced_branches(pulls, full_name)
            branches = api(f"{endpoint}/branches?per_page=100", paginate=True)
            required = {main_sha} | {branch["commit"]["sha"] for branch in branches
                                    if not keep_reason(branch, default, references)}
            with tempfile.TemporaryDirectory(prefix="archive-objects-", dir=args.report.parent) as temporary:
                directory = args.source_root / repo if args.source_root else Path(temporary)
                have_all = args.source_root is not None and all(
                    git(directory, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode == 0
                    for sha in required)
                if not have_all:
                    directory = Path(temporary)
                    git(directory, "init", "--bare", "--quiet")
                    git(directory, "fetch", "--quiet", "--no-tags", "--depth=1", remote,
                        "+refs/heads/*:refs/remotes/origin/*")
                    for sha in required:
                        git(directory, "cat-file", "-e", f"{sha}^{{commit}}")
                main_checks = inspect_workflows(directory, main_sha)
                repo_entry = {"repository": full_name, "default_branch": default,
                              "default_sha": main_sha, "default_workflows": main_checks}
                report["repositories"].append(repo_entry)
                default_blocked = any(item["issues"] for item in main_checks)
                existing_tags = remote_refs(directory, remote, "refs/tags/*")
                for branch in branches:
                    name, sha = branch["name"], branch["commit"]["sha"]
                    tag = ARCHIVE_PREFIX + name
                    entry = {"repository": full_name, "branch": name, "sha": sha, "archive_tag": tag}
                    report["branches"].append(entry)
                    why = keep_reason(branch, default, references)
                    if why:
                        entry.update(action="keep", reason=why)
                        continue
                    if reviewed is not None and (full_name, name) not in reviewed:
                        entry.update(action="keep", reason="not in reviewed candidate set")
                        continue
                    if reviewed is not None and reviewed[(full_name, name)] != sha:
                        raise RuntimeError(f"Reviewed branch SHA changed: {full_name}/{name}")
                    checks = inspect_workflows(directory, sha, name)
                    entry["workflows"] = checks
                    deletion_checks = [item for item in inspect_workflows(directory, main_sha, name) if item["issues"]]
                    entry["default_branch_deletion_issues"] = deletion_checks
                    if default_blocked or deletion_checks or any(item["issues"] for item in checks):
                        entry.update(action="blocked", reason="workflow trigger requires manual review")
                        continue
                    tag_ref = "refs/tags/" + tag
                    if tag_ref in existing_tags:
                        entry.update(action="blocked", reason="archive tag already exists")
                        continue
                    entry.update(action="candidate", reason="retired branch; exact tip retained by archive tag")
                    print(f"CANDIDATE {full_name} {name} -> {tag} ({sha})", flush=True)
                    save()
                    if not args.apply:
                        continue
                    current_settings = api(endpoint)
                    current_branch = api(f"{endpoint}/branches/{quote(name, safe='')}")
                    current_pulls = api(f"{endpoint}/pulls?state=open&per_page=100", paginate=True)
                    current_main = api(f"{endpoint}/branches/{quote(default, safe='')}")
                    if current_settings["archived"] or current_settings["default_branch"] != default:
                        raise RuntimeError(f"Repository state changed: {full_name}")
                    if current_branch["commit"]["sha"] != sha or current_main["commit"]["sha"] != main_sha:
                        raise RuntimeError(f"Inspected source changed: {full_name}/{name}")
                    why = keep_reason(current_branch, default, referenced_branches(current_pulls, full_name))
                    if why:
                        raise RuntimeError(f"Branch is now in use: {full_name}/{name}: {why}")
                    entry["action"] = "archive_attempted"
                    save()
                    archive_atomic(directory, remote, name, sha, tag)
                    entry["action"] = "archived"
                    save()
    except (OSError, RuntimeError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        report["errors"].append(str(error))
        print(f"STOPPED: {error}", file=sys.stderr)
    finally:
        save()
    for action in ("candidate", "archived", "blocked", "keep"):
        print(f"{action}: {sum(item.get('action') == action for item in report['branches'])}")
    print(f"Report: {args.report}")
    return 2 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
