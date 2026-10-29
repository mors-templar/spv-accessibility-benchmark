#!/usr/bin/env python3
"""Build and check a versioned, research-authored web accessibility action list.

The WCAG links identify relevant criteria, not formal proofs of compliance.
The items are editable study material, not validated test procedures.
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = "0.1.0"
STANDARD = "https://www.w3.org/TR/2024/REC-WCAG22-20241212/#"
SOURCES = {
    "apg": ("W3C ARIA Authoring Practices Guide", "https://www.w3.org/WAI/ARIA/apg/"),
    "dialog": ("W3C modal dialog pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/"),
    "combobox": ("W3C combobox pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/combobox/"),
    "tabs": ("W3C tabs pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/tabs/"),
    "accordion": ("W3C accordion pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/accordion/"),
    "slider": ("W3C slider pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/slider/"),
    "menu": ("W3C menu and menubar pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/menubar/"),
    "carousel": ("W3C carousel pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/carousel/"),
    "forms": ("W3C forms tutorial", "https://www.w3.org/WAI/tutorials/forms/"),
    "images": ("W3C images tutorial", "https://www.w3.org/WAI/tutorials/images/"),
    "tables": ("W3C tables tutorial", "https://www.w3.org/WAI/tutorials/tables/"),
    "sortable": ("W3C sortable table example", "https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/"),
    "media": ("W3C accessible audio and video guide", "https://www.w3.org/WAI/media/av/"),
    "coga": ("W3C cognitive accessibility guidance", "https://www.w3.org/TR/coga-usable/"),
    "reduced_motion": ("W3C reduced-motion technique", "https://www.w3.org/WAI/WCAG22/Techniques/css/C39"),
    "evaluation": ("W3C evaluation overview", "https://www.w3.org/WAI/test-evaluate/"),
    "techniques": ("W3C WCAG techniques", "https://www.w3.org/WAI/WCAG22/Techniques/"),
}

# Row fields: explicit ID | kind | conditional action | related WCAG IDs, or - |
# candidate review methods | optional non-normative source key. Preserve IDs
# when revising released data and record changes between versions.
# R = WCAG-derived outcome, G = optional implementation guidance, P = study process.
GROUPS = [
    ("Scope and preparation", """
ACT-001 | P | Inventory pages, routes, dialog states, and complete user journeys before review. | - | manual | evaluation
ACT-002 | P | Record the requested features and identify missing or nonfunctional features separately. | - | manual | evaluation
ACT-003 | P | Determine which checklist items apply to each implemented page, state, and process. | - | manual | evaluation
ACT-004 | P | Record the browser, viewport, operating system, and assistive technologies used for testing. | - | manual | evaluation
ACT-005 | P | Test each relevant loading, empty, success, error, and disabled state that exists. | - | manual,keyboard | evaluation
ACT-006 | P | Do not treat an untested item, missing feature, or tool error as a pass. | - | manual | evaluation
ACT-007 | P | Consult the linked criterion and its exceptions before reporting a WCAG failure. | - | manual | evaluation
ACT-008 | P | Involve people with disabilities and assistive-technology expertise where feasible. | - | manual | evaluation
ACT-009 | P | Include embedded and third-party content in scope when it forms part of the experience. | - | manual | evaluation
ACT-010 | P | Preserve original generated artifacts and record any changes made for testing. | - | manual | evaluation
"""),
    ("Page structure, reading order, and language", """
ACT-011 | R | Provide a descriptive page title for every page. | 2.4.2 | manual,automated | -
ACT-012 | R | Expose the default human language of each page programmatically. | 3.1.1 | manual,automated | -
ACT-013 | R | Identify changes in human language programmatically when the criterion applies. | 3.1.2 | manual,assistive-technology | -
ACT-014 | R | Expose meaningful headings and the relationships they convey programmatically or in text. | 1.3.1 | manual,assistive-technology | -
ACT-015 | R | Write headings and labels that describe their topic or purpose. | 2.4.6 | manual | -
ACT-016 | R | Preserve a meaningful programmatic sequence when the order affects meaning. | 1.3.2 | manual,assistive-technology | -
ACT-017 | R | Expose meaningful list relationships programmatically or in text. | 1.3.1 | manual,assistive-technology | -
ACT-018 | R | Expose meaningful group and section relationships programmatically or in text. | 1.3.1 | manual,assistive-technology | -
ACT-019 | R | Provide a way to bypass repeated blocks when they appear on multiple pages. | 2.4.1 | manual,keyboard | -
ACT-020 | R | Offer multiple ways to locate pages in a set, subject to the process exception. | 2.4.5 | manual | -
ACT-021 | R | Keep repeated navigation in consistent relative order unless the user changes it. | 3.2.3 | manual | -
ACT-022 | R | Identify components with the same functionality consistently across a set of pages. | 3.2.4 | manual,assistive-technology | -
ACT-023 | R | Keep repeated help mechanisms in consistent relative order when the criterion applies. | 3.2.6 | manual | -
ACT-024 | G | Use native headings, lists, landmarks, and other HTML elements when they convey the intended structure. | 1.3.1 | manual,assistive-technology | techniques
ACT-025 | G | Consider a skip link that reaches the main content when repeated navigation is present. | 2.4.1 | keyboard | techniques
ACT-026 | G | Avoid positive tabindex values that can make focus order difficult to maintain. | 2.4.3 | manual,keyboard | apg
"""),
    ("Images, icons, links, and instructions", """
