# VOLPAROSSA organization guidance

Follow the [shared development workflow](https://github.com/VOLPAROSSA/volparossa/blob/main/docs/development/CODEX_WORKFLOW.md) for Codex, OpenCode and other coding agents.
Start with the user's task and the relevant part of the [README](README.md).
Choose available models, reasoning effort, tools and any delegation according
to the task's complexity, risk and cost. Use targeted checks. Run builds and
runtime trials on approved disposable hosted runners.

Use the [maintenance index](MAINTENANCE.md) to find the repository that owns a
change and the [community guidance](COMMUNITY_MAINTENANCE.md) when maintaining
organization defaults. Each repository needs a root `AGENTS.md` that points to
the shared workflow and records its own instructions. GitHub's community-file
inheritance does not distribute `AGENTS.md` to repository checkouts.
