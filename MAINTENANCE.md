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
| Ongoing | Security and routine maintenance | The reviewed [RustSec refresh #367](https://github.com/VOLPAROSSA/volparossa/pull/367) is integrated after Quality and CodeQL passed. The pin is `26fd2d43f7280a1fb925a3743ec463017afe7119`; keep the scheduled advisory review active. Minor/patch proposals are grouped; major upgrades still need individual review. Grouping is not compatibility proof: pre-1.0 minor changes, compiler requirements and deliberately exact pins still need source review. The new [Cargo group #369](https://github.com/VOLPAROSSA/volparossa/pull/369) changes exact runtime/compiler pins and requires that separate review before integration. |
| 1 | Core and consumer Storage | [Core #371](https://github.com/VOLPAROSSA/volparossa/pull/371) restores the bounded maintenance fixture on main; its new actual passes the core lifecycle but fails the subsequent Cloud deposit. Resolve that request's challenge-read deadline before the joined upload trial in cumulative [Core #279](https://github.com/VOLPAROSSA/volparossa/pull/279). [Cloud #15](https://github.com/VOLPAROSSA/volparossa-cloud/pull/15) and [Image #8](https://github.com/VOLPAROSSA/volparossa-image/pull/8) remain drafts pending complete consumer acceptance. Parked historical [Core #208](https://github.com/VOLPAROSSA/volparossa/pull/208) and [#196](https://github.com/VOLPAROSSA/volparossa/pull/196) retain distinct history, not equivalent or accepted implementations. |
| 2 | Resident Compute | Review the accumulated integration in [Core #332](https://github.com/VOLPAROSSA/volparossa/pull/332) against current main. Parked [#276](https://github.com/VOLPAROSSA/volparossa/pull/276) retains distinct source: its head is not contained in #332. Public-model evidence does not establish confidential execution. |
| 3 | Browser integration | [Browser #4](https://github.com/VOLPAROSSA/volparossa-browser/pull/4), [#5](https://github.com/VOLPAROSSA/volparossa-browser/pull/5) and [Core #211](https://github.com/VOLPAROSSA/volparossa/pull/211) need their combined core/runtime boundary reviewed. Browser branches diverge and both remain drafts. |
| 4 | Source builds and publication | [Core #350](https://github.com/VOLPAROSSA/volparossa/pull/350) owns the cumulative Weather decoder source-build review. [#345](https://github.com/VOLPAROSSA/volparossa/pull/345)/[#346](https://github.com/VOLPAROSSA/volparossa/pull/346) are parked historical records of the blocked artifact-archive design; do not activate it implicitly. [Core #342](https://github.com/VOLPAROSSA/volparossa/pull/342) retains Studio publication integration. Protected application Pages remain excluded. |

Parked Storage diagnostics [#268](https://github.com/VOLPAROSSA/volparossa/pull/268),
[#300](https://github.com/VOLPAROSSA/volparossa/pull/300),
[#285](https://github.com/VOLPAROSSA/volparossa/pull/285) and
[#339](https://github.com/VOLPAROSSA/volparossa/pull/339) support later deliberate selection for the Storage work
stream; they are closed historical reviews, not active integration or accepted features. #285 and the predecessor
of #300 diverge by one commit. Preserve that distinction when reconciling them.

## November consolidation record

The audit began with **14 repositories, 129 branches, 59 open PRs and 49
committed workflows**. Forty-two branch tips are archived, fifteen redundant reviews were closed and
nine experiments parked. Dependabot has already opened fresh grouped proposals;
the exact later counts and observation time are recorded in the audit snapshot. See the [audit snapshot](maintenance/2026-11-05/audit-summary.json). Counts
are dated observations, not live status.

Verified and merged: [Browser #20](https://github.com/VOLPAROSSA/volparossa-browser/pull/20)
(bounded workflow), [Core #360](https://github.com/VOLPAROSSA/volparossa/pull/360)
(request-bound timeout diagnostics), [Core #362](https://github.com/VOLPAROSSA/volparossa/pull/362)
(DNS cache outage/recovery proof), [Core #361](https://github.com/VOLPAROSSA/volparossa/pull/361)
(bounded geodetic/GPSD inputs) and [Image #15](https://github.com/VOLPAROSSA/volparossa-image/pull/15)
(pinned setup-node update). Their original limits remain: no complete DICN,
real-sensor positioning or consumer Storage acceptance is inferred. Image's
aggregate CodeQL check was neutral, not a successful complete scan.

[Code #29](https://github.com/VOLPAROSSA/volparossa-code/pull/29) integrates the
truncated-SSE regression contribution from #26, with original attribution, bounded
tests and verified partial-byte arrival. All 11 focused tests and hosted checks
passed. Compatible dependency grouping is integrated in Core #366, Browser #23, Code #28,
Cloud #24 and Image #18. Core #366 also integrates the architecture ownership map,
single-source documentation table and corrected F04 integration status; Quality
and all CodeQL language checks passed.

The following redundant review entries were closed; source commits and original
evidence were preserved. Cumulative reviews were retargeted to main as drafts; the additional parking
decisions below then distinguish active integration from retained experiments.

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
| Code #26 | Corrected contribution integrated as #29, preserving author attribution. |

## Parked experiments and branch archive

Core #196, #208, #268, #285, #300 and #339 are parked behind the active Storage
work stream; #276 is parked behind Compute #332; #345/#346 retain the abandoned
artifact-archive approach behind the source-build work. Their exact source refs (branches or named archive tags) and
evidence remain available. These administrative closures do not claim that the
active candidates contain their commits or satisfy their unmet requirements.
See the [exact parked heads](maintenance/2026-11-05/parked-prs.json).

**42 retired branches** were replaced atomically by
`archive/2026-11-05/<original-branch>` tags, preserving each exact commit and its
history. Every resulting remote tag and absent branch was checked. The
[archive manifest](maintenance/2026-11-05/branch-archive.json) gives the restoration
reference for each branch. Twenty-one additional historical branches were retained
because deletion could match a workflow push trigger; they require a separate
[trigger review](maintenance/2026-11-05/retained-workflow-branches.json). Open PR heads/bases and all owner-reserved repositories were excluded.

Cloud #15 and Image #8 have now normally merged current main while remaining
drafts. Image `770a23fef01cb4cc69303a433b31b9df0d26b44e` and Cloud
`9c01c932a8443e689f5fd51c1a17d6c96156821a` pass their hosted source checks and
CodeQL. Cloud pins exact Image draft bytes with explicit provenance. Full consumer
Storage acceptance still depends on Core.

[Core #371](https://github.com/VOLPAROSSA/volparossa/pull/371) is integrated as
`ba6ab458429f5ac50cdc8c3538e6d24f44aad916`, after Quality and CodeQL passed. Its
[actual trial 42116076218](https://github.com/VOLPAROSSA/volparossa/actions/runs/42116076218)
passes core maintenance, repeated restore, all-copy deletion and zero provider
usage, then fails Cloud deposit while reading its challenge length. The complete
consumer lifecycle remains open. Exact source, diagnostics and cleanup limits
belong in the [current Storage integration status](https://github.com/VOLPAROSSA/volparossa/blob/3682669226d49f7f3b71eca3e93205a74ca3d2a5/docs/IMPLEMENTATION_STATUS.md#storage-consumer-and-provider-evidence).
The current application draft pins are prepared separately and remain unpublished
while the historical consumer baseline is investigated.

Core #279 consolidates its obsolete branch-specific source workflow into Quality.
Its [42116351790](https://github.com/VOLPAROSSA/volparossa/actions/runs/42116351790)
passes the focused and workspace tests but reaches the job limit during the final
integration harness. Follow-up `3682669226d4` separates source and build jobs,
retains a mandatory final result gate and scopes the existing connection observer
to Cloud deposit. Hosted checks and a new actual remain required. Cache only
verified build inputs, never test outcomes. The whole-workflow audit
cache key also causes unnecessary rebuilds after unrelated test edits; narrowing
it requires a separate review of every build input and the existing trust boundary.

## Administrative settings

All 14 repository rulesets were read and retain default-branch deletion, history
rewrite and PR protection. Twelve code/application repositories require their
relevant Actions check. The owner subsequently supplied an export on 5 November;
it was reviewed privately and confirms the existing per-repository protection.
The two requested portal preferences are verified enabled. The raw export is not
published here, and no protection or reserved Pages configuration was changed.

The [owner export script](scripts/maintenance/export-github-settings.py) now
distinguishes GitHub's explicit absence of a classic branch rule from an unreadable
resource, records plan-specific availability separately, and queries an Actions
allowlist only when that policy is selected. Generic access failures still fail
the export. Future exports also include the current code-security configuration
defaults; legacy new-repository fields alone do not establish those defaults.
The earlier [CLI instructions](maintenance/2026-11-05/ADMINISTRATION.txt) remain
as the dated maintenance record; the received export does not need to be repeated
for the existing repositories.

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