ACT-027 | R | Give meaningful images an equivalent text alternative, accounting for applicable exceptions. | 1.1.1 | manual,assistive-technology,automated | -
ACT-028 | R | Give image-based controls a text alternative that communicates their purpose. | 1.1.1,4.1.2 | manual,assistive-technology | -
ACT-029 | R | Allow decorative non-text content to be ignored by assistive technology when appropriate. | 1.1.1 | manual,assistive-technology | -
ACT-030 | R | Supply equivalent information for informative charts, diagrams, and complex images. | 1.1.1 | manual,assistive-technology | -
ACT-031 | R | Give non-text CAPTCHA alternatives that accommodate different sensory abilities when CAPTCHA is used. | 1.1.1 | manual | -
ACT-032 | R | Make link purpose understandable from link text or its programmatically determined context. | 2.4.4 | manual,assistive-technology | -
ACT-033 | R | Avoid instructions that rely solely on sensory characteristics such as position, shape, or sound. | 1.3.3 | manual | -
ACT-034 | R | Convey information without relying on color alone. | 1.4.1 | manual | -
ACT-035 | R | Use text instead of images of text where the criterion applies and no exception applies. | 1.4.5 | manual | -
ACT-036 | R | Include the visible text of a control in its accessible name when the criterion applies. | 2.5.3 | manual,assistive-technology | -
ACT-037 | G | For an icon-only button, provide a meaningful accessible name describing its action. | 1.1.1,4.1.2 | manual,assistive-technology | images
ACT-038 | G | Describe an informational image according to its purpose in the surrounding content. | 1.1.1 | manual | images
ACT-039 | G | Provide chart data in an accessible table or text summary when that gives an equivalent alternative. | 1.1.1,1.3.1 | manual,assistive-technology | images
ACT-040 | R | Provide the required text alternative for other non-text content, accounting for the criterion exceptions. | 1.1.1 | manual,assistive-technology | -
ACT-041 | G | Give an image-only link an accessible name that identifies the link purpose. | 1.1.1,2.4.4 | manual,assistive-technology | images
"""),
    ("Color, contrast, layout, and display adaptation", """
ACT-042 | R | Check normal text and its background for at least 4.5:1 contrast, subject to the criterion exceptions. | 1.4.3 | visual,automated | -
ACT-043 | R | Check large text and its background for at least 3:1 contrast, subject to the criterion exceptions. | 1.4.3 | visual,automated | -
ACT-044 | R | Check applicable control boundaries and state indicators for at least 3:1 contrast against adjacent colors. | 1.4.11 | visual,manual | -
ACT-045 | R | Check visual parts of graphics required for understanding for at least 3:1 contrast, subject to exceptions. | 1.4.11 | visual,manual | -
ACT-046 | R | Allow text to resize to 200% without loss of content or functionality, subject to exceptions. | 1.4.4 | visual,manual | -
ACT-047 | R | Support reflow at 320 CSS pixels wide for vertically scrolling content, subject to exceptions. | 1.4.10 | visual,manual | -
ACT-048 | R | Support reflow at 256 CSS pixels high for horizontally scrolling content, subject to exceptions. | 1.4.10 | visual,manual | -
ACT-049 | R | Preserve content and functionality when users apply the text-spacing overrides in the criterion. | 1.4.12 | visual,manual | -
ACT-050 | R | Support portrait and landscape orientation unless a particular orientation is essential. | 1.3.4 | visual,manual | -
ACT-051 | R | Make extra content shown on hover or focus dismissible when the criterion requires it. | 1.4.13 | keyboard,visual | -
ACT-052 | R | Let users move the pointer over applicable hover-triggered content without it disappearing. | 1.4.13 | manual,visual | -
ACT-053 | R | Keep applicable hover- or focus-triggered content visible until a criterion-defined dismissal condition occurs. | 1.4.13 | manual,keyboard | -
ACT-054 | G | Test text over images and gradients at the least-contrasting visible area. | 1.4.3 | visual,manual | techniques
ACT-055 | G | Use an additional shape, text, or icon to distinguish states that also use color. | 1.4.1 | visual,manual | techniques
ACT-056 | G | Respect the user's reduced-motion preference where motion can be reduced. | 2.3.3 | visual,manual | reduced_motion
ACT-057 | G | Test the interface with browser zoom and increased text spacing. | 1.4.4,1.4.10,1.4.12 | visual,manual | techniques
ACT-058 | G | Check focus indicators and controls in forced-colors or high-contrast display modes. | 2.4.7,1.4.11 | visual,keyboard | techniques
ACT-059 | G | Check contrast in each available theme and relevant interactive state. | 1.4.3,1.4.11 | visual,manual | techniques
"""),
    ("Keyboard, focus, and pointer input", """
