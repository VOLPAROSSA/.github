#!/usr/bin/env python3
"""Read-only VOLPAROSSA settings export. Requires Python 3 and authenticated gh."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote

ORG = "VOLPAROSSA"
ORG_FIELDS = (
    "login", "default_repository_permission", "members_can_create_repositories",
    "members_can_create_public_repositories", "members_can_create_private_repositories",
    "members_can_create_internal_repositories", "members_can_fork_private_repositories",
    "members_can_create_pages", "members_can_create_public_pages",
    "members_can_create_private_pages", "two_factor_requirement_enabled",
    "web_commit_signoff_required", "dependency_graph_enabled_for_new_repositories",
    "dependabot_alerts_enabled_for_new_repositories",
    "dependabot_security_updates_enabled_for_new_repositories",
    "secret_scanning_enabled_for_new_repositories",
    "secret_scanning_push_protection_enabled_for_new_repositories",
)
REPO_FIELDS = (
    "full_name", "visibility", "archived", "default_branch", "has_issues", "has_projects",
    "has_wiki", "has_pages", "has_discussions", "allow_forking", "allow_merge_commit",
    "allow_squash_merge", "allow_rebase_merge", "allow_auto_merge", "allow_update_branch",
    "delete_branch_on_merge", "web_commit_signoff_required", "security_and_analysis",
    "squash_merge_commit_title", "squash_merge_commit_message",
    "merge_commit_title", "merge_commit_message",
)


class ApiError(RuntimeError):
    """Keep GitHub's status/message so absence is not confused with denied access."""

    def __init__(self, result):
        try:
            payload = json.loads(result.stdout)
        except (ValueError, TypeError):
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        self.message = payload.get("message") or result.stderr.strip() or f"gh exited {result.returncode}"
        status = str(payload.get("status", ""))
        match = re.search(r"\(HTTP (\d{3})\)", result.stderr)
        self.status = int(status) if status.isdigit() else int(match[1]) if match else None
        super().__init__(self.message)


def expected_unavailability(endpoint, error):
    if (error.status == 404 and endpoint.startswith(f"repos/{ORG}/")
            and "/branches/" in endpoint and endpoint.endswith("/protection")
            and error.message in ("Branch not protected", "gh: Branch not protected (HTTP 404)")):
        return "classic_rule_not_configured; repository rulesets are evaluated separately"
    if (error.status == 403 and endpoint.split("?", 1)[0] == f"orgs/{ORG}/rulesets"
            and "Upgrade to GitHub Team to enable this feature" in error.message):
        return "organization_rulesets_unavailable_on_current_plan"
    # Generic 403/404s remain errors, including hidden or inaccessible resources.
    return None


