# Maintaining shared community guidance

Keep shared guidance in the public `VOLPAROSSA/.github` repository. GitHub
[uses default community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file),
including `ACCESSIBILITY.md`, when a repository has no corresponding local file.
Check `.github/`, the repository root and `docs/` for overrides, in that order.
Inherited files are not copied into repository clones or packages. Add a local
override only when the repository needs different guidance, and keep it current.

Update [accessibility guidance](ACCESSIBILITY.md) when relevant interfaces,
validation evidence or reporting routes change. Keep goals separate from verified
results; link a barrier's issue to its fix and actual test conditions.

## Checklist for a new public repository

- Confirm the default accessibility guidance appears in the repository's
  community standards view. Check for unintended local overrides; do not copy
  the shared file merely to make it appear in the source tree.
- Check that issue, discussion and private security reporting links lead to the
  intended channels. Retain repository-specific build and evidence instructions.
- Verify content reporting separately in the repository settings. This setting
  is not inherited from a Markdown file.

## Content reporting policy and verification

For a public organization repository, an administrator can open **Settings >
Access > Moderation options > Reported content**, select **Prior contributors
and collaborators**, then **Save**. Preserve **All users** where it is already
selected; do not reduce existing reporting access. See GitHub's
[reported-content instructions](https://docs.github.com/en/communities/moderating-comments-and-conversations/managing-how-contributors-report-abuse-in-your-organizations-repository).

Verify and record the selected option in the settings UI after saving.
`GET /repos/{owner}/{repo}/community/profile` exposes
`content_reports_enabled` only as a boolean; it does not identify the reporting
permission tier. An enabled boolean alone cannot verify this policy. If settings
access is unavailable, record the tier as unverified and leave the check open.
Do not infer completion from a default or from another repository's settings.
