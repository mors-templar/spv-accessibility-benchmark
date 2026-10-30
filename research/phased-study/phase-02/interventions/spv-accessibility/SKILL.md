---
name: spv-accessibility
description: Plan and check accessibility for a requested website using the supplied checklist and an advisory plan diagnostic.
---

# Website accessibility plan

1. Read the original website request and the supplied checklist.
2. Identify required user journeys and interface features.
3. Identify relevant R items and G guidance for those features.
4. Plan keyboard use, names, states, visual presentation, and errors when relevant.
5. Ask a question for each material accessibility risk.
6. Answer each question with a concrete plan or mark it unknown.
7. Save the plan and questions in `spv-plan.md` when files can be written.
8. Otherwise, put the plan and questions before the code in the response.
9. Call `verify_plan` with the plan and questions when that tool is available.
10. Consider every diagnostic warning before implementation.
11. Keep the user's required features in the implementation.
12. Test observable behavior with available tools.
13. Mark unobserved checklist items as unassessed.
14. Record the diagnostic result and any unresolved risks.

The diagnostic is advisory and does not establish WCAG conformance.
Guidance may describe a technique; its underlying outcome can still be required.
