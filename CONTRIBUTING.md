# Contributing to VOLPAROSSA

Help make cooperative infrastructure understandable, useful and verifiable.
VOLPAROSSA is an early-stage open-source project; careful questions and small
improvements are welcome alongside code. There is no required donation or
financial relationship to contribute.

## Choose a starting point

Read the relevant repository README and linked status. The
[documentation guide](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/README.md)
connects the shared architecture, applications and evidence. Repository-specific
instructions and build guides take precedence over these defaults.

| Your interest | A useful first contribution |
| --- | --- |
| Documentation or education | Fix an unclear instruction or broken link; say where you got stuck and validate the revised steps. |
| Design and accessibility | Check one page with a keyboard, small screen or screen reader; report the exact barrier and propose a focused fix. |
| Translation | Translate a bounded, agreed page while preserving safety qualifications and source revision. |
| Testing | Reproduce an existing unprivileged example using public fixtures and report the exact source, command and result. |
| Research | Review one documented assumption or compare a method using primary sources and explicit limitations. |
| Development | Pick a bounded issue with an observable outcome; follow that repository's dependency and test instructions. |

Search [introductory issues](https://github.com/search?q=org%3AVOLPAROSSA+is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22&type=issues)
or [requests for help](https://github.com/search?q=org%3AVOLPAROSSA+is%3Aissue+is%3Aopen+label%3A%22help+wanted%22&type=issues).
Labels identify scope, not a promise of mentoring or immediate review. If nothing
fits, describe a small improvement in the owning repository before starting a
large change. Use [central Discussions](https://github.com/VOLPAROSSA/volparossa/discussions)
for general and cross-project questions; keep actionable bugs in their owning repo.

## Prepare your change

1. Check the current default branch, README, applicable `AGENTS.md` and status.
2. Create a topic branch or fork. Keep unrelated work separate.
3. Follow the repository's reproducible dependency and build instructions. For
   the core, use the [contributor guide](https://github.com/VOLPAROSSA/volparossa/blob/main/CONTRIBUTING.md)
   and [operations guide](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/development/OPERATIONS.md).
4. Make the smallest complete change that addresses the stated problem. Preserve
   privacy boundaries, fail-closed behavior, upstream licenses and provenance.
5. Run focused checks appropriate to the change. Documentation changes need
   link and claim checks; they do not require pretending to run a network trial.
6. Open a pull request explaining the problem, result, actual verification and
   remaining limitations. Existing branch protections and review rules apply.

Network tests belong only in disposable namespaces or the documented disposable
VM topology. Do not change your active routes, DNS, firewall, sysctls or VPN to
try a contribution. Never use real private data in public fixtures or peer trials.
Do not submit secrets, identifiable traffic captures or raw private logs.

Keep **intended**, **implemented**, **tested on an exact revision** and **unfinished**
claims distinct. Do not present simulation, ordinary TCP or single-path QUIC as
proof of a real multipath or distributed service. Preserve failures in the evidence.

## Review and collaboration

Follow the [code of conduct](CODE_OF_CONDUCT.md). Explain tradeoffs, credit prior
work and respond to review with evidence. AI assistance does not remove your
responsibility to understand, verify and license a contribution. Disclose material
AI assistance and check any applicable upstream or funding restrictions before
using it; never put private project data into an unauthorized service. Do not use
AI-generated text for an application whose funder forbids it.

Maintainer time is limited; review and support have no fixed turnaround. Work may
need revision or be declined where it conflicts with scope, privacy or evidence.
Report vulnerabilities through [SECURITY.md](SECURITY.md), not a public issue.