ACT-060 | R | Make functionality operable through a keyboard interface, subject to the path-dependent exception. | 2.1.1 | keyboard | -
ACT-061 | R | Do not require specific timings for individual keystrokes, subject to the keyboard criterion exception. | 2.1.1 | keyboard | -
ACT-062 | R | Let users move keyboard focus away from each component. | 2.1.2 | keyboard | -
ACT-063 | R | Explain any nonstandard way to move focus out of a component. | 2.1.2 | keyboard,manual | -
ACT-064 | R | Preserve meaning and operability in focus order when sequence affects them. | 2.4.3 | keyboard,manual | -
ACT-065 | R | Show a visible focus indicator for keyboard-operable interfaces. | 2.4.7 | keyboard,visual | -
ACT-066 | R | Prevent author-created content from entirely obscuring the focused component. | 2.4.11 | keyboard,visual | -
ACT-067 | R | Permit applicable character-only shortcuts to be disabled, remapped, or active only on focus. | 2.1.4 | keyboard,manual | -
ACT-068 | R | Provide a single-pointer alternative for applicable multipoint or path-based gestures. | 2.5.1 | manual | -
ACT-069 | R | Provide a single-pointer alternative to dragging when the dragging criterion applies. | 2.5.7 | manual | -
ACT-070 | R | Support pointer cancellation using an allowed condition or applicable exception. | 2.5.2 | manual | -
ACT-071 | R | Provide an interface alternative to motion actuation when the criterion applies. | 2.5.4 | manual | -
ACT-072 | R | Allow applicable motion actuation to be disabled, subject to the criterion exceptions. | 2.5.4 | manual | -
ACT-073 | R | Make pointer targets at least 24 by 24 CSS pixels or satisfy an allowed exception. | 2.5.8 | manual,visual | -
ACT-074 | R | Do not trigger a change of context merely when a component receives focus. | 3.2.1 | keyboard,manual | -
ACT-075 | R | Do not unexpectedly change context when a setting changes; provide prior notice where allowed. | 3.2.2 | keyboard,manual | -
ACT-076 | G | Use native links for navigation and native buttons for actions where appropriate. | 2.1.1,4.1.2 | keyboard,assistive-technology | apg
ACT-077 | G | Check keyboard operation independently from the non-dragging pointer alternative. | 2.1.1,2.5.7 | keyboard,manual | techniques
ACT-078 | G | Check focused elements around sticky headers, overlays, and mobile virtual keyboards. | 2.4.11 | keyboard,visual | techniques
ACT-079 | G | Provide an accessible, visible close control for dismissible overlays. | 2.1.1,4.1.2 | keyboard,assistive-technology | dialog
ACT-080 | G | Check that tab order reaches visible controls without reaching hidden controls unexpectedly. | 2.4.3 | keyboard | techniques
ACT-081 | G | Make keyboard focus visually distinguishable on all interactive controls. | 2.4.7 | keyboard,visual | techniques
"""),
    ("Forms, errors, authentication, and transactions", """
