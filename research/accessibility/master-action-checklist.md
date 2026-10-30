# Master accessibility action checklist for web projects

**Version:** 0.2.0, 2026-10-30. **Status:** research draft for expert review.

This checklist translates WCAG 2.2 into practical actions for building and reviewing websites. It is a study resource, not a validated intervention, test suite, or conformance claim.

**How to use it:** Inventory the actual pages, states, and tasks first. Apply each item only when its feature and conditions exist. Consult the linked WCAG criterion, definitions, exceptions, and conformance requirements before deciding whether it passes. Requirements can be met in different ways. Missing required features are functional failures and may make dependent checks unassessable.

The source is the [12 December 2024 WCAG 2.2 Recommendation](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), especially Levels A and AA. The complete criterion index, including AAA, is in [master-checklist.md](master-checklist.md). A guidance item can also refer to an AAA criterion. Related criterion links identify the topic; a checked action does not prove that the entire criterion passes. This checklist does not cover every accessibility need or establish legal compliance.

[Sources and AI evidence](sources-and-ai-evidence.md) separates published observations from untested hypotheses. Items in this checklist are potential checks; they are not claims that the selected models or sites have failed them.

### Item labels

- **R: WCAG-derived outcome.** A plain-language summary of a requirement, subject to the linked criterion and exceptions. It is not the normative text.
- **G: Guidance.** A possible technique or interaction pattern. Its underlying outcome can still be required by WCAG.
- **P: Research process.** A proposed study or review practice, not a WCAG success criterion.

**Review methods** are possible approaches: manual, keyboard, visual, assistive technology, and automated. They are not complete procedures, and automated checks cannot determine conformance alone. A checklist item may need several tests, states, devices, or reviewers.

For a criterion or relevant R item, record **pass**, **fail**, **not applicable**, **unassessable**, or **not tested**, with evidence and rationale. A G item records use of one optional technique; not using it does not by itself establish a WCAG failure. Record P items as study activities, not website defects. Do not count unchecked items as failures. Freeze the checklist, test protocol, and any scoring rules before confirmatory runs. Keep this evaluation reference out of the unmodified baseline prompt.

Numeric context: large text is at least 18 pt or 14 pt bold under WCAG's definition. Reflow includes exceptions for content requiring two-dimensional layout. Target size has spacing and other exceptions. The text-spacing criterion specifies line height 1.5 times font size, following paragraph spacing 2 times, letter spacing 0.12 times, and word spacing 0.16 times.

## Scope and preparation

- [ ] <a id="act-001"></a> **ACT-001 [P]** Inventory pages, routes, dialog states, and complete user journeys before review.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-002"></a> **ACT-002 [P]** Record the requested features and identify missing or nonfunctional features separately.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-003"></a> **ACT-003 [P]** Determine which checklist items apply to each implemented page, state, and process.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-004"></a> **ACT-004 [P]** Record the browser, viewport, operating system, and assistive technologies used for testing.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-005"></a> **ACT-005 [P]** Test each relevant loading, empty, success, error, and disabled state that exists.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual, keyboard.
- [ ] <a id="act-006"></a> **ACT-006 [P]** Do not treat an untested item, missing feature, or tool error as a pass.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-007"></a> **ACT-007 [P]** Consult the linked criterion and its exceptions before reporting a WCAG failure.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-008"></a> **ACT-008 [P]** Involve people with disabilities and assistive-technology expertise where feasible.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-009"></a> **ACT-009 [P]** Include embedded and third-party content in scope when it forms part of the experience.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-010"></a> **ACT-010 [P]** Preserve original generated artifacts and record any changes made for testing.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.

## Page structure, reading order, and language

