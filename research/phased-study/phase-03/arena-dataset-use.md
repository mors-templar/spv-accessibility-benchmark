# Arena dataset use: terms and uncertainty

Reviewed on 30 October 2026. This note records research evidence, not a legal determination.

The selected task manifest identifies the WebDev Arena Preference 10K dataset.
Its [dataset card and license agreement](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k#dataset-license-agreement) set the applicable published terms.
The [recorded dataset revision](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k/blob/7c397e652ffb8c2384e6d71d21d8388c19365fdc/README.md) contains the same clause.

The agreement's section on prohibited transfers says:

> You should not distribute, copy, disclose, assign, sublicense, embed, host, or otherwise transfer the dataset to any third party.

The agreement also grants a limited license for research and commercial purposes, subject to its conditions.
It refers to the dataset, including conversations and annotations.
Read the full agreement for its other conditions.

The clause does not explicitly mention submitting individual prompts to hosted model APIs.
It does not define how a model service provider is treated in that use case.
We cannot determine from this wording alone whether a separate permission is mandatory.
It is also unclear how publication of task text or outputs is treated.

As of this review, the researcher reports no separate written permission.
The researcher chose to proceed with the selected prompts despite the uncertainty.
This decision does not resolve the legal interpretation of the agreement.

The [WebDevJudge paper](https://arxiv.org/html/2510.18560) reports using Gemini 2.5 Pro to filter queries from the Arena dataset.
Its [repository](https://github.com/lcy2723/WebDevJudge) says it excludes raw data and asks users to acquire it independently.
This is research precedent, not evidence of permission for this study.
The paper does not establish the authors' license arrangements.

Record any written clarification with its scope, date, and provider.
The decision to use the prompts does not establish permission to publish their source text.
