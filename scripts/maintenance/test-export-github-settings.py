#!/usr/bin/env python3
"""Regression checks for absence, access failures and conditional policy reads."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("settings_export", Path(__file__).with_name("export-github-settings.py"))
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


def api_error(status, message, body_status=True):
    payload = {"message": message}
    if body_status:
        payload["status"] = str(status)
    result = subprocess.CompletedProcess([], 1, json.dumps(payload), f"gh: {message} (HTTP {status})")
    return exporter.ApiError(result)


class ExportTests(unittest.TestCase):
    def run_export(self, mode="all", overrides=None):
        org = exporter.ORG
        repo = f"repos/{org}/example"
        routes = {
            f"orgs/{org}": {"login": org},
            f"orgs/{org}/actions/permissions": {"enabled_repositories": "all", "allowed_actions": mode},
            f"orgs/{org}/actions/permissions/workflow": {"default_workflow_permissions": "read"},
            f"orgs/{org}/code-security/configurations/defaults": [],
            f"orgs/{org}/rulesets?per_page=100": api_error(403, "Upgrade to GitHub Team to enable this feature."),
            f"orgs/{org}/repos?per_page=100&type=all": [
                {"full_name": f"{org}/example", "name": "example", "default_branch": "main"}
            ],
            repo: {"full_name": f"{org}/example", "default_branch": "main"},
            repo + "/branches/main/protection": api_error(404, "Branch not protected"),
            repo + "/rulesets?includes_parents=true&per_page=100": [{"id": 42}],
            repo + "/rulesets/42": {"id": 42, "enforcement": "active"},
            repo + "/actions/permissions": {"enabled": True, "allowed_actions": mode},
            repo + "/actions/permissions/workflow": {"default_workflow_permissions": "read"},
            repo + "/environments?per_page=100": {"total_count": 0, "environments": []},
        }
        if mode == "selected":
            for prefix in (f"orgs/{org}", repo):
                routes[prefix + "/actions/permissions/selected-actions"] = {"github_owned_allowed": True}
        routes.update(overrides or {})
        calls = []

        def fake_api(endpoint, paginate=False):
            calls.append(endpoint)
            value = routes[endpoint]  # Unexpected endpoint fails the test/export.
            if isinstance(value, Exception):
                raise value
            return value

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "settings"
            previous_umask = os.umask(0o077)
            try:
                with patch.object(exporter, "api", side_effect=fake_api), \
                        patch("sys.argv", ["export", "--output", str(output)]), \
                        contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    code = exporter.main()
                summary = json.loads((output / "SUMMARY.json").read_text())
                files = {name: json.loads((output / name).read_text()) for name in summary["files"]}
            finally:
                os.umask(previous_umask)
        return code, summary, calls, files

    def test_absent_classic_rule_keeps_active_ruleset_and_successful_export(self):
        code, summary, calls, files = self.run_export()
        self.assertEqual(code, 0)
        self.assertEqual(summary["errors"], [])
        self.assertEqual(len(summary["unavailable"]), 2)
        self.assertEqual(len(summary["skipped"]), 2)
        self.assertEqual(files["example/ruleset-42.json"]["enforcement"], "active")
        self.assertFalse(any(path.endswith("selected-actions") for path in calls))

    def test_selected_policy_is_actually_exported_at_both_levels(self):
        code, summary, calls, files = self.run_export("selected")
        self.assertEqual(code, 0)
        self.assertEqual(sum(path.endswith("selected-actions") for path in calls), 2)
        self.assertEqual(summary["skipped"], [])
        self.assertTrue(files["example/actions-selected-actions.json"]["github_owned_allowed"])

    def test_local_only_has_no_selected_policy_lookup(self):
        code, summary, calls, _ = self.run_export("local_only")
        self.assertEqual(code, 0)
        self.assertFalse(any(path.endswith("selected-actions") for path in calls))

    def test_generic_protection_404_remains_unknown(self):
        endpoint = f"repos/{exporter.ORG}/example/branches/main/protection"
        code, summary, _, _ = self.run_export(overrides={endpoint: api_error(404, "Not Found")})
        self.assertEqual(code, 2)
        self.assertEqual(summary["errors"][0]["endpoint"], endpoint)

    def test_denied_org_rulesets_are_not_reported_as_plan_limits(self):
        endpoint = f"orgs/{exporter.ORG}/rulesets?per_page=100"
        code, summary, _, _ = self.run_export(overrides={endpoint: api_error(403, "Resource not accessible by integration")})
        self.assertEqual(code, 2)
        self.assertEqual(summary["errors"][0]["endpoint"], endpoint)

    def test_unreadable_current_security_defaults_remain_visible(self):
        endpoint = f"orgs/{exporter.ORG}/code-security/configurations/defaults"
        code, summary, _, _ = self.run_export(overrides={endpoint: api_error(403, "Resource not accessible by integration")})
        self.assertEqual(code, 2)
        self.assertEqual(summary["errors"][0]["endpoint"], endpoint)

    def test_missing_permissions_do_not_invent_an_actions_policy(self):
        endpoint = f"orgs/{exporter.ORG}/actions/permissions"
        code, summary, calls, _ = self.run_export(overrides={endpoint: api_error(403, "Forbidden")})
        self.assertEqual(code, 2)
        self.assertEqual(summary["errors"][0]["endpoint"], endpoint)
        self.assertNotIn(endpoint + "/selected-actions", calls)

    def test_http_status_is_recovered_from_gh_stderr(self):
        error = api_error(404, "Branch not protected", body_status=False)
        self.assertEqual(error.status, 404)
        self.assertIsNotNone(exporter.expected_unavailability(
            f"repos/{exporter.ORG}/example/branches/main/protection", error))

    def test_adjacent_array_pagination_and_read_only_invocation(self):
        result = subprocess.CompletedProcess([], 0, '[{"id":1}]\n[{"id":2}]', "")
        with patch.object(exporter.subprocess, "run", return_value=result) as run:
            self.assertEqual(exporter.api("repos/VOLPAROSSA/example/rulesets", True), [{"id": 1}, {"id": 2}])
        self.assertEqual(run.call_args.args[0], [
            "gh", "api", "--hostname", "github.com", "repos/VOLPAROSSA/example/rulesets", "--paginate"
        ])


if __name__ == "__main__":
    unittest.main()
