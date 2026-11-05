#!/usr/bin/env python3
"""Read-only VOLPAROSSA settings export. Requires Python 3 and authenticated gh."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
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


def api(endpoint, paginate=False):
    command = ["gh", "api", "--hostname", "github.com", endpoint]
    if paginate:
        command += ["--paginate"]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"gh exited {result.returncode}")
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
               "read_only": True, "files": [], "errors": []}

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
            summary["errors"].append({"endpoint": endpoint, "error": str(error)})
            print(f"UNREADABLE {endpoint}: {error}", file=sys.stderr)
            return None

    capture("organization/settings", f"orgs/{ORG}", ORG_FIELDS)
    for suffix in ("actions/permissions", "actions/permissions/workflow",
                   "actions/permissions/selected-actions"):
        capture("organization/" + suffix.replace("/", "-"), f"orgs/{ORG}/{suffix}")
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
                "actions-selected-actions": "actions/permissions/selected-actions",
                "environments": "environments?per_page=100",
            }
            for label, endpoint in endpoints.items():
                captured = capture(f"{root}/{label}", f"repos/{full_name}/{endpoint}",
                                   paginate=label == "rulesets")
                if label == "rulesets":
                    for ruleset in captured or []:
                        capture(f"{root}/ruleset-{ruleset['id']}",
                                f"repos/{full_name}/rulesets/{ruleset['id']}")
    (args.output / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(summary['files'])} files; {len(summary['errors'])} unreadable endpoints.")
    print(f"Read {args.output / 'SUMMARY.json'}; 403/404 responses are not proof of absent protections.")
    return 2 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
