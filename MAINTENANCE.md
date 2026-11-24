# VOLPAROSSA maintenance and integration

The owner-designated central build chat coordinates the alpha across repositories.
Its [mandate and project goal](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/development/GOAL.md)
covers pull requests, branches, worktrees, workflows, Actions and repository settings.
Older build sessions are retired.

## Start here

Choose the repository that owns the change below. For work spanning an application
and Core, use the [architecture source map](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/architecture/ARCHITECTURE.md)
to locate the shared Network, Cache, Storage, Compute or Transaction contract.
When splitting interface changes, assign distinct paths and record both source
revisions for the integration check.
Follow the [shared development workflow](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/development/WORKFLOW.md).

## Repository ownership

| Repository instructions | Responsibility |
| --- | --- |
| [volparossa](https://github.com/VOLPAROSSA/volparossa/blob/main/AGENTS.md) | Shared core, service contracts, platform integration and source-bound acceptance. |
| [.github](AGENTS.md) | Organization defaults, contribution guidance and this coordination index. |
| [volparossa.github.io](https://github.com/VOLPAROSSA/volparossa.github.io/blob/main/AGENTS.md) | Public organization portal and product navigation. |
| [volparossa-browser](https://github.com/VOLPAROSSA/volparossa-browser/blob/main/AGENTS.md) | Browser source integration and scoped core adapters. |
| [volparossa-code](https://github.com/VOLPAROSSA/volparossa-code/blob/main/AGENTS.md) | Coding interface and execution integration. |
| [volparossa-cloud](https://github.com/VOLPAROSSA/volparossa-cloud/blob/main/AGENTS.md) | Cloud file interface and core storage consumer. |
| [volparossa-image](https://github.com/VOLPAROSSA/volparossa-image/blob/main/AGENTS.md) | Image interface and core compute/storage consumer. |
| [volparossa-mail](https://github.com/VOLPAROSSA/volparossa-mail/blob/main/AGENTS.md) | Mail application. |
| [volparossa-chat](https://github.com/VOLPAROSSA/volparossa-chat/blob/main/AGENTS.md) | Chat application. |
| [volparossa-map](https://github.com/VOLPAROSSA/volparossa-map/blob/main/AGENTS.md) | Map application and positioning integration. |
| [volparossa-weather](https://github.com/VOLPAROSSA/volparossa-weather/blob/main/AGENTS.md) | Weather clients and bounded source/runtime integration. |
| [volparossa-bank](https://github.com/VOLPAROSSA/volparossa-bank/blob/main/AGENTS.md) | Bank application and explicit TEST transaction integration. |
| [volparossa-citizen](https://github.com/VOLPAROSSA/volparossa-citizen/blob/main/AGENTS.md) | Citizen application. |
| [volparossa-studio](https://github.com/VOLPAROSSA/volparossa-studio/blob/main/AGENTS.md) | Studio authoring, local preview and authorized publication integration. |

## Active integration queue

Use the [organization’s open pull requests](https://github.com/pulls?q=is%3Apr+is%3Aopen+org%3AVOLPAROSSA+sort%3Aupdated-desc)
to find work in progress before starting another branch. The
[Core implementation status](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/IMPLEMENTATION_STATUS.md)
records shared dependencies, priorities and verified results. Check the owning
repository's evidence for application behavior. Before integrating a change,
refresh the PR head, base, diff and required checks.

Maintain application code, public documentation and existing websites through their ordinary repository checks. Keep public claims tied to working features and original evidence. Financial and legal commitments, external outreach and DNS or hosting changes follow the owner's authorization in the project goal.

## Maintenance rules

- Keep one active review per cumulative implementation; close superseded entries
  only after proving ancestry or exact equivalence. Distinct alternatives stay
  explicit. Closing a PR never supplies missing acceptance evidence.
- Retired branch tips may move to named archive tags only after checking current
  refs and open PR heads/bases. Never overwrite an archive tag or rewrite history.
- Required checks and protection rules stay in force. All audited external action
  references were pinned; workflows already use explicit permissions and checkout
  credential controls. Keep manual acceptance workflows where they prove different
  boundaries; a smaller workflow count is not itself an improvement.
- Verify administrative settings through an authorized owner export. An inaccessible
  setting is unknown, not absent. Do not replace branch protections from a template
  without reading the current configuration.
- Cache only verified build inputs. Review their trust boundaries before narrowing a cache key.
- Record shared capability changes once in Core status. Link to the original
  evidence and retain failures in the owning repository.

## Retained evidence

The [November integration record](maintenance/2026-11-19/integration-record.md) preserves the former queue and its source revisions.

### [November consolidation record](maintenance/2026-11-19/integration-record.md#november-consolidation-record)

### [Parked experiments and branch archive](maintenance/2026-11-19/integration-record.md#parked-experiments-and-branch-archive)

### [Earlier Storage trials](maintenance/2026-11-19/integration-record.md#earlier-storage-trials)

### [Administrative settings](maintenance/2026-11-19/integration-record.md#administrative-settings)
