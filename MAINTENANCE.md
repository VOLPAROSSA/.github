# VOLPAROSSA maintenance and integration

The owner-designated central build chat coordinates the full VOLPAROSSA alpha across repositories. It manages pull requests, branches, worktrees, workflows, Actions and repository settings. Older build sessions are retired. The project goal defines the scope and the implementation status records what has run. [Project goal and mandate](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/development/GOAL.md) · [Implementation status](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/IMPLEMENTATION_STATUS.md)

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

Maintain application code, public documentation and existing websites through their ordinary repository checks. Keep public claims tied to working features and original evidence. Financial and legal commitments, external outreach and DNS or hosting changes follow the owner's authorization in the project goal.

## Active integration queue

| Work stream | Current dependency and evidence |
| --- | --- |
| Storage, Image and Cloud | Finish a single twelve-node run through publication, repair, cold restore and deletion with zero usage at all three providers. The foreground Cloud upload has already recovered the original bytes after provider loss. The next joined run exercises the bounded challenge retry and durable owner accounting. [Combined trial](https://github.com/VOLPAROSSA/volparossa/actions/runs/44430761553) · [Core #279](https://github.com/VOLPAROSSA/volparossa/pull/279) · [Image #8](https://github.com/VOLPAROSSA/volparossa-image/pull/8) · [Cloud #15](https://github.com/VOLPAROSSA/volparossa-cloud/pull/15) |
| Private Compute | The ordinary owner path refused four requests in the no-device trial and released no private input. Positive private execution requires a machine that can supply the approved hardware evidence. [Refusal and public receipts](https://github.com/VOLPAROSSA/volparossa/pull/394) · [Verified public resident session](https://github.com/VOLPAROSSA/volparossa/pull/332) |
| Browser and Code | The pinned Firefox source built offline. Its first runtime reached the first origin request and stopped at the second. Verify both HTTPS requests and disconnection on the corrected origin, then complete the cooperative path. Code's model-driven read, edit and test scenario still needs the production editor UI. [Firefox](https://github.com/VOLPAROSSA/volparossa/pull/211) · [Cooperative Browser](https://github.com/VOLPAROSSA/volparossa-browser/pull/5) · [OpenCode trial](https://github.com/VOLPAROSSA/volparossa-code/actions/runs/38824828727) |
| Studio and Weather | Complete independent Studio retrieval after publication and keep the actual editor exports and owner recovery reproducible. Weather's two cold Drizz.li builds produced identical output in all 97 files. The separate Flutter build is tracked with Overmorrow. [Studio publication](https://github.com/VOLPAROSSA/volparossa/pull/393) · [Drizz.li comparison](https://github.com/VOLPAROSSA/volparossa-weather/pull/41) · [Overmorrow](https://github.com/VOLPAROSSA/volparossa-weather/pull/35) |
| Applications | Follow the actual client through restart or expiry. Thunderbird recovered the original message from a restarted mailbox. The Signal Desktop receipt test reopened the four original rows with their expected states. Continue the peer Map traffic path and native verification of synthetic Citizen counts. [Mail](https://github.com/VOLPAROSSA/volparossa-mail/pull/15) · [Chat](https://github.com/VOLPAROSSA/volparossa-chat/pull/17) · [Map](https://github.com/VOLPAROSSA/volparossa/pull/403) · [Citizen](https://github.com/VOLPAROSSA/volparossa-citizen/pull/9) |
| Transactions and maintenance | Four validators replayed the same Bank TEST transfers after restart. Current Core includes the maintained D-Bus integration and keeps ordinary main Quality runs from canceling each other. Reconcile the X.509 update with the SEV certificate verifier. [Bank replay](https://github.com/VOLPAROSSA/volparossa/pull/391) · [D-Bus](https://github.com/VOLPAROSSA/volparossa/pull/396) · [Quality](https://github.com/VOLPAROSSA/volparossa/pull/398) · [X.509 migration](https://github.com/VOLPAROSSA/volparossa/issues/404) |

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
reference for each branch. Twenty-one additional historical branches were initially
retained for [trigger review](maintenance/2026-11-05/retained-workflow-branches.json).
That review and a bounded deletion canary are complete, but GitHub's rule engine
then rejected archival even for one atomic branch/tag pair with
`fatal error in commit_refs_rules`. At the 5 November observation, all 21 original heads were present, with
no new archive tags. The [follow-up record](maintenance/2026-11-05/retained-workflow-review.json)
preserves the source checks, observed limits and rejection; resume from those facts.
The 5 November pass excluded open PR heads and bases and the application sites reserved at the time.

On 19 November, seven completed F04 Clippy experiment branches from the retained list were archived. Each atomic push created a tag at the exact original commit and removed its branch. A fresh remote lookup verified every pair. The archive records the successful and failed Actions runs and their original source revisions. [Seven archived experiments](maintenance/2026-11-19/f04-workflow-archive.json)

### Earlier Storage trials

On 5 November, Cloud #15 and Image #8 had merged the then-current main while remaining
drafts. Image `770a23fef01cb4cc69303a433b31b9df0d26b44e` and Cloud
`9c01c932a8443e689f5fd51c1a17d6c96156821a` pass their hosted source checks and
CodeQL. Cloud pins exact Image draft bytes with explicit provenance. Full consumer
Storage acceptance still depends on Core.

On `5186411b`, Core again restored the archive twice, deleted eleven copies
and reached zero usage on all three Core providers. The fixture reduced the
Cloud catalog GnuPG socket path from 105 to 102 bytes. Quality and CodeQL
passed. The catalog's single Storage restore returned
`retained_operation_incomplete` with `restore_verified=false`. It stopped
before Cloud could decrypt the file using the shorter path. The three consumer
providers still held 6, 6 and 4 leases. Guest cleanup recorded zero remaining
fixture-owned objects.
[Quality](https://github.com/VOLPAROSSA/volparossa/actions/runs/44348766162) · [CodeQL](https://github.com/VOLPAROSSA/volparossa/actions/runs/44348748897) · [Exact-source trial](https://github.com/VOLPAROSSA/volparossa/actions/runs/44348799240) · [Trial artifact](https://github.com/VOLPAROSSA/volparossa/actions/runs/44348799240/artifacts/14452602822)

On `49955656`, the foreground `storage peer progress` call succeeded. Core
restored the archive twice, deleted all eleven copies and independently measured
zero leases and bytes at each of its three providers. The same call now has an
opt-in bounded failure diagnostic. The hosted CLI test verified its exit status
and JSON output. The collector test verified byte-for-byte retention of a
synthetic foreground failure receipt.

Consumer publication stopped at `cloud_catalog_create` with
`catalog_materialization_failed`. The Cloud catalog's single Storage restore
returned `ok` with verified content and a joined local process. The catalog
failure remains unclassified within that step. The three consumer providers
still had 6, 6 and 4 leases. The VM reported zero remaining fixture-owned objects.
[Quality](https://github.com/VOLPAROSSA/volparossa/actions/runs/44341148430) · [CodeQL](https://github.com/VOLPAROSSA/volparossa/actions/runs/44341135770) · [Exact-source trial](https://github.com/VOLPAROSSA/volparossa/actions/runs/44341178239) · [Trial artifact](https://github.com/VOLPAROSSA/volparossa/actions/runs/44341178239/artifacts/14445958116)

The previous revision `ff268f3e` bounds a client MPTCP connection attempt by
the caller deadline and the worker lease. The required Quality gate and all five
CodeQL analyses passed. The end-to-end trial stopped during Core upload when
foreground `storage peer progress` exited during a maintenance turn. The first
failing CLI operation is known. Its underlying error remains unclassified.
Local cleanup reported zero owned objects. Image and Cloud were never started.
[Quality](https://github.com/VOLPAROSSA/volparossa/actions/runs/44330047802) · [CodeQL](https://github.com/VOLPAROSSA/volparossa/actions/runs/44330036879) · [Exact-source trial](https://github.com/VOLPAROSSA/volparossa/actions/runs/44332080434)

The preceding trial on `11a1c34e` stored eight fragment copies, then could not
select a route after Core restarted. Earlier runs reached Image after Core
deleted eleven copies and all three providers reported zero usage. Image then
failed during publication and left consumer leases outstanding.
[Restart trial](https://github.com/VOLPAROSSA/volparossa/actions/runs/44325758765) · [Consumer evidence and source revisions](https://github.com/VOLPAROSSA/volparossa/blob/ff268f3e40a9fdc4eceae2ae10a27f87accc3f58/docs/IMPLEMENTATION_STATUS.md#storage-consumer-and-provider-evidence) · [Earlier combined trial](https://github.com/VOLPAROSSA/volparossa/actions/runs/44301340772)

On the earlier combined source `2a8b4fdf`, all 21 Storage source suites,
the build and the required Quality gate passed. All five CodeQL analyses passed. [Quality](https://github.com/VOLPAROSSA/volparossa/actions/runs/42147777520) · [CodeQL](https://github.com/VOLPAROSSA/volparossa/actions/runs/42147771678)

The earlier trial on `3e8a27e3` passed Core maintenance through two restores,
deletion of eleven copies and independent zero usage at three providers. Image
then failed to acquire a transport for APPEND. Core #279 adds nine diagnostic
codes for existing acquisition failure points and a regression test for a retry
on the same worker. [Original failed trial](https://github.com/VOLPAROSSA/volparossa/actions/runs/42133516630) · [Storage source history](https://github.com/VOLPAROSSA/volparossa/blob/2a8b4fdff5eec755cbad14998d2411f54c066cbe/docs/IMPLEMENTATION_STATUS.md#storage-consumer-and-provider-evidence)

Cache only verified build inputs, never test outcomes. Narrowing the whole-workflow
audit cache key still requires separate review of every build input and its trust
boundary.

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
