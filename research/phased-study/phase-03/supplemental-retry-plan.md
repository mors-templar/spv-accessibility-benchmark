# Supplemental retry for the interrupted dashboard baseline

**Status:** Proposed after observing the failed exploratory attempt.
This is a development decision, not a preregistered retry policy.

The scheduled dashboard baseline `batch10` stopped after the runner reported a usage limit.
Its original record, events, and partial files remain unchanged.
The failed attempt stays in the scheduled-attempt denominator.

After the untouched scheduled attempts stop, make at most one fresh supplemental attempt.
Use run ID `supplemental01`, the same task bytes, baseline condition, model, and isolated runner configuration.
Record its timestamps, input hash, output, and status separately.
Do not reuse the partial workspace or overwrite the original record.

The supplemental result may help development and manual inspection.
Show it as an additional attempt, not as a replacement for `batch10`.
If the runner reports another usage limit, retain that result and stop.