ACT-082 | R | Provide labels or instructions when a user must enter data. | 3.3.2 | manual,assistive-technology | -
ACT-083 | R | Expose the relationship between a label and its input programmatically or in text. | 1.3.1 | manual,assistive-technology | -
ACT-084 | R | Identify applicable input purposes programmatically for fields collecting information about the user. | 1.3.5 | manual,automated | -
ACT-085 | R | Identify detected input errors and describe them in text. | 3.3.1 | manual,keyboard | -
ACT-086 | R | Suggest known corrections for detected input errors unless security or purpose would be compromised. | 3.3.3 | manual | -
ACT-087 | R | Give an allowed error-prevention mechanism for the transactions covered by the criterion. | 3.3.4 | manual | -
ACT-088 | R | Reuse information entered earlier in the same process or make it selectable, subject to exceptions. | 3.3.7 | manual | -
ACT-089 | R | Provide an allowed alternative or assistance mechanism for authentication cognitive tests, subject to exceptions. | 3.3.8 | manual | -
ACT-090 | R | Make form-control names and roles programmatically determinable. | 4.1.2 | assistive-technology,automated | -
ACT-091 | R | Expose applicable form status messages so assistive technology can present them without focus. | 4.1.3 | assistive-technology,manual | -
ACT-092 | G | Keep visible labels available after users start typing. | 3.3.2 | manual | forms
ACT-093 | G | Indicate required fields and input format before users submit the form. | 3.3.2 | manual | forms
ACT-094 | G | Associate field-specific error text with the affected input. | 1.3.1,3.3.1 | assistive-technology,manual | forms
ACT-095 | G | Provide an error summary linked to affected fields when a long form has several errors. | 3.3.1,3.3.3 | keyboard,assistive-technology | forms
ACT-096 | G | Allow password managers and pasting for authentication where feasible. | 3.3.8 | manual | techniques
ACT-097 | G | Avoid clearing correctly entered form data after a failed submission. | 3.3.3 | manual | forms
ACT-098 | G | Make review and correction available before a significant transaction is submitted. | 3.3.4 | keyboard,manual | techniques
ACT-099 | G | Expose expanded or selected states when multi-step navigation uses interactive controls. | 4.1.2 | keyboard,assistive-technology | apg
ACT-100 | G | Use appropriate autocomplete tokens for applicable personal-information fields. | 1.3.5 | manual,automated | forms
ACT-101 | G | Check form validation and correction with both keyboard and assistive technology. | 3.3.1,3.3.3 | keyboard,assistive-technology | forms
"""),
    ("Cognitive accessibility and clear content", """
ACT-102 | G | Use clear, familiar words and explain unfamiliar terms when needed. | - | manual | coga
ACT-103 | G | Make the purpose of each page and its important actions easy to identify. | - | manual | coga
ACT-104 | G | Break complex instructions into clear steps. | - | manual | coga
ACT-105 | G | Reduce the need to remember information across multiple steps where feasible. | - | manual | coga
ACT-106 | G | Allow users to go back and correct mistakes without losing their work where feasible. | - | manual | coga
ACT-107 | G | Make help or feedback options easy to find when they are provided. | - | manual | coga
ACT-108 | G | Tell users about relevant costs and required information before they begin a process. | - | manual | coga
ACT-109 | G | Avoid making controls or content move unexpectedly. | - | manual,visual | coga
"""),
    ("Dynamic content and assistive-technology semantics", """
ACT-110 | R | Expose each user-interface component's name and role programmatically. | 4.1.2 | assistive-technology,automated | -
ACT-111 | R | Make user-settable component states, properties, and values programmatically settable. | 4.1.2 | assistive-technology,manual | -
ACT-112 | R | Notify user agents, including assistive technologies, of changes to names, roles, states, properties, and values. | 4.1.2 | assistive-technology,manual | -
ACT-113 | R | Expose applicable status messages so assistive technology can present them without focus. | 4.1.3 | assistive-technology,manual | -
ACT-114 | R | Preserve meaningful information and relationships conveyed through presentation in code or text. | 1.3.1 | assistive-technology,manual | -
ACT-115 | G | Prefer native HTML semantics where they already provide the correct accessible behavior. | 4.1.2 | assistive-technology,keyboard | apg
ACT-116 | G | Use live regions or suitable native status semantics for applicable asynchronous status messages. | 4.1.3 | assistive-technology,manual | techniques
ACT-117 | G | Check that live messages announce once, at an appropriate priority, with useful content. | 4.1.3 | assistive-technology,manual | techniques
ACT-118 | G | Update accessible expanded, selected, checked, and pressed states when their controls change. | 4.1.2 | assistive-technology,keyboard | apg
ACT-119 | G | Avoid adding ARIA roles or attributes that conflict with native semantics. | 4.1.2 | assistive-technology,manual | apg
ACT-120 | G | Check that hidden or inactive content does not leave unexpected focusable controls available. | 2.4.3,4.1.2 | keyboard,assistive-technology | apg
ACT-121 | G | Check that an accessible status is understandable without surrounding visual context. | 4.1.3 | assistive-technology,manual | techniques
"""),
    ("Dialogs and overlays, when present", """
