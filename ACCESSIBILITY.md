# Accessibility and inclusive participation

VOLPAROSSA aims to make its privacy-first, modular open-source software and
community accessible to people with different abilities, devices and ways of
working. Inclusive participation and user autonomy guide this work.

## Development goals and current limitations

For applications, websites and documentation we develop or change,
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) Level AA is a development goal,
not a statement of conformance. Priorities include:

- Keyboard operation, logical focus order, visible focus and no keyboard traps.
- Semantic headings, controls and labels, useful text alternatives, and clear
  status and error messages for screen-reader users.
- Sufficient contrast and information that does not depend on color alone.
- Readable typography, text resizing and reflow on small screens and at zoom.
- Respect for reduced-motion preferences and control over unnecessary animation.

The project has not had a complete accessibility audit. Applications remain
experimental, and upstream interfaces may have barriers outside our changes.
Platform targets and build availability do not establish accessibility support.
There is no validated support matrix for assistive technologies. Test results
apply only to the stated revision, task and environment; untested combinations
remain unverified.

## Report a barrier

Search the affected repository's issues, then describe the task or interface,
expected behavior, observed barrier and smallest safe reproduction. Include the
revision and relevant operating system, browser or app version; add assistive
technology and its version if useful and you are comfortable sharing them.
Screenshots are optional; text reports are welcome. Do not share a diagnosis,
medical record, credentials, private files, browsing history or raw private logs.

If issues are unavailable or you need help finding the right repository, use
[central Discussions](https://github.com/VOLPAROSSA/volparossa/discussions).
For a vulnerability or a report needing confidential security details, follow
[SECURITY.md](SECURITY.md) and its private reporting instructions.

## Contribute and maintain

For a focused change, check the affected task with a keyboard, inspect semantics
and labels, and test small screens, text resizing or 200% zoom, contrast and
reduced motion as relevant. Screen-reader checks are welcome. Record the exact
revision, environment, steps and results, including barriers you could not fix.
Automated checks help find problems but do not prove accessibility.

Maintainers triage barriers by their impact on completing a task, link fixes and
validation to the issue, and revisit this guidance when relevant interfaces,
evidence or reporting routes change. Review, response dates and fixes are not
guaranteed.

Translations are welcome. Start with one bounded page or interface and identify
its source revision and language. Preserve technical limitations, safety warnings,
licenses and attribution. Coordinate terminology in the relevant issue rather
than creating a parallel, unmaintained documentation tree. No translation or
particular assistive technology is currently promised ongoing support.