- [ ] <a id="act-011"></a> **ACT-011 [R]** Provide a descriptive page title for every page.<br>
  Sources: [2.4.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#page-titled). Possible checks: manual, automated.
- [ ] <a id="act-012"></a> **ACT-012 [R]** Expose the default human language of each page programmatically.<br>
  Sources: [3.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#language-of-page). Possible checks: manual, automated.
- [ ] <a id="act-013"></a> **ACT-013 [R]** Identify changes in human language programmatically when the criterion applies.<br>
  Sources: [3.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#language-of-parts). Possible checks: manual, assistive-technology.
- [ ] <a id="act-014"></a> **ACT-014 [R]** Expose meaningful headings and the relationships they convey programmatically or in text.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships). Possible checks: manual, assistive-technology.
- [ ] <a id="act-015"></a> **ACT-015 [R]** Write headings and labels that describe their topic or purpose.<br>
  Sources: [2.4.6](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#headings-and-labels). Possible checks: manual.
- [ ] <a id="act-016"></a> **ACT-016 [R]** Make a correct reading sequence programmatically determinable when the presentation order affects meaning.<br>
  Sources: [1.3.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#meaningful-sequence). Possible checks: manual, assistive-technology.
- [ ] <a id="act-017"></a> **ACT-017 [R]** Expose meaningful list relationships programmatically or in text.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships). Possible checks: manual, assistive-technology.
- [ ] <a id="act-018"></a> **ACT-018 [R]** Expose meaningful group and section relationships programmatically or in text.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships). Possible checks: manual, assistive-technology.
- [ ] <a id="act-019"></a> **ACT-019 [R]** Provide a way to bypass repeated blocks when they appear on multiple pages.<br>
  Sources: [2.4.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#bypass-blocks). Possible checks: manual, keyboard.
- [ ] <a id="act-020"></a> **ACT-020 [R]** Offer multiple ways to locate pages in a set, subject to the process exception.<br>
  Sources: [2.4.5](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#multiple-ways). Possible checks: manual.
- [ ] <a id="act-021"></a> **ACT-021 [R]** Keep repeated navigation in consistent relative order unless the user changes it.<br>
  Sources: [3.2.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#consistent-navigation). Possible checks: manual.
- [ ] <a id="act-022"></a> **ACT-022 [R]** Identify components with the same functionality consistently across a set of pages.<br>
  Sources: [3.2.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#consistent-identification). Possible checks: manual, assistive-technology.
- [ ] <a id="act-023"></a> **ACT-023 [R]** Keep repeated help mechanisms in consistent relative order when the criterion applies.<br>
  Sources: [3.2.6](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#consistent-help). Possible checks: manual.
- [ ] <a id="act-024"></a> **ACT-024 [G]** Use native headings, lists, landmarks, and other HTML elements when they convey the intended structure.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: manual, assistive-technology.
- [ ] <a id="act-025"></a> **ACT-025 [G]** Consider a skip link that reaches the main content when repeated navigation is present.<br>
  Sources: [2.4.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#bypass-blocks), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: keyboard.
- [ ] <a id="act-026"></a> **ACT-026 [G]** Avoid positive tabindex values that can make focus order difficult to maintain.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: manual, keyboard.

## Images, icons, links, and instructions

- [ ] <a id="act-027"></a> **ACT-027 [R]** Give meaningful images an equivalent text alternative, accounting for applicable exceptions.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content). Possible checks: manual, assistive-technology, automated.
- [ ] <a id="act-028"></a> **ACT-028 [R]** Give image-based controls a text alternative that communicates their purpose.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value). Possible checks: manual, assistive-technology.
- [ ] <a id="act-029"></a> **ACT-029 [R]** Allow decorative non-text content to be ignored by assistive technology when appropriate.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content). Possible checks: manual, assistive-technology.
- [ ] <a id="act-030"></a> **ACT-030 [R]** Supply equivalent information for informative charts, diagrams, and complex images.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content). Possible checks: manual, assistive-technology.
- [ ] <a id="act-031"></a> **ACT-031 [R]** Give non-text CAPTCHA a text alternative that identifies and describes its purpose. Provide alternatives for different sensory abilities.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content). Possible checks: manual.
- [ ] <a id="act-032"></a> **ACT-032 [R]** Make each link purpose clear from its text or programmatically determined context, subject to the criterion exception.<br>
  Sources: [2.4.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#link-purpose-in-context). Possible checks: manual, assistive-technology.
- [ ] <a id="act-033"></a> **ACT-033 [R]** Avoid instructions that rely solely on sensory characteristics such as position, shape, or sound.<br>
  Sources: [1.3.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#sensory-characteristics). Possible checks: manual.
- [ ] <a id="act-034"></a> **ACT-034 [R]** Do not use color as the only visual means to convey information, actions, response prompts, or distinctions.<br>
  Sources: [1.4.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#use-of-color). Possible checks: manual.
- [ ] <a id="act-035"></a> **ACT-035 [R]** Use text rather than images of text when technology permits the presentation, subject to the criterion exceptions.<br>
  Sources: [1.4.5](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#images-of-text). Possible checks: manual.
- [ ] <a id="act-036"></a> **ACT-036 [R]** Include the visible text of a control in its accessible name when the criterion applies.<br>
  Sources: [2.5.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#label-in-name). Possible checks: manual, assistive-technology.
- [ ] <a id="act-037"></a> **ACT-037 [G]** For an icon-only button, provide a meaningful accessible name describing its action.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C images tutorial](https://www.w3.org/WAI/tutorials/images/). Possible checks: manual, assistive-technology.
- [ ] <a id="act-038"></a> **ACT-038 [G]** Describe an informational image according to its purpose in the surrounding content.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content), [W3C images tutorial](https://www.w3.org/WAI/tutorials/images/). Possible checks: manual.
- [ ] <a id="act-039"></a> **ACT-039 [G]** Provide chart data in an accessible table or text summary when that gives an equivalent alternative.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content), [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships), [W3C images tutorial](https://www.w3.org/WAI/tutorials/images/). Possible checks: manual, assistive-technology.
- [ ] <a id="act-040"></a> **ACT-040 [R]** Provide the required text alternative for other non-text content, accounting for the criterion exceptions.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content). Possible checks: manual, assistive-technology.
- [ ] <a id="act-041"></a> **ACT-041 [G]** Give an image-only link an accessible name that identifies the link purpose.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content), [2.4.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#link-purpose-in-context), [W3C images tutorial](https://www.w3.org/WAI/tutorials/images/). Possible checks: manual, assistive-technology.

## Color, contrast, layout, and display adaptation

- [ ] <a id="act-042"></a> **ACT-042 [R]** Check normal-size text and images of normal-size text for at least 4.5:1 contrast, subject to exceptions.<br>
  Sources: [1.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#contrast-minimum). Possible checks: visual, automated.
- [ ] <a id="act-043"></a> **ACT-043 [R]** Check large text and images of large text for at least 3:1 contrast, subject to the criterion exceptions.<br>
  Sources: [1.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#contrast-minimum). Possible checks: visual, automated.
- [ ] <a id="act-044"></a> **ACT-044 [R]** Ensure visual information needed to identify controls and states has 3:1 contrast against adjacent colors. Apply the criterion exceptions.<br>
  Sources: [1.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-contrast). Possible checks: visual, manual.
- [ ] <a id="act-045"></a> **ACT-045 [R]** Check visual parts of graphics required for understanding for at least 3:1 contrast, subject to exceptions.<br>
  Sources: [1.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-contrast). Possible checks: visual, manual.
- [ ] <a id="act-046"></a> **ACT-046 [R]** Allow text to resize to 200% without assistive technology. Prevent content or function loss, subject to exceptions.<br>
  Sources: [1.4.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#resize-text). Possible checks: visual, manual.
- [ ] <a id="act-047"></a> **ACT-047 [R]** For vertically scrolling content, avoid two-dimensional scrolling at 320 CSS pixels wide. Prevent loss of content or function, subject to exceptions.<br>
  Sources: [1.4.10](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#reflow). Possible checks: visual, manual.
- [ ] <a id="act-048"></a> **ACT-048 [R]** For horizontally scrolling content, avoid two-dimensional scrolling at 256 CSS pixels high. Prevent loss of content or function, subject to exceptions.<br>
  Sources: [1.4.10](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#reflow). Possible checks: visual, manual.
- [ ] <a id="act-049"></a> **ACT-049 [R]** Preserve content and functionality when users apply the text-spacing overrides in the criterion.<br>
  Sources: [1.4.12](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#text-spacing). Possible checks: visual, manual.
- [ ] <a id="act-050"></a> **ACT-050 [R]** Support portrait and landscape orientation unless a particular orientation is essential.<br>
  Sources: [1.3.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#orientation). Possible checks: visual, manual.
- [ ] <a id="act-051"></a> **ACT-051 [R]** When required, let users dismiss hover or focus content without moving pointer hover or keyboard focus.<br>
  Sources: [1.4.13](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#content-on-hover-or-focus). Possible checks: keyboard, visual.
- [ ] <a id="act-052"></a> **ACT-052 [R]** Let users move the pointer over applicable hover-triggered content without it disappearing.<br>
  Sources: [1.4.13](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#content-on-hover-or-focus). Possible checks: manual, visual.
- [ ] <a id="act-053"></a> **ACT-053 [R]** Keep applicable hover- or focus-triggered content visible until a criterion-defined dismissal condition occurs.<br>
  Sources: [1.4.13](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#content-on-hover-or-focus). Possible checks: manual, keyboard.
- [ ] <a id="act-054"></a> **ACT-054 [G]** Test text over images and gradients at the least-contrasting visible area.<br>
  Sources: [1.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#contrast-minimum), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: visual, manual.
- [ ] <a id="act-055"></a> **ACT-055 [G]** Use an additional shape, text, or icon to distinguish states that also use color.<br>
  Sources: [1.4.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#use-of-color), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: visual, manual.
- [ ] <a id="act-056"></a> **ACT-056 [G]** Respect the user's reduced-motion preference where motion can be reduced.<br>
  Sources: [2.3.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#animation-from-interactions), [W3C reduced-motion technique](https://www.w3.org/WAI/WCAG22/Techniques/css/C39). Possible checks: visual, manual.
- [ ] <a id="act-057"></a> **ACT-057 [G]** Test the interface with browser zoom and increased text spacing.<br>
  Sources: [1.4.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#resize-text), [1.4.10](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#reflow), [1.4.12](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#text-spacing), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: visual, manual.
- [ ] <a id="act-058"></a> **ACT-058 [G]** Check focus indicators and controls in forced-colors or high-contrast display modes.<br>
  Sources: [2.4.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-visible), [1.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-contrast), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: visual, keyboard.
- [ ] <a id="act-059"></a> **ACT-059 [G]** Check contrast in each available theme and relevant interactive state.<br>
  Sources: [1.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#contrast-minimum), [1.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-contrast), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: visual, manual.

## Keyboard, focus, and pointer input

- [ ] <a id="act-060"></a> **ACT-060 [R]** Make functionality operable through a keyboard interface, subject to the path-dependent exception.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard). Possible checks: keyboard.
- [ ] <a id="act-061"></a> **ACT-061 [R]** Do not require specific timings for individual keystrokes, subject to the keyboard criterion exception.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard). Possible checks: keyboard.
- [ ] <a id="act-062"></a> **ACT-062 [R]** Allow keyboard focus to leave any component reached by keyboard using only a keyboard interface.<br>
  Sources: [2.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#no-keyboard-trap). Possible checks: keyboard.
- [ ] <a id="act-063"></a> **ACT-063 [R]** Tell users the exit method when unmodified arrow, Tab, or another standard exit method is insufficient.<br>
  Sources: [2.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#no-keyboard-trap). Possible checks: keyboard, manual.
- [ ] <a id="act-064"></a> **ACT-064 [R]** Preserve meaning and operability in focus order when sequence affects them.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order). Possible checks: keyboard, manual.
- [ ] <a id="act-065"></a> **ACT-065 [R]** Provide a mode where the keyboard focus indicator is visible on keyboard-operable user interfaces.<br>
  Sources: [2.4.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-visible). Possible checks: keyboard, visual.
- [ ] <a id="act-066"></a> **ACT-066 [R]** When a component receives keyboard focus, do not let author-created content entirely obscure it. Apply the criterion notes.<br>
  Sources: [2.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-not-obscured-minimum). Possible checks: keyboard, visual.
- [ ] <a id="act-067"></a> **ACT-067 [R]** Allow character-only shortcuts to be disabled, remapped to include a non-printable key, or active only on focus.<br>
  Sources: [2.1.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#character-key-shortcuts). Possible checks: keyboard, manual.
- [ ] <a id="act-068"></a> **ACT-068 [R]** For multipoint or path-based gestures, provide a single-pointer alternative without a path-based gesture, subject to exceptions.<br>
  Sources: [2.5.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pointer-gestures). Possible checks: manual.
- [ ] <a id="act-069"></a> **ACT-069 [R]** Provide a single-pointer alternative to dragging when the dragging criterion applies.<br>
  Sources: [2.5.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#dragging-movements). Possible checks: manual.
- [ ] <a id="act-070"></a> **ACT-070 [R]** For single-pointer functions, meet one allowed condition. Options include no execution on down-event, up-event with abort or undo, up reversal, or an essential down-event.<br>
  Sources: [2.5.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pointer-cancellation). Possible checks: manual.
- [ ] <a id="act-071"></a> **ACT-071 [R]** Provide an interface alternative to motion actuation when the criterion applies.<br>
  Sources: [2.5.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#motion-actuation). Possible checks: manual.
- [ ] <a id="act-072"></a> **ACT-072 [R]** Allow applicable motion actuation to be disabled, subject to the criterion exceptions.<br>
  Sources: [2.5.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#motion-actuation). Possible checks: manual.
- [ ] <a id="act-073"></a> **ACT-073 [R]** Make pointer targets at least 24 by 24 CSS pixels or satisfy an allowed exception.<br>
  Sources: [2.5.8](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#target-size-minimum). Possible checks: manual, visual.
- [ ] <a id="act-074"></a> **ACT-074 [R]** Do not trigger a change of context merely when a component receives focus.<br>
  Sources: [3.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#on-focus). Possible checks: keyboard, manual.
- [ ] <a id="act-075"></a> **ACT-075 [R]** Do not automatically change context when a component's setting changes unless users receive advance notice.<br>
  Sources: [3.2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#on-input). Possible checks: keyboard, manual.
- [ ] <a id="act-076"></a> **ACT-076 [G]** Use native links for navigation and native buttons for actions where appropriate.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-077"></a> **ACT-077 [G]** Check keyboard operation independently from the non-dragging pointer alternative.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [2.5.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#dragging-movements), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: keyboard, manual.
- [ ] <a id="act-078"></a> **ACT-078 [G]** Check focused elements around sticky headers, overlays, and mobile virtual keyboards.<br>
  Sources: [2.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-not-obscured-minimum), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: keyboard, visual.
- [ ] <a id="act-079"></a> **ACT-079 [G]** Provide an accessible, visible close control for dismissible overlays.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-080"></a> **ACT-080 [G]** Check that tab order reaches visible controls without reaching hidden controls unexpectedly.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: keyboard.
- [ ] <a id="act-081"></a> **ACT-081 [G]** Make keyboard focus visually distinguishable on all interactive controls.<br>
  Sources: [2.4.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-visible), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: keyboard, visual.

## Forms, errors, authentication, and transactions

- [ ] <a id="act-082"></a> **ACT-082 [R]** Provide labels or instructions when a user must enter data.<br>
  Sources: [3.3.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#labels-or-instructions). Possible checks: manual, assistive-technology.
- [ ] <a id="act-083"></a> **ACT-083 [R]** Expose the relationship between a label and its input programmatically or in text.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships). Possible checks: manual, assistive-technology.
- [ ] <a id="act-084"></a> **ACT-084 [R]** Identify applicable input purposes programmatically for fields collecting information about the user.<br>
  Sources: [1.3.5](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#identify-input-purpose). Possible checks: manual, automated.
- [ ] <a id="act-085"></a> **ACT-085 [R]** Identify the input item with an automatically detected error and describe the error in text.<br>
  Sources: [3.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-identification). Possible checks: manual, keyboard.
- [ ] <a id="act-086"></a> **ACT-086 [R]** Suggest known corrections for detected input errors unless security or purpose would be compromised.<br>
  Sources: [3.3.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-suggestion). Possible checks: manual.
- [ ] <a id="act-087"></a> **ACT-087 [R]** For covered legal or financial actions, data changes, or test responses, offer reversal, error correction, or confirmation as allowed.<br>
  Sources: [3.3.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-prevention-legal-financial-data). Possible checks: manual.
- [ ] <a id="act-088"></a> **ACT-088 [R]** Within one process, auto-populate or let users select information needed again. Include information entered by or provided to the user and apply exceptions.<br>
  Sources: [3.3.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#redundant-entry). Possible checks: manual.
- [ ] <a id="act-089"></a> **ACT-089 [R]** Provide an allowed alternative or assistance mechanism for authentication cognitive tests, subject to exceptions.<br>
  Sources: [3.3.8](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#accessible-authentication-minimum). Possible checks: manual.
- [ ] <a id="act-090"></a> **ACT-090 [R]** Make form-control names and roles programmatically determinable.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value). Possible checks: assistive-technology, automated.
- [ ] <a id="act-091"></a> **ACT-091 [R]** Expose applicable form status messages so assistive technology can present them without focus.<br>
  Sources: [4.1.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages). Possible checks: assistive-technology, manual.
- [ ] <a id="act-092"></a> **ACT-092 [G]** Keep visible labels available after users start typing.<br>
  Sources: [3.3.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#labels-or-instructions), [W3C forms tutorial](https://www.w3.org/WAI/tutorials/forms/). Possible checks: manual.
- [ ] <a id="act-093"></a> **ACT-093 [G]** Indicate required fields and input format before users submit the form.<br>
  Sources: [3.3.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#labels-or-instructions), [W3C forms tutorial](https://www.w3.org/WAI/tutorials/forms/). Possible checks: manual.
- [ ] <a id="act-094"></a> **ACT-094 [G]** Associate field-specific error text with the affected input.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships), [3.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-identification), [W3C forms tutorial](https://www.w3.org/WAI/tutorials/forms/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-095"></a> **ACT-095 [G]** Provide an error summary linked to affected fields when a long form has several errors.<br>
  Sources: [3.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-identification), [3.3.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-suggestion), [W3C forms tutorial](https://www.w3.org/WAI/tutorials/forms/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-096"></a> **ACT-096 [G]** Allow password managers and pasting for authentication where feasible.<br>
  Sources: [3.3.8](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#accessible-authentication-minimum), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: manual.
- [ ] <a id="act-097"></a> **ACT-097 [G]** Avoid clearing correctly entered form data after a failed submission.<br>
  Sources: [3.3.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-suggestion), [W3C forms tutorial](https://www.w3.org/WAI/tutorials/forms/). Possible checks: manual.
- [ ] <a id="act-098"></a> **ACT-098 [G]** Make review and correction available before a significant transaction is submitted.<br>
  Sources: [3.3.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-prevention-legal-financial-data), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: keyboard, manual.
- [ ] <a id="act-099"></a> **ACT-099 [G]** Expose expanded or selected states when multi-step navigation uses interactive controls.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-100"></a> **ACT-100 [G]** Use appropriate autocomplete tokens for applicable personal-information fields.<br>
  Sources: [1.3.5](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#identify-input-purpose), [W3C forms tutorial](https://www.w3.org/WAI/tutorials/forms/). Possible checks: manual, automated.
- [ ] <a id="act-101"></a> **ACT-101 [G]** Check form validation and correction with both keyboard and assistive technology.<br>
  Sources: [3.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-identification), [3.3.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-suggestion), [W3C forms tutorial](https://www.w3.org/WAI/tutorials/forms/). Possible checks: keyboard, assistive-technology.

## Cognitive accessibility and clear content

- [ ] <a id="act-102"></a> **ACT-102 [G]** Use clear, familiar words and explain unfamiliar terms when needed.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.
- [ ] <a id="act-103"></a> **ACT-103 [G]** Make the purpose of each page and its important actions easy to identify.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.
- [ ] <a id="act-104"></a> **ACT-104 [G]** Break complex instructions into clear steps.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.
- [ ] <a id="act-105"></a> **ACT-105 [G]** Reduce the need to remember information across multiple steps where feasible.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.
- [ ] <a id="act-106"></a> **ACT-106 [G]** Allow users to go back and correct mistakes without losing their work where feasible.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.
- [ ] <a id="act-107"></a> **ACT-107 [G]** Make help or feedback options easy to find when they are provided.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.
- [ ] <a id="act-108"></a> **ACT-108 [G]** Tell users about relevant costs and required information before they begin a process.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.
- [ ] <a id="act-109"></a> **ACT-109 [G]** Avoid making controls or content move unexpectedly.<br>
  Sources: [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual, visual.

## Dynamic content and assistive-technology semantics

- [ ] <a id="act-110"></a> **ACT-110 [R]** Expose each user-interface component's name and role programmatically.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value). Possible checks: assistive-technology, automated.
- [ ] <a id="act-111"></a> **ACT-111 [R]** Make user-settable component states, properties, and values programmatically settable.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value). Possible checks: assistive-technology, manual.
- [ ] <a id="act-112"></a> **ACT-112 [R]** Make notifications of name, role, state, property, and value changes available to user agents and assistive technologies.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value). Possible checks: assistive-technology, manual.
- [ ] <a id="act-113"></a> **ACT-113 [R]** Expose applicable status messages so assistive technology can present them without focus.<br>
  Sources: [4.1.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages). Possible checks: assistive-technology, manual.
- [ ] <a id="act-114"></a> **ACT-114 [R]** Preserve meaningful information and relationships conveyed through presentation in code or text.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships). Possible checks: assistive-technology, manual.
- [ ] <a id="act-115"></a> **ACT-115 [G]** Prefer native HTML semantics where they already provide the correct accessible behavior.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: assistive-technology, keyboard.
- [ ] <a id="act-116"></a> **ACT-116 [G]** Use live regions or suitable native status semantics for applicable asynchronous status messages.<br>
  Sources: [4.1.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-117"></a> **ACT-117 [G]** Check that live messages announce once, at an appropriate priority, with useful content.<br>
  Sources: [4.1.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-118"></a> **ACT-118 [G]** Update accessible expanded, selected, checked, and pressed states when their controls change.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: assistive-technology, keyboard.
- [ ] <a id="act-119"></a> **ACT-119 [G]** Avoid adding ARIA roles or attributes that conflict with native semantics.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-120"></a> **ACT-120 [G]** Check that hidden or inactive content does not leave unexpected focusable controls available.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-121"></a> **ACT-121 [G]** Check that an accessible status is understandable without surrounding visual context.<br>
  Sources: [4.1.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: assistive-technology, manual.

## Dialogs and overlays, when present

- [ ] <a id="act-122"></a> **ACT-122 [G]** Give each dialog an accessible name that identifies its purpose.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-123"></a> **ACT-123 [G]** Move focus to an appropriate location inside a modal dialog when it opens.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-124"></a> **ACT-124 [G]** Keep background content inert while a true modal dialog is open.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard, manual.
- [ ] <a id="act-125"></a> **ACT-125 [G]** Keep Tab and Shift+Tab within an open modal dialog.<br>
  Sources: [2.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#no-keyboard-trap), [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard.
- [ ] <a id="act-126"></a> **ACT-126 [G]** Let users close a modal dialog with Escape when the pattern permits it.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [2.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#no-keyboard-trap), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard.
- [ ] <a id="act-127"></a> **ACT-127 [G]** Return focus to the invoking control after closing a dialog when it remains the logical destination.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-128"></a> **ACT-128 [G]** Choose a logical focus destination if the invoking control no longer exists.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard, manual.
- [ ] <a id="act-129"></a> **ACT-129 [G]** Check nested dialogs and overlays in each open and close sequence.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Possible checks: keyboard, manual.

## Menus, tabs, accordions, and carousels, when present

- [ ] <a id="act-130"></a> **ACT-130 [G]** Distinguish ordinary site navigation from an application-style menu before choosing roles.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C menu and menubar pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/). Possible checks: manual, assistive-technology.
- [ ] <a id="act-131"></a> **ACT-131 [G]** For application-style menus, implement the keyboard interactions for the chosen pattern.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [W3C menu and menubar pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/). Possible checks: keyboard.
- [ ] <a id="act-132"></a> **ACT-132 [G]** For tabs, expose the selected tab and its associated panel.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C tabs pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-133"></a> **ACT-133 [G]** For tabs, implement the keyboard navigation of the selected tabs pattern.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [W3C tabs pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). Possible checks: keyboard.
- [ ] <a id="act-134"></a> **ACT-134 [G]** For accordions, expose whether each controlled panel is expanded or collapsed.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C accordion pattern](https://www.w3.org/WAI/ARIA/apg/patterns/accordion/). Possible checks: assistive-technology, keyboard.
- [ ] <a id="act-135"></a> **ACT-135 [G]** For accordions, make each panel trigger keyboard operable.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [W3C accordion pattern](https://www.w3.org/WAI/ARIA/apg/patterns/accordion/). Possible checks: keyboard.
- [ ] <a id="act-136"></a> **ACT-136 [G]** For carousels, provide accessible controls to move between items.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C carousel pattern](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-137"></a> **ACT-137 [G]** For automatically rotating carousels, provide an applicable pause or stop mechanism.<br>
  Sources: [2.2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pause-stop-hide), [W3C carousel pattern](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/). Possible checks: keyboard, manual.
- [ ] <a id="act-138"></a> **ACT-138 [G]** Check that closed menus and inactive panels do not expose inappropriate focus targets.<br>
  Sources: [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Possible checks: keyboard.

## Comboboxes, listboxes, and sliders, when present

- [ ] <a id="act-139"></a> **ACT-139 [G]** Give a combobox an accessible name and expose its expanded or collapsed state.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-140"></a> **ACT-140 [G]** Connect a combobox to its popup using the semantics required by the selected pattern.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-141"></a> **ACT-141 [G]** Support the selected combobox pattern's keyboard interactions, including navigation and selection.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [W3C combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). Possible checks: keyboard.
- [ ] <a id="act-142"></a> **ACT-142 [G]** Keep the active option available to assistive technology when focus remains on the combobox.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). Possible checks: assistive-technology, keyboard.
- [ ] <a id="act-143"></a> **ACT-143 [G]** Preserve normal text-editing keys in an editable combobox.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [W3C combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). Possible checks: keyboard.
- [ ] <a id="act-144"></a> **ACT-144 [G]** Expose a custom slider's name, current value, and allowed range.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-145"></a> **ACT-145 [G]** Support the keyboard interactions of the selected slider pattern.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [W3C slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/). Possible checks: keyboard.
- [ ] <a id="act-146"></a> **ACT-146 [G]** Offer a non-dragging single-pointer way to change a slider when the criterion applies.<br>
  Sources: [2.5.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#dragging-movements), [W3C slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/). Possible checks: manual.
- [ ] <a id="act-147"></a> **ACT-147 [G]** Verify custom widgets with actual assistive technologies, including touch where relevant.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/). Possible checks: assistive-technology, manual.

## Tables, dashboards, and data displays, when present

- [ ] <a id="act-148"></a> **ACT-148 [R]** Make data-table headers and cell relationships programmatically determinable or available in text.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships). Possible checks: assistive-technology, manual.
- [ ] <a id="act-149"></a> **ACT-149 [R]** Ensure the information conveyed by a chart has an equivalent text alternative.<br>
  Sources: [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content). Possible checks: manual, assistive-technology.
- [ ] <a id="act-150"></a> **ACT-150 [R]** Do not use color alone to distinguish chart data or status.<br>
  Sources: [1.4.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#use-of-color). Possible checks: visual, manual.
- [ ] <a id="act-151"></a> **ACT-151 [G]** Use appropriate native table elements for tabular data.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships), [W3C tables tutorial](https://www.w3.org/WAI/tutorials/tables/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-152"></a> **ACT-152 [G]** Associate complex table cells with the correct headers.<br>
  Sources: [1.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships), [W3C tables tutorial](https://www.w3.org/WAI/tutorials/tables/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-153"></a> **ACT-153 [G]** Expose the current sort state on the relevant header when a table is sortable.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C sortable table example](https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/). Possible checks: assistive-technology, keyboard.
- [ ] <a id="act-154"></a> **ACT-154 [G]** Make sort and row-expansion controls keyboard operable and clearly named.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C tables tutorial](https://www.w3.org/WAI/tutorials/tables/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-155"></a> **ACT-155 [G]** Announce result counts or updated data when the update is an applicable status message.<br>
  Sources: [4.1.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages), [W3C WCAG techniques](https://www.w3.org/WAI/WCAG22/Techniques/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-156"></a> **ACT-156 [G]** Test scrollable data regions for usable focus and reading order at narrow widths.<br>
  Sources: [1.3.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#meaningful-sequence), [2.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order), [W3C tables tutorial](https://www.w3.org/WAI/tutorials/tables/). Possible checks: keyboard, visual.
- [ ] <a id="act-157"></a> **ACT-157 [G]** Test data updates, sorting, and filtering with assistive technology in each relevant state.<br>
  Sources: [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [4.1.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages), [W3C sortable table example](https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/). Possible checks: assistive-technology, keyboard.

## Audio, video, animation, and time limits, when present

- [ ] <a id="act-158"></a> **ACT-158 [R]** Provide an equivalent time-based media alternative for prerecorded audio-only content, subject to the criterion exception.<br>
  Sources: [1.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-only-and-video-only-prerecorded). Possible checks: manual.
- [ ] <a id="act-159"></a> **ACT-159 [R]** Provide an equivalent time-based media alternative or audio track for prerecorded video-only content, subject to the criterion exception.<br>
  Sources: [1.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-only-and-video-only-prerecorded). Possible checks: manual.
- [ ] <a id="act-160"></a> **ACT-160 [R]** Provide captions for prerecorded synchronized audio, subject to the stated exception.<br>
  Sources: [1.2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#captions-prerecorded). Possible checks: manual.
- [ ] <a id="act-161"></a> **ACT-161 [R]** Provide a time-based media alternative or audio description for prerecorded video in synchronized media, subject to the criterion exception.<br>
  Sources: [1.2.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-description-or-media-alternative-prerecorded). Possible checks: manual.
- [ ] <a id="act-162"></a> **ACT-162 [R]** Provide captions for live audio in synchronized media.<br>
  Sources: [1.2.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#captions-live). Possible checks: manual.
- [ ] <a id="act-163"></a> **ACT-163 [R]** Provide audio description for applicable prerecorded synchronized video.<br>
  Sources: [1.2.5](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-description-prerecorded). Possible checks: manual.
- [ ] <a id="act-164"></a> **ACT-164 [R]** For automatic audio over three seconds, provide pause, stop, or volume control independent of the system volume.<br>
  Sources: [1.4.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-control). Possible checks: keyboard, manual.
- [ ] <a id="act-165"></a> **ACT-165 [R]** Provide an allowed way to turn off, adjust, or extend time limits, subject to the criterion exceptions.<br>
  Sources: [2.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#timing-adjustable). Possible checks: manual, keyboard.
- [ ] <a id="act-166"></a> **ACT-166 [R]** Provide pause, stop, or hide controls for applicable automatic moving, blinking, or scrolling content.<br>
  Sources: [2.2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pause-stop-hide). Possible checks: keyboard, manual.
- [ ] <a id="act-167"></a> **ACT-167 [R]** Provide a way to pause, stop, hide, or control the frequency of applicable auto-updating information.<br>
  Sources: [2.2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pause-stop-hide). Possible checks: keyboard, manual.
- [ ] <a id="act-168"></a> **ACT-168 [R]** Avoid more than three flashes in one second, unless flashes remain below the general and red flash thresholds.<br>
  Sources: [2.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#three-flashes-or-below-threshold). Possible checks: visual, manual.
- [ ] <a id="act-169"></a> **ACT-169 [G]** Provide keyboard-operable and named controls for any custom media player.<br>
  Sources: [2.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard), [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value), [W3C accessible audio and video guide](https://www.w3.org/WAI/media/av/). Possible checks: keyboard, assistive-technology.
- [ ] <a id="act-170"></a> **ACT-170 [G]** Review captions for accuracy, speaker information, and synchronization.<br>
  Sources: [1.2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#captions-prerecorded), [1.2.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#captions-live), [W3C accessible audio and video guide](https://www.w3.org/WAI/media/av/). Possible checks: manual.
- [ ] <a id="act-171"></a> **ACT-171 [G]** Use a transcript as an additional way to access audio or video content where feasible.<br>
  Sources: [1.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-only-and-video-only-prerecorded), [1.2.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-description-or-media-alternative-prerecorded), [W3C accessible audio and video guide](https://www.w3.org/WAI/media/av/). Possible checks: manual.
- [ ] <a id="act-172"></a> **ACT-172 [G]** Warn users before a timeout and preserve their entered data where feasible.<br>
  Sources: [2.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#timing-adjustable), [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/). Possible checks: manual.

## Verification and evidence

- [ ] <a id="act-173"></a> **ACT-173 [P]** Run automated accessibility checks across the selected pages and interactive states.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: automated.
- [ ] <a id="act-174"></a> **ACT-174 [P]** Review automated findings, incomplete results, and tool errors individually.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: automated, manual.
- [ ] <a id="act-175"></a> **ACT-175 [P]** Traverse the full flow with a keyboard and inspect visible focus.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: keyboard, visual.
- [ ] <a id="act-176"></a> **ACT-176 [P]** Review semantics and announcements with suitable assistive technologies.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: assistive-technology, manual.
- [ ] <a id="act-177"></a> **ACT-177 [P]** Inspect text alternatives, instructions, captions, and error messages for meaning.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-178"></a> **ACT-178 [P]** Exercise relevant pointer, touch, motion, zoom, and display conditions.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual, visual.
- [ ] <a id="act-179"></a> **ACT-179 [P]** Save reproducible steps, the affected page state, expected behavior, and observed behavior.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-180"></a> **ACT-180 [P]** Link each issue to evidence and the applicable criterion or guidance.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-181"></a> **ACT-181 [P]** Record pass, fail, not applicable, unassessable, or not tested with reasons.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-182"></a> **ACT-182 [P]** Report missing required features separately from accessibility results.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-183"></a> **ACT-183 [P]** Record tool versions and rules, reviewer experience, and test limitations.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-184"></a> **ACT-184 [P]** Do not present a clean automated scan as proof of WCAG conformance.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-185"></a> **ACT-185 [P]** Keep the evaluation checklist and scoring instructions out of the unchanged baseline input.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-186"></a> **ACT-186 [P]** Record whether each reviewed issue comes from the generated site or an external dependency.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-187"></a> **ACT-187 [P]** Keep reviewer evidence and final decisions separate from assumptions made before testing.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.
- [ ] <a id="act-188"></a> **ACT-188 [P]** Keep study guidance out of the baseline runtime, including automatically loaded workspace instructions.<br>
  Sources: [W3C evaluation overview](https://www.w3.org/WAI/test-evaluate/). Possible checks: manual.

## Applying the list to the five selected tasks

These are possible review areas based on the selected task descriptions. Determine applicability from the actual task and generated artifact; do not assume the features were generated or function correctly. See [working decisions](../study-working-decisions.md).

| Selected task | Areas to inspect if present or requested |
| --- | --- |
| 7: Services | Page structure, tabs, FAQ disclosures, and any order-related controls. |
| 8: Consulting | Structure, text contrast, animation, navigation, and relevant interactive states. The original task explicitly mentions accessible contrast and semantic HTML. |
| 18: Cinema | Listing navigation, ticket selection, forms, error states, and any confirmation process. |
| 19: Dashboard | Keyboard access, the single-pointer alternative to dragging, chart alternatives, and data updates. |
| 1: Portfolio | Navigation, project links, images, headings, responsive layout, and any additional controls. |


## Coverage and limits

The generator checks that each of the 55 WCAG 2.2 A/AA criteria has at least one R item. This checks references and coverage only. It does not validate the paraphrases, prove that every condition is represented, or turn these actions into a complete audit procedure.

An action that represents a possible technique is labelled G even when the underlying outcome is required. These suggestions do not imply that every site needs every listed widget. AAA criteria, legal context, empirical AI evidence, and source limitations remain in the related accessibility research files. Guidance pages may change; record their versions or retrieval dates when the study protocol is frozen.

For study results, the unit of analysis, applicable denominator, state sampling, issue deduplication, reviewer calibration, and scoring need to be set in a separate protocol before runs begin.

## WCAG 2.2 A/AA crosswalk

Each link below points to at least one WCAG-derived action that refers to the criterion. The mapping is not a complete set of test cases or a claim of correct interpretation.

- [1.1.1 Non-text Content (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content): [ACT-027](#act-027), [ACT-028](#act-028), [ACT-029](#act-029), [ACT-030](#act-030), [ACT-031](#act-031), [ACT-040](#act-040), [ACT-149](#act-149).
- [1.2.1 Audio-only and Video-only (Prerecorded) (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-only-and-video-only-prerecorded): [ACT-158](#act-158), [ACT-159](#act-159).
- [1.2.2 Captions (Prerecorded) (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#captions-prerecorded): [ACT-160](#act-160).
- [1.2.3 Audio Description or Media Alternative (Prerecorded) (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-description-or-media-alternative-prerecorded): [ACT-161](#act-161).
- [1.2.4 Captions (Live) (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#captions-live): [ACT-162](#act-162).
- [1.2.5 Audio Description (Prerecorded) (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-description-prerecorded): [ACT-163](#act-163).
- [1.3.1 Info and Relationships (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#info-and-relationships): [ACT-014](#act-014), [ACT-017](#act-017), [ACT-018](#act-018), [ACT-083](#act-083), [ACT-114](#act-114), [ACT-148](#act-148).
- [1.3.2 Meaningful Sequence (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#meaningful-sequence): [ACT-016](#act-016).
- [1.3.3 Sensory Characteristics (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#sensory-characteristics): [ACT-033](#act-033).
- [1.3.4 Orientation (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#orientation): [ACT-050](#act-050).
- [1.3.5 Identify Input Purpose (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#identify-input-purpose): [ACT-084](#act-084).
- [1.4.1 Use of Color (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#use-of-color): [ACT-034](#act-034), [ACT-150](#act-150).
- [1.4.2 Audio Control (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-control): [ACT-164](#act-164).
- [1.4.3 Contrast (Minimum) (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#contrast-minimum): [ACT-042](#act-042), [ACT-043](#act-043).
- [1.4.4 Resize Text (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#resize-text): [ACT-046](#act-046).
- [1.4.5 Images of Text (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#images-of-text): [ACT-035](#act-035).
- [1.4.10 Reflow (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#reflow): [ACT-047](#act-047), [ACT-048](#act-048).
- [1.4.11 Non-text Contrast (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-contrast): [ACT-044](#act-044), [ACT-045](#act-045).
- [1.4.12 Text Spacing (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#text-spacing): [ACT-049](#act-049).
- [1.4.13 Content on Hover or Focus (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#content-on-hover-or-focus): [ACT-051](#act-051), [ACT-052](#act-052), [ACT-053](#act-053).
- [2.1.1 Keyboard (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#keyboard): [ACT-060](#act-060), [ACT-061](#act-061).
- [2.1.2 No Keyboard Trap (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#no-keyboard-trap): [ACT-062](#act-062), [ACT-063](#act-063).
- [2.1.4 Character Key Shortcuts (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#character-key-shortcuts): [ACT-067](#act-067).
- [2.2.1 Timing Adjustable (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#timing-adjustable): [ACT-165](#act-165).
- [2.2.2 Pause, Stop, Hide (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pause-stop-hide): [ACT-166](#act-166), [ACT-167](#act-167).
- [2.3.1 Three Flashes or Below Threshold (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#three-flashes-or-below-threshold): [ACT-168](#act-168).
- [2.4.1 Bypass Blocks (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#bypass-blocks): [ACT-019](#act-019).
- [2.4.2 Page Titled (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#page-titled): [ACT-011](#act-011).
- [2.4.3 Focus Order (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-order): [ACT-064](#act-064).
- [2.4.4 Link Purpose (In Context) (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#link-purpose-in-context): [ACT-032](#act-032).
- [2.4.5 Multiple Ways (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#multiple-ways): [ACT-020](#act-020).
- [2.4.6 Headings and Labels (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#headings-and-labels): [ACT-015](#act-015).
- [2.4.7 Focus Visible (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-visible): [ACT-065](#act-065).
- [2.4.11 Focus Not Obscured (Minimum) (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-not-obscured-minimum): [ACT-066](#act-066).
- [2.5.1 Pointer Gestures (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pointer-gestures): [ACT-068](#act-068).
- [2.5.2 Pointer Cancellation (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pointer-cancellation): [ACT-070](#act-070).
- [2.5.3 Label in Name (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#label-in-name): [ACT-036](#act-036).
- [2.5.4 Motion Actuation (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#motion-actuation): [ACT-071](#act-071), [ACT-072](#act-072).
- [2.5.7 Dragging Movements (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#dragging-movements): [ACT-069](#act-069).
- [2.5.8 Target Size (Minimum) (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#target-size-minimum): [ACT-073](#act-073).
- [3.1.1 Language of Page (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#language-of-page): [ACT-012](#act-012).
- [3.1.2 Language of Parts (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#language-of-parts): [ACT-013](#act-013).
- [3.2.1 On Focus (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#on-focus): [ACT-074](#act-074).
- [3.2.2 On Input (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#on-input): [ACT-075](#act-075).
- [3.2.3 Consistent Navigation (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#consistent-navigation): [ACT-021](#act-021).
- [3.2.4 Consistent Identification (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#consistent-identification): [ACT-022](#act-022).
- [3.2.6 Consistent Help (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#consistent-help): [ACT-023](#act-023).
- [3.3.1 Error Identification (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-identification): [ACT-085](#act-085).
- [3.3.2 Labels or Instructions (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#labels-or-instructions): [ACT-082](#act-082).
- [3.3.3 Error Suggestion (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-suggestion): [ACT-086](#act-086).
- [3.3.4 Error Prevention (Legal, Financial, Data) (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-prevention-legal-financial-data): [ACT-087](#act-087).
- [3.3.7 Redundant Entry (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#redundant-entry): [ACT-088](#act-088).
- [3.3.8 Accessible Authentication (Minimum) (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#accessible-authentication-minimum): [ACT-089](#act-089).
- [4.1.2 Name, Role, Value (A)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value): [ACT-028](#act-028), [ACT-090](#act-090), [ACT-110](#act-110), [ACT-111](#act-111), [ACT-112](#act-112).
- [4.1.3 Status Messages (AA)](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages): [ACT-091](#act-091), [ACT-113](#act-113).