ACT-122 | G | Give each dialog an accessible name that identifies its purpose. | 4.1.2 | assistive-technology,manual | dialog
ACT-123 | G | Move focus to an appropriate location inside a modal dialog when it opens. | 2.4.3 | keyboard,assistive-technology | dialog
ACT-124 | G | Keep background content inert while a true modal dialog is open. | 2.4.3 | keyboard,manual | dialog
ACT-125 | G | Keep Tab and Shift+Tab within an open modal dialog. | 2.1.2,2.4.3 | keyboard | dialog
ACT-126 | G | Let users close a modal dialog with Escape when the pattern permits it. | 2.1.1,2.1.2 | keyboard | dialog
ACT-127 | G | Return focus to the invoking control after closing a dialog when it remains the logical destination. | 2.4.3 | keyboard,assistive-technology | dialog
ACT-128 | G | Choose a logical focus destination if the invoking control no longer exists. | 2.4.3 | keyboard,manual | dialog
ACT-129 | G | Check nested dialogs and overlays in each open and close sequence. | 2.4.3 | keyboard,manual | dialog
"""),
    ("Menus, tabs, accordions, and carousels, when present", """
ACT-130 | G | Distinguish ordinary site navigation from an application-style menu before choosing roles. | 4.1.2 | manual,assistive-technology | menu
ACT-131 | G | For application-style menus, implement the keyboard interactions for the chosen pattern. | 2.1.1 | keyboard | menu
ACT-132 | G | For tabs, expose the selected tab and its associated panel. | 1.3.1,4.1.2 | assistive-technology,manual | tabs
ACT-133 | G | For tabs, implement the keyboard navigation of the selected tabs pattern. | 2.1.1 | keyboard | tabs
ACT-134 | G | For accordions, expose whether each controlled panel is expanded or collapsed. | 4.1.2 | assistive-technology,keyboard | accordion
ACT-135 | G | For accordions, make each panel trigger keyboard operable. | 2.1.1 | keyboard | accordion
ACT-136 | G | For carousels, provide accessible controls to move between items. | 2.1.1,4.1.2 | keyboard,assistive-technology | carousel
ACT-137 | G | For automatically rotating carousels, provide an applicable pause or stop mechanism. | 2.2.2 | keyboard,manual | carousel
ACT-138 | G | Check that closed menus and inactive panels do not expose inappropriate focus targets. | 2.4.3 | keyboard | apg
"""),
    ("Comboboxes, listboxes, and sliders, when present", """
ACT-139 | G | Give a combobox an accessible name and expose its expanded or collapsed state. | 4.1.2 | assistive-technology,manual | combobox
ACT-140 | G | Connect a combobox to its popup using the semantics required by the selected pattern. | 1.3.1,4.1.2 | assistive-technology,manual | combobox
ACT-141 | G | Support the selected combobox pattern's keyboard interactions, including navigation and selection. | 2.1.1 | keyboard | combobox
ACT-142 | G | Keep the active option available to assistive technology when focus remains on the combobox. | 4.1.2 | assistive-technology,keyboard | combobox
ACT-143 | G | Preserve normal text-editing keys in an editable combobox. | 2.1.1 | keyboard | combobox
ACT-144 | G | Expose a custom slider's name, current value, and allowed range. | 4.1.2 | assistive-technology,manual | slider
ACT-145 | G | Support the keyboard interactions of the selected slider pattern. | 2.1.1 | keyboard | slider
ACT-146 | G | Offer a non-dragging single-pointer way to change a slider when the criterion applies. | 2.5.7 | manual | slider
ACT-147 | G | Verify custom widgets with actual assistive technologies, including touch where relevant. | 4.1.2 | assistive-technology,manual | slider
"""),
    ("Tables, dashboards, and data displays, when present", """
ACT-148 | R | Make data-table headers and cell relationships programmatically determinable or available in text. | 1.3.1 | assistive-technology,manual | -
ACT-149 | R | Ensure the information conveyed by a chart has an equivalent text alternative. | 1.1.1 | manual,assistive-technology | -
ACT-150 | R | Do not use color alone to distinguish chart data or status. | 1.4.1 | visual,manual | -
ACT-151 | G | Use appropriate native table elements for tabular data. | 1.3.1 | assistive-technology,manual | tables
ACT-152 | G | Associate complex table cells with the correct headers. | 1.3.1 | assistive-technology,manual | tables
ACT-153 | G | Expose the current sort state on the relevant header when a table is sortable. | 4.1.2 | assistive-technology,keyboard | sortable
ACT-154 | G | Make sort and row-expansion controls keyboard operable and clearly named. | 2.1.1,4.1.2 | keyboard,assistive-technology | tables
ACT-155 | G | Announce result counts or updated data when the update is an applicable status message. | 4.1.3 | assistive-technology,manual | techniques
ACT-156 | G | Test scrollable data regions for usable focus and reading order at narrow widths. | 1.3.2,2.4.3 | keyboard,visual | tables
ACT-157 | G | Test data updates, sorting, and filtering with assistive technology in each relevant state. | 4.1.2,4.1.3 | assistive-technology,keyboard | sortable
"""),
    ("Audio, video, animation, and time limits, when present", """