def api(endpoint, paginate=False):
    command = ["gh", "api", "--hostname", "github.com", endpoint]
    if paginate:
        command += ["--paginate"]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise ApiError(result)
    if not paginate:
        return json.loads(result.stdout)
    # Older gh versions emit adjacent JSON arrays and do not support --slurp.
    remaining, merged = result.stdout.lstrip(), []
    decoder = json.JSONDecoder()
    while remaining:
        page, end = decoder.raw_decode(remaining)
        if not isinstance(page, list):
            raise ValueError("Expected a paginated array response")
        merged.extend(page)
        remaining = remaining[end:].lstrip()
    return merged


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("volparossa-settings"))
    args = parser.parse_args()
    os.umask(0o077)
    args.output.mkdir(parents=True, exist_ok=False)
    summary = {"organization": ORG, "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
               "read_only": True, "files": [], "unavailable": [], "skipped": [], "errors": []}

    def capture(name, endpoint, fields=None, paginate=False):
        try:
            value = api(endpoint, paginate)
            if fields is not None:
                value = {key: value[key] for key in fields if key in value}
            path = args.output / f"{name}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            summary["files"].append(str(path.relative_to(args.output)))
            return value
        except (OSError, RuntimeError, ValueError, TypeError, KeyError) as error:
            reason = expected_unavailability(endpoint, error) if isinstance(error, ApiError) else None
            if reason:
                summary["unavailable"].append({"endpoint": endpoint, "status": error.status,
                                               "reason": reason, "message": error.message})
                return None
            summary["errors"].append({"endpoint": endpoint, "error": str(error)})
            print(f"UNREADABLE {endpoint}: {error}", file=sys.stderr)
            return None

    def selected_actions(name, endpoint, permissions):
        if permissions is None:
            return  # The failed prerequisite is already recorded as an error.
        mode = permissions.get("allowed_actions")
        if mode == "selected":
            capture(name, endpoint)
        elif mode in ("all", "local_only") or permissions.get("enabled") is False or permissions.get("enabled_repositories") == "none":
            summary["skipped"].append({"endpoint": endpoint, "reason": "no_selected_actions_policy"})
        else:
            summary["errors"].append({"endpoint": endpoint, "error": "Unrecognized Actions permissions response"})

    capture("organization/settings", f"orgs/{ORG}", ORG_FIELDS)
    permissions = capture("organization/actions-permissions", f"orgs/{ORG}/actions/permissions")
    capture("organization/actions-permissions-workflow", f"orgs/{ORG}/actions/permissions/workflow")
    selected_actions("organization/actions-permissions-selected-actions",
                     f"orgs/{ORG}/actions/permissions/selected-actions", permissions)
    # Legacy org fields for new repositories do not establish current defaults.
    capture("organization/code-security-defaults", f"orgs/{ORG}/code-security/configurations/defaults")
    org_rulesets = capture("organization/rulesets", f"orgs/{ORG}/rulesets?per_page=100", paginate=True)
    for ruleset in org_rulesets or []:
        capture(f"organization/ruleset-{ruleset['id']}", f"orgs/{ORG}/rulesets/{ruleset['id']}")

    repos = capture("repositories", f"orgs/{ORG}/repos?per_page=100&type=all", paginate=True)
    # Replace the enumeration response with a small identity list; no private profile fields.
    if repos is not None:
        (args.output / "repositories.json").write_text(json.dumps(
            [{"full_name": repo["full_name"], "default_branch": repo["default_branch"]}
             for repo in repos], indent=2) + "\n", encoding="utf-8")
        for repo in repos:
            full_name = repo["full_name"]
            if full_name.split("/", 1)[0].lower() != ORG.lower():
                continue
            root = repo["name"]
            capture(f"{root}/settings", f"repos/{full_name}", REPO_FIELDS)
            default = quote(repo["default_branch"], safe="")
            endpoints = {
                "branch-protection": f"branches/{default}/protection",
                "rulesets": "rulesets?includes_parents=true&per_page=100",
                "actions-permissions": "actions/permissions",
                "actions-workflow-permissions": "actions/permissions/workflow",
                "environments": "environments?per_page=100",
            }
            for label, endpoint in endpoints.items():
                captured = capture(f"{root}/{label}", f"repos/{full_name}/{endpoint}",
                                   paginate=label == "rulesets")
                if label == "actions-permissions":
                    selected_actions(f"{root}/actions-selected-actions",
                                     f"repos/{full_name}/actions/permissions/selected-actions", captured)
                if label == "rulesets":
                    for ruleset in captured or []:
                        capture(f"{root}/ruleset-{ruleset['id']}",
                                f"repos/{full_name}/rulesets/{ruleset['id']}")
    (args.output / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(summary['files'])} files; {len(summary['errors'])} unreadable endpoints.")
    print(f"Recorded {len(summary['unavailable'])} explicit absence/plan limits; skipped {len(summary['skipped'])} inapplicable endpoints.")
    print(f"Read {args.output / 'SUMMARY.json'}; a missing classic rule does not mean repository rulesets are absent.")
    return 2 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
