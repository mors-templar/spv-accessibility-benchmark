# Master accessibility checklist for web projects

**Version:** 0.1, 2026-10-29. **Status:** research draft for review, not a validated audit or a conformance claim. The suggested study target is WCAG 2.2 Level AA: all 31 Level A and 24 Level AA criteria, subject to their applicability and exceptions. The 31 Level AAA criteria are included separately as an extended reference.

The criterion identifiers and names below are from the [W3C WCAG 2.2 Recommendation](https://www.w3.org/TR/2024/REC-WCAG22-20241212/). The check descriptions are our brief, non-normative summaries. Use the linked W3C criterion, definitions, exceptions, and conformance rules when making a determination. The [W3C Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) and [Understanding documents](https://www.w3.org/WAI/WCAG22/Understanding/) provide further guidance.

The checklist covers all 55 A and AA criteria as an index. A checkbox is not a complete test procedure. Some criteria require several checks, expert interpretation, or assistive technology. A criterion is not applicable when the relevant content or feature genuinely does not exist. If a task requires a feature that was not generated, record the functional failure and any dependent accessibility checks as unassessable.

## Before evaluating a site

1. Define the site, pages, page states, processes, browsers, assistive technologies, viewport sizes, and any excluded scope.
2. Identify required features from the original task. Record missing or nonfunctional features separately.
3. Record each criterion as pass, fail, not applicable, or unassessable, with rationale and evidence. Distinguish not tested from pass. Record who reviewed it and the tools and versions used.
4. Use automated scans, keyboard and browser tests, and manual review. Automated tools detect only a subset of barriers. Inspect incomplete results. Do not claim WCAG conformance from a clean scan.
5. Test full pages and relevant variations and complete processes. WCAG also has conformance requirements for accessible ways of using technologies and non-interference. A sample does not establish conformance for an entire site.
6. Where possible, involve people with disabilities and reviewers familiar with assistive technology. Record actual participation; do not assume it occurred.

W3C's [WCAG Evaluation Methodology 2.0](https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/) is a 2026 Group Note that describes a structured evaluation process. It does not replace WCAG or turn a sample into a whole-site conformance claim.

## Level A and AA criteria

### 1. Perceivable

- [ ] **1.1.1 Non-text Content (A):** Give informative images and other non-text content an equivalent text alternative. Handle controls, CAPTCHA, decorative content, and other exceptions according to the criterion. [W3C](https://www.w3.org/TR/WCAG22/#non-text-content)
- [ ] **1.2.1 Audio-only and Video-only (Prerecorded) (A):** Provide an appropriate equivalent alternative for prerecorded audio-only or video-only content, subject to the media-alternative exception. [W3C](https://www.w3.org/TR/WCAG22/#audio-only-and-video-only-prerecorded)
- [ ] **1.2.2 Captions (Prerecorded) (A):** Provide captions for prerecorded audio in synchronized media, subject to the stated exception. Review accuracy and synchronization. [W3C](https://www.w3.org/TR/WCAG22/#captions-prerecorded)
- [ ] **1.2.3 Audio Description or Media Alternative (Prerecorded) (A):** Provide an appropriate media alternative or audio description for relevant prerecorded synchronized media. [W3C](https://www.w3.org/TR/WCAG22/#audio-description-or-media-alternative-prerecorded)
- [ ] **1.2.4 Captions (Live) (AA):** Provide captions for live audio in synchronized media. [W3C](https://www.w3.org/TR/WCAG22/#captions-live)
- [ ] **1.2.5 Audio Description (Prerecorded) (AA):** Provide audio description for prerecorded video in synchronized media. Review W3C's guidance when the existing audio already conveys the visual information. [W3C](https://www.w3.org/TR/WCAG22/#audio-description-prerecorded)
- [ ] **1.3.1 Info and Relationships (A):** Make visually conveyed structure and relationships available programmatically or in text. Review headings, lists, forms, tables, and groups when present. [W3C](https://www.w3.org/TR/WCAG22/#info-and-relationships)
- [ ] **1.3.2 Meaningful Sequence (A):** Ensure the programmatically determined reading order preserves meaning when sequence matters. [W3C](https://www.w3.org/TR/WCAG22/#meaningful-sequence)
- [ ] **1.3.3 Sensory Characteristics (A):** Do not rely solely on shape, color, size, visual location, orientation, or sound to explain how to use content. [W3C](https://www.w3.org/TR/WCAG22/#sensory-characteristics)
- [ ] **1.3.4 Orientation (AA):** Support both display orientations unless a specific orientation is essential. [W3C](https://www.w3.org/TR/WCAG22/#orientation)
- [ ] **1.3.5 Identify Input Purpose (AA):** Programmatically identify the purpose of applicable fields collecting information about the user, using the relevant input-purpose taxonomy. [W3C](https://www.w3.org/TR/WCAG22/#identify-input-purpose)
- [ ] **1.4.1 Use of Color (A):** Do not use color as the only visual means of conveying information, an action, or a distinction. [W3C](https://www.w3.org/TR/WCAG22/#use-of-color)
- [ ] **1.4.2 Audio Control (A):** If audio plays automatically for more than three seconds, provide the required pause, stop, or independent volume mechanism. [W3C](https://www.w3.org/TR/WCAG22/#audio-control)
- [ ] **1.4.3 Contrast (Minimum) (AA):** Measure text contrast. The usual minimum is 4.5:1 for normal text and 3:1 for large text; apply the defined exceptions. [W3C](https://www.w3.org/TR/WCAG22/#contrast-minimum)
- [ ] **1.4.4 Resize Text (AA):** Verify text can be resized to 200% without assistive technology and without loss of content or functionality, subject to the specified exceptions. [W3C](https://www.w3.org/TR/WCAG22/#resize-text)
- [ ] **1.4.5 Images of Text (AA):** Use actual text rather than images of text when the technology can provide the visual presentation, unless an exception applies. [W3C](https://www.w3.org/TR/WCAG22/#images-of-text)
- [ ] **1.4.10 Reflow (AA):** Check reflow at a width equivalent to 320 CSS pixels for vertically scrolling content, or 256 CSS pixels high for horizontally scrolling content, without loss of content or functionality. Respect exceptions for content requiring two-dimensional layout. [W3C](https://www.w3.org/TR/WCAG22/#reflow)
- [ ] **1.4.11 Non-text Contrast (AA):** Check at least 3:1 contrast for applicable visual information needed to identify user-interface components, states, and meaningful graphics, subject to exceptions. [W3C](https://www.w3.org/TR/WCAG22/#non-text-contrast)
- [ ] **1.4.12 Text Spacing (AA):** Apply user overrides for line height, paragraph spacing, letter spacing, and word spacing at the levels in the criterion. Check that no content or functionality is lost. [W3C](https://www.w3.org/TR/WCAG22/#text-spacing)
- [ ] **1.4.13 Content on Hover or Focus (AA):** Check that applicable extra content is dismissible, hoverable, and persistent, with the criterion's exceptions. [W3C](https://www.w3.org/TR/WCAG22/#content-on-hover-or-focus)

### 2. Operable

- [ ] **2.1.1 Keyboard (A):** Make functionality operable through a keyboard interface, except where the underlying function requires a path-dependent input. [W3C](https://www.w3.org/TR/WCAG22/#keyboard)
- [ ] **2.1.2 No Keyboard Trap (A):** Ensure users can move keyboard focus away from components. Provide instructions if a nonstandard exit method is needed. [W3C](https://www.w3.org/TR/WCAG22/#no-keyboard-trap)
- [ ] **2.1.4 Character Key Shortcuts (A):** For applicable character-only shortcuts, allow them to be disabled, remapped with a modifier, or active only when the component has focus. [W3C](https://www.w3.org/TR/WCAG22/#character-key-shortcuts)
- [ ] **2.2.1 Timing Adjustable (A):** Provide the specified ways to turn off, adjust, or extend applicable time limits, unless an exception applies. [W3C](https://www.w3.org/TR/WCAG22/#timing-adjustable)
- [ ] **2.2.2 Pause, Stop, Hide (A):** Provide controls for applicable automatically moving, blinking, scrolling, or updating content. The triggering conditions differ for moving and updating content. [W3C](https://www.w3.org/TR/WCAG22/#pause-stop-hide)
- [ ] **2.3.1 Three Flashes or Below Threshold (A):** Check flashing content against the frequency and size thresholds. [W3C](https://www.w3.org/TR/WCAG22/#three-flashes-or-below-threshold)
- [ ] **2.4.1 Bypass Blocks (A):** Provide a way to bypass blocks repeated on multiple pages. A skip link is one possible technique. [W3C](https://www.w3.org/TR/WCAG22/#bypass-blocks)
- [ ] **2.4.2 Page Titled (A):** Give each page a title that describes its topic or purpose. [W3C](https://www.w3.org/TR/WCAG22/#page-titled)
- [ ] **2.4.3 Focus Order (A):** Ensure focus order preserves meaning and operability when sequence affects them. [W3C](https://www.w3.org/TR/WCAG22/#focus-order)
- [ ] **2.4.4 Link Purpose (In Context) (A):** Make link purpose understandable from its text or its programmatically determined context, except for the stated ambiguity exception. [W3C](https://www.w3.org/TR/WCAG22/#link-purpose-in-context)
- [ ] **2.4.5 Multiple Ways (AA):** Provide more than one way to locate pages within a set of pages, unless a page is part of a process. [W3C](https://www.w3.org/TR/WCAG22/#multiple-ways)
- [ ] **2.4.6 Headings and Labels (AA):** Make headings and labels describe the associated topic or purpose. [W3C](https://www.w3.org/TR/WCAG22/#headings-and-labels)
- [ ] **2.4.7 Focus Visible (AA):** Provide a visible keyboard-focus indicator for applicable user interface components. [W3C](https://www.w3.org/TR/WCAG22/#focus-visible)
- [ ] **2.4.11 Focus Not Obscured (Minimum) (AA):** Check that author-created content does not entirely hide the focused component. [W3C](https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum)
- [ ] **2.5.1 Pointer Gestures (A):** Provide a single-pointer alternative for applicable multipoint or path-based gestures, unless the gesture is essential. [W3C](https://www.w3.org/TR/WCAG22/#pointer-gestures)
- [ ] **2.5.2 Pointer Cancellation (A):** Check that applicable pointer actions satisfy an allowed condition, such as not executing on the down-event, an up-event with abort or undo, or a valid exception. [W3C](https://www.w3.org/TR/WCAG22/#pointer-cancellation)
- [ ] **2.5.3 Label in Name (A):** Ensure the accessible name of an applicable control contains the visible label text. [W3C](https://www.w3.org/TR/WCAG22/#label-in-name)
- [ ] **2.5.4 Motion Actuation (A):** Provide an interface alternative to applicable device or user motion and allow motion activation to be disabled, subject to exceptions. [W3C](https://www.w3.org/TR/WCAG22/#motion-actuation)
- [ ] **2.5.7 Dragging Movements (AA):** Provide a single-pointer method that does not require dragging for applicable drag operations, unless an exception applies. Keyboard access is assessed separately. [W3C](https://www.w3.org/TR/WCAG22/#dragging-movements)
- [ ] **2.5.8 Target Size (Minimum) (AA):** Check pointer targets against the 24 by 24 CSS pixel minimum or the spacing and other defined exceptions. [W3C](https://www.w3.org/TR/WCAG22/#target-size-minimum)

### 3. Understandable

- [ ] **3.1.1 Language of Page (A):** Make the default human language of each page programmatically determinable. [W3C](https://www.w3.org/TR/WCAG22/#language-of-page)
- [ ] **3.1.2 Language of Parts (AA):** Mark applicable changes in human language, accounting for the stated exceptions. [W3C](https://www.w3.org/TR/WCAG22/#language-of-parts)
- [ ] **3.2.1 On Focus (A):** Do not initiate a change of context solely because a component receives focus. [W3C](https://www.w3.org/TR/WCAG22/#on-focus)
- [ ] **3.2.2 On Input (A):** Do not unexpectedly change context when a setting changes; provide prior notice when the criterion allows it. [W3C](https://www.w3.org/TR/WCAG22/#on-input)
- [ ] **3.2.3 Consistent Navigation (AA):** Keep repeated navigational mechanisms in a consistent relative order across a set of pages unless the user changes them. [W3C](https://www.w3.org/TR/WCAG22/#consistent-navigation)
- [ ] **3.2.4 Consistent Identification (AA):** Identify components with the same functionality consistently within a set of pages. [W3C](https://www.w3.org/TR/WCAG22/#consistent-identification)
- [ ] **3.2.6 Consistent Help (A):** When the specified help mechanisms repeat across pages, keep them in a consistent relative order unless the user changes it. This criterion does not require every site to provide help. [W3C](https://www.w3.org/TR/WCAG22/#consistent-help)
- [ ] **3.3.1 Error Identification (A):** Identify and describe detected input errors in text. [W3C](https://www.w3.org/TR/WCAG22/#error-identification)
- [ ] **3.3.2 Labels or Instructions (A):** Provide labels or instructions when content requires user input. [W3C](https://www.w3.org/TR/WCAG22/#labels-or-instructions)
- [ ] **3.3.3 Error Suggestion (AA):** Provide known suggestions for correcting detected input errors unless doing so would compromise security or purpose. [W3C](https://www.w3.org/TR/WCAG22/#error-suggestion)
- [ ] **3.3.4 Error Prevention (Legal, Financial, Data) (AA):** For the specified legal or financial transactions, data changes, and user test submissions, provide an allowed means such as reversibility, checking and correction, or review and confirmation. [W3C](https://www.w3.org/TR/WCAG22/#error-prevention-legal-financial-data)
- [ ] **3.3.7 Redundant Entry (A):** In the same process, provide previously entered information automatically or for selection unless an exception applies. [W3C](https://www.w3.org/TR/WCAG22/#redundant-entry)
- [ ] **3.3.8 Accessible Authentication (Minimum) (AA):** When a cognitive-function test is used for authentication, provide an allowed alternative or assistance mechanism unless an exception applies. [W3C](https://www.w3.org/TR/WCAG22/#accessible-authentication-minimum)

### 4. Robust

- [ ] **4.1.2 Name, Role, Value (A):** Make applicable component names, roles, values, properties, and state changes programmatically available. Native controls can satisfy this without unnecessary ARIA. [W3C](https://www.w3.org/TR/WCAG22/#name-role-value)
- [ ] **4.1.3 Status Messages (AA):** Make applicable status messages programmatically determinable without requiring focus, using an appropriate mechanism. [W3C](https://www.w3.org/TR/WCAG22/#status-messages)

**Version note:** 4.1.1 Parsing was removed from WCAG 2.2. It remains visible as obsolete in W3C's serialization and is not counted among these 55 criteria. A specific legal or reporting obligation may reference an older version.

### Measurement details

- **Text contrast:** 1.4.3 generally requires 4.5:1 for normal text and 3:1 for large text. Large text is at least 18 pt, or 14 pt bold, or an equivalent size. Exceptions apply, including some incidental text and logotypes.
- **Non-text contrast:** 1.4.11 generally requires 3:1 against adjacent colors for applicable information needed to identify controls, states, or graphical objects. It is not a blanket rule for every decorative graphic.
- **Text resize and reflow:** 1.4.4 checks resizing text to 200%. The 320 CSS pixel width in 1.4.10 corresponds to 400% zoom from a 1280 CSS pixel viewport. These are different checks, with different scopes and exceptions.
- **Spacing overrides:** 1.4.12 tests line height of at least 1.5 times font size, spacing following paragraphs of at least 2 times font size, letter spacing of at least 0.12 times font size, and word spacing of at least 0.16 times font size. Content must tolerate these user overrides; the site is not required to use them by default.
- **Pointer targets:** 2.5.8 uses 24 by 24 CSS pixels or the specified spacing and other exceptions. The AAA target criterion and Android's native-app guidance use different dimensions and units.

## Level AAA: additional criteria

These 31 criteria extend the above A and AA set. AAA is not the default study target. W3C notes that it is not possible to satisfy every AAA criterion for some content. Apply them when a project, law, or study explicitly requires them, and consider them as quality improvements where relevant.

- [ ] **1.2.6 Sign Language (Prerecorded) (AAA):** Provide sign-language interpretation for applicable prerecorded audio in synchronized media. [W3C](https://www.w3.org/TR/WCAG22/#sign-language-prerecorded)
- [ ] **1.2.7 Extended Audio Description (Prerecorded) (AAA):** Provide extended audio description where the relevant prerecorded video requires pauses to convey visual information. [W3C](https://www.w3.org/TR/WCAG22/#extended-audio-description-prerecorded)
- [ ] **1.2.8 Media Alternative (Prerecorded) (AAA):** Provide an alternative for applicable prerecorded synchronized media and video-only media. [W3C](https://www.w3.org/TR/WCAG22/#media-alternative-prerecorded)
- [ ] **1.2.9 Audio-only (Live) (AAA):** Provide a text alternative for live audio-only information. [W3C](https://www.w3.org/TR/WCAG22/#audio-only-live)
- [ ] **1.3.6 Identify Purpose (AAA):** Make the purpose of applicable interface components, icons, and regions programmatically determinable. [W3C](https://www.w3.org/TR/WCAG22/#identify-purpose)
- [ ] **1.4.6 Contrast (Enhanced) (AAA):** Apply the enhanced text-contrast thresholds and exceptions. [W3C](https://www.w3.org/TR/WCAG22/#contrast-enhanced)
- [ ] **1.4.7 Low or No Background Audio (AAA):** Make applicable prerecorded speech easier to distinguish from background sound. [W3C](https://www.w3.org/TR/WCAG22/#low-or-no-background-audio)
- [ ] **1.4.8 Visual Presentation (AAA):** Support the specified presentation choices for blocks of text. [W3C](https://www.w3.org/TR/WCAG22/#visual-presentation)
- [ ] **1.4.9 Images of Text (No Exception) (AAA):** Use images of text only for the limited purposes allowed by the criterion. [W3C](https://www.w3.org/TR/WCAG22/#images-of-text-no-exception)
- [ ] **2.1.3 Keyboard (No Exception) (AAA):** Make all functionality operable through a keyboard interface. [W3C](https://www.w3.org/TR/WCAG22/#keyboard-no-exception)
- [ ] **2.2.3 No Timing (AAA):** Do not make timing essential to the applicable activity, subject to the listed exceptions. [W3C](https://www.w3.org/TR/WCAG22/#no-timing)
- [ ] **2.2.4 Interruptions (AAA):** Let users postpone or suppress interruptions, except emergencies. [W3C](https://www.w3.org/TR/WCAG22/#interruptions)
- [ ] **2.2.5 Re-authenticating (AAA):** Preserve user data when a session expires and the user re-authenticates. [W3C](https://www.w3.org/TR/WCAG22/#re-authenticating)
- [ ] **2.2.6 Timeouts (AAA):** Warn users of the duration of inactivity that could cause data loss, subject to the criterion's exception. [W3C](https://www.w3.org/TR/WCAG22/#timeouts)
- [ ] **2.3.2 Three Flashes (AAA):** Ensure content does not flash more than three times in any one-second period. [W3C](https://www.w3.org/TR/WCAG22/#three-flashes)
- [ ] **2.3.3 Animation from Interactions (AAA):** Allow applicable motion animation triggered by interaction to be disabled unless essential. [W3C](https://www.w3.org/TR/WCAG22/#animation-from-interactions)
- [ ] **2.4.8 Location (AAA):** Provide information about the user's location within a set of pages. [W3C](https://www.w3.org/TR/WCAG22/#location)
- [ ] **2.4.9 Link Purpose (Link Only) (AAA):** Make link purpose identifiable from the link text alone, with the stated exception. [W3C](https://www.w3.org/TR/WCAG22/#link-purpose-link-only)
- [ ] **2.4.10 Section Headings (AAA):** Use headings to organize content into sections. [W3C](https://www.w3.org/TR/WCAG22/#section-headings)
- [ ] **2.4.12 Focus Not Obscured (Enhanced) (AAA):** Ensure author-created content does not obscure any part of the focused component. [W3C](https://www.w3.org/TR/WCAG22/#focus-not-obscured-enhanced)
- [ ] **2.4.13 Focus Appearance (AAA):** Check the defined area and contrast requirements for the focus indicator, including exceptions. [W3C](https://www.w3.org/TR/WCAG22/#focus-appearance)
- [ ] **2.5.5 Target Size (Enhanced) (AAA):** Check the enhanced 44 by 44 CSS pixel target requirement and exceptions. [W3C](https://www.w3.org/TR/WCAG22/#target-size-enhanced)
- [ ] **2.5.6 Concurrent Input Mechanisms (AAA):** Do not restrict available input modalities except in the stated circumstances. [W3C](https://www.w3.org/TR/WCAG22/#concurrent-input-mechanisms)
- [ ] **3.1.3 Unusual Words (AAA):** Provide a way to identify definitions of unusual or restricted-use words. [W3C](https://www.w3.org/TR/WCAG22/#unusual-words)
- [ ] **3.1.4 Abbreviations (AAA):** Provide a way to identify the expanded form or meaning of abbreviations. [W3C](https://www.w3.org/TR/WCAG22/#abbreviations)
- [ ] **3.1.5 Reading Level (AAA):** Provide the specified supplemental content or simpler version for text above the defined reading level. [W3C](https://www.w3.org/TR/WCAG22/#reading-level)
- [ ] **3.1.6 Pronunciation (AAA):** Provide pronunciation where meaning is ambiguous without it. [W3C](https://www.w3.org/TR/WCAG22/#pronunciation)
- [ ] **3.2.5 Change on Request (AAA):** Initiate changes of context only on user request or provide a mechanism to turn them off. [W3C](https://www.w3.org/TR/WCAG22/#change-on-request)
- [ ] **3.3.5 Help (AAA):** Provide context-sensitive help. [W3C](https://www.w3.org/TR/WCAG22/#help)
- [ ] **3.3.6 Error Prevention (All) (AAA):** Apply the specified error-prevention options to all user submissions. [W3C](https://www.w3.org/TR/WCAG22/#error-prevention-all)
- [ ] **3.3.9 Accessible Authentication (Enhanced) (AAA):** Apply the enhanced authentication requirement and its exceptions. [W3C](https://www.w3.org/TR/WCAG22/#accessible-authentication-enhanced)

## Interaction patterns and inclusive practices

These checks apply only when the corresponding feature exists. They interpret or extend the criteria above; they are not additional universal WCAG success criteria. The [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) provides informative patterns, not the only conforming implementation.

- **Modal dialogs:** Review initial focus, keyboard movement, dismissal, background interaction, accessible name, and focus return. See the [modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
- **Tabs, menus, accordions, and comboboxes:** Check names, current state, relationships, keyboard interaction, and state updates against the actual pattern. Prefer native elements where suitable.
- **Forms:** Check visible and programmatic labels, required fields, understandable errors, correction, and successful completion. Do not assume that every form needs the same live-region or focus strategy.
- **Dynamic updates:** Inspect status changes and error feedback in the states where they occur. Verify actual assistive-technology behavior where possible; an `aria-live` attribute alone is not proof of an announcement.
- **Charts, tables, and complex images:** Check whether the information and relationships remain understandable without visual presentation. Avoid assuming that the existence of `alt` text alone makes it meaningful.
- **Movement and cognitive access:** Review distracting animation, reduced-motion preferences, plain language, predictable navigation, and error recovery. Use [W3C cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/) as additional guidance; not every suggestion is an AA requirement.
- **Embedded and external content:** Include applicable consent panels, third-party widgets, CAPTCHA, and downloadable documents in the agreed product scope. Review whether each can be operated and understood through the relevant input and output modes.
- **User preferences:** Review high-contrast or forced-colors modes, zoom, text sizing, and reduced-motion preferences where relevant. Identify which observations are WCAG criteria and which are additional platform or usability guidance.
- **Assistive technology and user experience:** Review keyboard-only use, zoom, mobile and desktop layouts, screen readers, and other relevant input modes. Involve disabled users when feasible. A single review does not represent all disabilities or technologies.

## Applying this checklist in the AI study

1. Freeze a task-specific subset and test procedure before the comparative runs. Preserve the full 55-criterion index so that exclusions are visible.
2. Assess the generated pages and relevant states, including the basic journey. Do not insert evaluation answers into the original task prompt.
3. Record model, runner, condition, version, browser, test states, tool versions, reviewer, and evidence. Use the same task-specific rules across conditions.
4. Record a missing required feature as a functionality failure and dependent checks as unassessable. Do not classify missing elements as zero accessibility defects.
5. Report automated rule findings, manual findings, incomplete checks, and functional outcomes separately. Do not treat axe impact labels as WCAG severity levels.
6. The list identifies what should be examined. It does not establish what ChatGPT, Gemini, or any other model skips. Those claims require evidence from named studies or our own completed runs.

Source provenance, relevant laws, platform guidance, and research findings are documented in [sources-and-ai-evidence.md](sources-and-ai-evidence.md). The machine-readable criterion index preserves W3C identifiers and names and is checked against the W3C serialization; see [coverage-verification.md](coverage-verification.md).