ACT-158 | R | Provide the required alternative for prerecorded audio-only content, subject to exceptions. | 1.2.1 | manual | -
ACT-159 | R | Provide the required alternative for prerecorded video-only content, subject to exceptions. | 1.2.1 | manual | -
ACT-160 | R | Provide captions for prerecorded synchronized audio, subject to the stated exception. | 1.2.2 | manual | -
ACT-161 | R | Provide an audio description or media alternative for applicable prerecorded synchronized media. | 1.2.3 | manual | -
ACT-162 | R | Provide captions for live audio in synchronized media. | 1.2.4 | manual | -
ACT-163 | R | Provide audio description for applicable prerecorded synchronized video. | 1.2.5 | manual | -
ACT-164 | R | Provide an allowed audio control if automatic audio plays for more than three seconds. | 1.4.2 | keyboard,manual | -
ACT-165 | R | Provide an allowed way to turn off, adjust, or extend applicable time limits. | 2.2.1 | manual,keyboard | -
ACT-166 | R | Provide pause, stop, or hide controls for applicable automatic moving, blinking, or scrolling content. | 2.2.2 | keyboard,manual | -
ACT-167 | R | Provide a way to pause, stop, hide, or control the frequency of applicable auto-updating information. | 2.2.2 | keyboard,manual | -
ACT-168 | R | Keep flashes within the frequency or general and red flash thresholds in the criterion. | 2.3.1 | visual,manual | -
ACT-169 | G | Provide keyboard-operable and named controls for any custom media player. | 2.1.1,4.1.2 | keyboard,assistive-technology | media
ACT-170 | G | Review captions for accuracy, speaker information, and synchronization. | 1.2.2,1.2.4 | manual | media
ACT-171 | G | Use a transcript as an additional way to access audio or video content where feasible. | 1.2.1,1.2.3 | manual | media
ACT-172 | G | Warn users before a timeout and preserve their entered data where feasible. | 2.2.1 | manual | coga
"""),
    ("Verification and evidence", """
