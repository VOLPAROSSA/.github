# VOLPAROSSA maintenance and integration

This is the organization-wide starting point for development coordination.
The central maintenance session established on **5 November 2026** owns the
active queue; older sessions are retired. Repository requirements, source-bound
evidence and GitHub protections remain authoritative. This index coordinates
them without declaring unfinished features accepted.

## Start here

1. Read the [goal](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/development/GOAL.md)
   and [current implementation status](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/IMPLEMENTATION_STATUS.md)
   for the affected capability.
2. Use the [architecture source map](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/architecture/ARCHITECTURE.md)
   to extend its existing owner. Network, Cache, Storage, Compute and Transaction
   are shared responsibilities, not a reason to add parallel daemons or ledgers.
3. Choose one bounded result from the queue below. Refresh its live head, base,
   diff and required checks before integrating; a historical green run is valid
   only for the inputs it actually tested.
4. Follow [AGENTS](https://github.com/VOLPAROSSA/volparossa/blob/main/AGENTS.md)
   and the [shared workflow](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/development/CODEX_WORKFLOW.md).
   Put current capability evidence in implementation status, original failures
   in their retained record, and cross-repository coordination here.

## Repository ownership

| Repository | Responsibility |
| --- | --- |
| [volparossa](https://github.com/VOLPAROSSA/volparossa) | Shared core, service contracts, platform integration and source-bound acceptance. |
| [.github](https://github.com/VOLPAROSSA/.github) | Organization defaults, contribution guidance and this coordination index. |
| [volparossa.github.io](https://github.com/VOLPAROSSA/volparossa.github.io) | Public organization portal and product navigation. |
| [volparossa-browser](https://github.com/VOLPAROSSA/volparossa-browser) | Browser source integration and scoped core adapters. |
| [volparossa-code](https://github.com/VOLPAROSSA/volparossa-code) | Coding interface and execution integration. |
| [volparossa-cloud](https://github.com/VOLPAROSSA/volparossa-cloud) | Cloud file interface and core storage consumer. |
| [volparossa-image](https://github.com/VOLPAROSSA/volparossa-image) | Image interface and core compute/storage consumer. |
| [volparossa-mail](https://github.com/VOLPAROSSA/volparossa-mail) | Mail application. |
| [volparossa-chat](https://github.com/VOLPAROSSA/volparossa-chat) | Chat application. |
| [volparossa-map](https://github.com/VOLPAROSSA/volparossa-map) | Map application and positioning integration. |
| [volparossa-weather](https://github.com/VOLPAROSSA/volparossa-weather) | Weather clients and bounded source/runtime integration. |
| [volparossa-bank](https://github.com/VOLPAROSSA/volparossa-bank) | Bank application and explicit TEST transaction integration. |
| [volparossa-citizen](https://github.com/VOLPAROSSA/volparossa-citizen) | Citizen application. |
| [volparossa-studio](https://github.com/VOLPAROSSA/volparossa-studio) | Studio authoring, local preview and authorized publication integration. |

**Owner-reserved work:** the GitHub Pages of Mail, Map, Weather, Studio, Bank,
Citizen and Chat remain with the owner. Do not modify their site content,
publication workflows, Pages settings or shared portal content that would change
those pages. The November maintenance pass leaves those seven repositories
unchanged. Any later non-site work in them must keep this boundary explicit.

## Active integration queue

Use these as work streams, not instructions to merge every linked PR.
Each retained cumulative draft must reconcile with current main and pass the
relevant checks before it becomes an integration candidate.

| Order | Work stream | Next concrete result / retained review |
| --- | --- | --- |
| 1 | Security and routine maintenance | Finish the reviewed [RustSec refresh #367](https://github.com/VOLPAROSSA/volparossa/pull/367) under the existing Quality gate. Compatible dependency updates are grouped; major upgrades still need individual review. |
| 2 | Core and consumer Storage | Start with the cumulative [Core #279](https://github.com/VOLPAROSSA/volparossa/pull/279), [Cloud #15](https://github.com/VOLPAROSSA/volparossa-cloud/pull/15) and [Image #8](https://github.com/VOLPAROSSA/volparossa-image/pull/8). Reconcile current main, then prove one complete upload/renew/repair/restore/delete lifecycle with bounded authority and cleanup. Earlier [Core #208](https://github.com/VOLPAROSSA/volparossa/pull/208) and [#196](https://github.com/VOLPAROSSA/volparossa/pull/196) contain distinct history and are not claimed equivalent. |
| 3 | Resident Compute | Review the accumulated integration in [Core #332](https://github.com/VOLPAROSSA/volparossa/pull/332) against current main. Retain [#276](https://github.com/VOLPAROSSA/volparossa/pull/276) as a distinct cumulative draft: its current head is not contained in #332. Public-model evidence does not establish confidential execution. |
| 4 | Browser integration | [Browser #4](https://github.com/VOLPAROSSA/volparossa-browser/pull/4), [#5](https://github.com/VOLPAROSSA/volparossa-browser/pull/5) and [Core #211](https://github.com/VOLPAROSSA/volparossa/pull/211) need their combined core/runtime boundary reviewed. Browser branches diverge and both remain drafts. |
| 5 | Source builds and publication | [Core #350](https://github.com/VOLPAROSSA/volparossa/pull/350) owns the cumulative Weather decoder source-build review. [#345](https://github.com/VOLPAROSSA/volparossa/pull/345)/[#346](https://github.com/VOLPAROSSA/volparossa/pull/346) retain the separate blocked artifact-archive design; do not activate it implicitly. [Core #342](https://github.com/VOLPAROSSA/volparossa/pull/342) retains Studio publication integration. Protected application Pages remain excluded. |

Storage diagnostics [#268](https://github.com/VOLPAROSSA/volparossa/pull/268),
[#300](https://github.com/VOLPAROSSA/volparossa/pull/300),
[#285](https://github.com/VOLPAROSSA/volparossa/pull/285) and
[#339](https://github.com/VOLPAROSSA/volparossa/pull/339) support the Storage work
stream; they are not four independent product milestones. #285 and the predecessor
of #300 diverge by one commit. Preserve that distinction when reconciling them.

## November consolidation record

The audit began with **14 repositories, 129 branches, 59 open PRs and 49
committed workflows**. Counts are a dated baseline, not live status.

Verified and merged: [Browser #20](https://github.com/VOLPAROSSA/volparossa-browser/pull/20)
(bounded workflow), [Core #360](https://github.com/VOLPAROSSA/volparossa/pull/360)
(request-bound timeout diagnostics), [Core #362](https://github.com/VOLPAROSSA/volparossa/pull/362)
(DNS cache outage/recovery proof), [Core #361](https://github.com/VOLPAROSSA/volparossa/pull/361)
(bounded geodetic/GPSD inputs) and [Image #15](https://github.com/VOLPAROSSA/volparossa-image/pull/15)
(pinned setup-node update). Their original limits remain: no complete DICN,
real-sensor positioning or consumer Storage acceptance is inferred. Image's
aggregate CodeQL check was neutral, not a successful complete scan.

The following redundant review entries were closed; source commits and original
evidence were preserved. Cumulative survivors now target main and remain drafts.

| Closed review | Retained review / reason |
| --- | --- |
| Core #347 | Integrated #349; historical precursor. |
| Core #356 | Exact duplicate tree and parent of #353. |
| Core #194 | Ancestor of #208; #196 remains distinct. |
| Core #233 | Ancestor of #279. |
| Core #267 | Cumulative #268. |
| Core #271, #272 | Cumulative #276. |
| Core #287 | Cumulative #300; #285 divergence retained. |
| Core #340 | Ancestor of #342. |
| Core #348 | Cumulative #350. |
| Cloud #13, #14 | Cumulative #15. |
| Image #6, #7 | Cumulative #8. |

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
- Keep the queue concise. On integration, update capability status and this queue;
  retain exact original evidence through links instead of copying long session logs.