ACT-173 | P | Run automated accessibility checks across the selected pages and interactive states. | - | automated | evaluation
ACT-174 | P | Review automated findings, incomplete results, and tool errors individually. | - | automated,manual | evaluation
ACT-175 | P | Traverse the full flow with a keyboard and inspect visible focus. | - | keyboard,visual | evaluation
ACT-176 | P | Review semantics and announcements with suitable assistive technologies. | - | assistive-technology,manual | evaluation
ACT-177 | P | Inspect text alternatives, instructions, captions, and error messages for meaning. | - | manual | evaluation
ACT-178 | P | Exercise relevant pointer, touch, motion, zoom, and display conditions. | - | manual,visual | evaluation
ACT-179 | P | Save reproducible steps, the affected page state, expected behavior, and observed behavior. | - | manual | evaluation
ACT-180 | P | Link each issue to evidence and the applicable criterion or guidance. | - | manual | evaluation
ACT-181 | P | Record pass, fail, not applicable, unassessable, or not tested with reasons. | - | manual | evaluation
ACT-182 | P | Report missing required features separately from accessibility results. | - | manual | evaluation
ACT-183 | P | Record tool versions and rules, reviewer experience, and test limitations. | - | manual | evaluation
ACT-184 | P | Do not present a clean automated scan as proof of WCAG conformance. | - | manual | evaluation
ACT-185 | P | Keep the evaluation checklist and scoring instructions out of the unchanged baseline input. | - | manual | evaluation
ACT-186 | P | Record whether each reviewed issue comes from the generated site or an external dependency. | - | manual | evaluation
ACT-187 | P | Keep reviewer evidence and final decisions separate from assumptions made before testing. | - | manual | evaluation
ACT-188 | P | Keep study guidance out of the baseline runtime, including automatically loaded workspace instructions. | - | manual | evaluation
"""),
]


def load_items():
    items = []
    for section, rows in GROUPS:
        for line in rows.strip().splitlines():
            parts = [part.strip() for part in line.split("|")]
            if len(parts) != 6:
                raise ValueError(f"Expected six fields in {section}: {line}")
            item_id, kind, action, criteria, methods, source = parts
            items.append({
                "id": item_id,
                "section": section,
                "basis": kind,
                "action": action,
                "wcag_criteria": [] if criteria == "-" else criteria.split(","),
                "candidate_methods": methods.split(","),
                "guidance_source": None if source == "-" else source,
            })
    return items


def check_items(items, index):
    if STANDARD != index["normative_standard"] + "#":
        raise ValueError("WCAG links do not point to the indexed Recommendation version.")
    criteria = {c["number"]: c for c in index["criteria"]}
    required = {number for number, c in criteria.items() if c["level"] in ("A", "AA")}
    methods = {"manual", "keyboard", "visual", "assistive-technology", "automated"}
    seen = set()
    covered = set()
    for item in items:
        if not re.fullmatch(r"ACT-\d{3,}", item["id"]) or item["id"] in seen:
            raise ValueError(f"Invalid or duplicate action ID: {item['id']}")
        seen.add(item["id"])
        if item["basis"] not in ("R", "G", "P") or not item["action"]:
            raise ValueError(f"Invalid action: {item['id']}")
        if not item["candidate_methods"] or not set(item["candidate_methods"]) <= methods:
            raise ValueError(f"Invalid review method: {item['id']}")
        if not set(item["wcag_criteria"]) <= set(criteria):
            raise ValueError(f"Unknown criterion: {item['id']}")
        if item["basis"] == "R":
            if not item["wcag_criteria"] or not set(item["wcag_criteria"]) <= required or item["guidance_source"] is not None:
                raise ValueError(f"WCAG-derived item has invalid references: {item['id']}")
            covered.update(item["wcag_criteria"])
        if item["basis"] == "G":
            if item["guidance_source"] not in SOURCES:
                raise ValueError(f"Guidance item lacks references: {item['id']}")
        if item["basis"] == "P" and item["guidance_source"] not in SOURCES:
            raise ValueError(f"Process item lacks a source: {item['id']}")
    missing = sorted(required - covered)
    if missing:
        raise ValueError(f"Missing WCAG A/AA outcomes: {', '.join(missing)}")
    return criteria


def render(items, criteria):
    lines = [
        "# Master accessibility action checklist for web projects",
        "",
        f"**Version:** {VERSION}, 2026-10-29. **Status:** research draft for expert review.",
        "",
        "This checklist translates WCAG 2.2 into practical actions for building and reviewing websites. It is a study resource, not a validated intervention, test suite, or conformance claim.",
        "",
        "**How to use it:** Inventory the actual pages, states, and tasks first. Apply each item only when its feature and conditions exist. Consult the linked WCAG criterion, definitions, exceptions, and conformance requirements before deciding whether it passes. Requirements can be met in different ways. Missing required features are functional failures and may make dependent checks unassessable.",
        "",
        "The source is the [12 December 2024 WCAG 2.2 Recommendation](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), especially Levels A and AA. The complete criterion index, including AAA, is in [master-checklist.md](master-checklist.md). A guidance item can also refer to an AAA criterion. Related criterion links identify the topic; a checked action does not prove that the entire criterion passes. This checklist does not cover every accessibility need or establish legal compliance.",
        "",
        "[Sources and AI evidence](sources-and-ai-evidence.md) separates published observations from untested hypotheses. Items in this checklist are potential checks; they are not claims that the selected models or sites have failed them.",
        "",
        "### Item labels",
        "",
        "- **R: WCAG-derived outcome.** A plain-language summary of a requirement, subject to the linked criterion and exceptions. It is not the normative text.",
        "- **G: Guidance.** A possible technique or interaction pattern. It is not mandatory merely because W3C recommends or illustrates it.",
        "- **P: Research process.** A proposed study or review practice, not a WCAG success criterion.",
        "",
        "**Review methods** are possible approaches: manual, keyboard, visual, assistive technology, and automated. They are not complete procedures, and automated checks cannot determine conformance alone. A checklist item may need several tests, states, devices, or reviewers.",
        "",
        "For a criterion or relevant R item, record **pass**, **fail**, **not applicable**, **unassessable**, or **not tested**, with evidence and rationale. A G item records use of one optional technique; not using it does not by itself establish a WCAG failure. Record P items as study activities, not website defects. Do not count unchecked items as failures. Freeze the checklist, test protocol, and any scoring rules before confirmatory runs. Keep this evaluation reference out of the unmodified baseline prompt.",
        "",
        "Numeric context: large text is at least 18 pt or 14 pt bold under WCAG's definition. Reflow includes exceptions for content requiring two-dimensional layout. Target size has spacing and other exceptions. The text-spacing criterion specifies line height 1.5 times font size, following paragraph spacing 2 times, letter spacing 0.12 times, and word spacing 0.16 times.",
    ]
    current = None
    for item in items:
        if item["section"] != current:
            current = item["section"]
            lines += ["", "## " + current, ""]
        refs = []
        for number in item["wcag_criteria"]:
            criterion = criteria[number]
            refs.append(f"[{number}]({STANDARD}{criterion['anchor']})")
        if item["guidance_source"]:
            label, url = SOURCES[item["guidance_source"]]
            refs.append(f"[{label}]({url})")
        methods = ", ".join(item["candidate_methods"])
        anchor = item["id"].lower()
        lines.append(f"- [ ] <a id=\"{anchor}\"></a> **{item['id']} [{item['basis']}]** {item['action']}<br>")
        lines.append(f"  Sources: {', '.join(refs)}. Possible checks: {methods}.")
    lines += [
        "", "## Applying the list to the five selected tasks", "",
        "These are possible review areas based on the selected task descriptions. Determine applicability from the actual task and generated artifact; do not assume the features were generated or function correctly. See [working decisions](../study-working-decisions.md).",
        "",
        "| Selected task | Areas to inspect if present or requested |",
        "| --- | --- |",
        "| 7: Services | Page structure, tabs, FAQ disclosures, and any order-related controls. |",
        "| 8: Consulting | Structure, text contrast, animation, navigation, and relevant interactive states. The original task explicitly mentions accessible contrast and semantic HTML. |",
        "| 18: Cinema | Listing navigation, ticket selection, forms, error states, and any confirmation process. |",
        "| 19: Dashboard | Keyboard access, the single-pointer alternative to dragging, chart alternatives, and data updates. |",
        "| 1: Portfolio | Navigation, project links, images, headings, responsive layout, and any additional controls. |",
        "",
        "", "## Coverage and limits", "",
        "The generator checks that each of the 55 WCAG 2.2 A/AA criteria has at least one R item. This checks references and coverage only. It does not validate the paraphrases, prove that every condition is represented, or turn these actions into a complete audit procedure.",
        "",
        "An action that represents a possible technique is labelled G even when the underlying outcome is required. These suggestions do not imply that every site needs every listed widget. AAA criteria, legal context, empirical AI evidence, and source limitations remain in the related accessibility research files. Guidance pages may change; record their versions or retrieval dates when the study protocol is frozen.",
        "",
        "For study results, the unit of analysis, applicable denominator, state sampling, issue deduplication, reviewer calibration, and scoring need to be set in a separate protocol before runs begin.",
        "", "## WCAG 2.2 A/AA crosswalk", "",
        "Each link below points to at least one WCAG-derived action that refers to the criterion. The mapping is not a complete set of test cases or a claim of correct interpretation.",
    ]
    for number, criterion in criteria.items():
        if criterion["level"] not in ("A", "AA"):
            continue
        relevant = [item for item in items if item["basis"] == "R" and number in item["wcag_criteria"]]
        actions = ", ".join(f"[{item['id']}](#{item['id'].lower()})" for item in relevant)
        lines.append(f"- [{number} {criterion['name']} ({criterion['level']})]({STANDARD}{criterion['anchor']}): {actions}.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify that generated files are current without writing them.")
    args = parser.parse_args()
    index = json.loads((HERE / "wcag22-criteria-index.json").read_text(encoding="utf-8"))
    items = load_items()
    criteria = check_items(items, index)
    data = {
        "version": VERSION,
        "status": "research_draft_not_validated",
        "criteria_source": index["normative_standard"],
        "labels": {"R": "WCAG-derived outcome", "G": "Non-mandatory guidance", "P": "Proposed research process"},
        "sources": {key: {"name": name, "url": url} for key, (name, url) in SOURCES.items()},
        "items": items,
    }
    outputs = {
        HERE / "master-action-checklist.md": render(items, criteria),
        HERE / "action-checklist.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    }
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise ValueError(f"Generated file differs: {path.name}")
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    counts = collections.Counter(item["basis"] for item in items)
    print(f"Actions: {len(items)} ({counts['R']} WCAG-derived, {counts['G']} guidance, {counts['P']} research process).")
    required_count = sum(c["level"] in ("A", "AA") for c in criteria.values())
    print(f"Coverage: {required_count} of {required_count} A/AA criterion IDs referenced by WCAG-derived outcomes.")
    print("Reference coverage and generated-file consistency only; expert content review remains necessary.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
