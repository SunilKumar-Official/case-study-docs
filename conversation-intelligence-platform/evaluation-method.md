# Evaluation method

The model's output is only useful if it can be trusted, so the evaluation is as much a part of the project as the pipeline. This document describes what the model is asked to judge, how each rating is tied to evidence, and how the model was chosen and then checked against people.

## What the model judges

For each conversation the model returns a structured record:

- whether the conversation was resolved, and whether the issue was resolved;
- the conversation type;
- three 1-5 ratings: **frustration**, **customer satisfaction** and **agent quality**;
- a **confidence score** for each judgment;
- a short **reasoning** that must cite the signals that drove the rating.

## Ratings tied to evidence

Every rating point has a written definition, and each definition is backed by observable signals from the deterministic layer, so a rating can be traced and challenged.

| Rating | 1 means | 5 means | Signals that back it |
|---|---|---|---|
| Frustration | No negative signals, polite throughout, quick resolution | Aggressive or angry tone, abandonment signals | Negative-phrase counts, customer wait times, burst sizes, a decline in politeness, an unresolved issue, no closing statement |
| Customer satisfaction | Unresolved issue, angry tone, no positive signals | Resolved cleanly, explicit thanks, positive tone, empathy from the agent | Positive-phrase counts, thanks, politeness, a closing statement, resolution, first-response time |
| Agent quality | Rude, dismissive, slow, unhelpful | Fast, empathetic, clear ownership, proactive | Agent response times, empathy, reassurance, ownership and acknowledgements, resolution, professionalism |

The same written definitions are used as anchor points when people label conversations by hand, so the model and the human reviewers are measured against the same scale. Confidence is meant to track the evidence: high when several signals agree, lower when the model is inferring from thin signals.

## Choosing the model: five axes

A model is measured on five separate axes, not one accuracy number:

1. **Accuracy** against hand-labelled examples.
2. **Output validity:** does it return well-formed, correctly typed JSON at all.
3. **Summary quality.**
4. **Run-to-run consistency:** the same conversation is analysed three times, and the question is whether it gives the same answer each time.
5. **Confidence:** how certain the model was at the exact token where it made each judgment call.

Three model sizes were evaluated against 100 hand-labelled conversations each.

**What decided the choice.** The larger of two candidate models scored higher on raw accuracy but was noticeably less consistent: rerun the same conversation and it shifted its judgment more often. Measuring its token-level confidence at each sentiment judgment showed why. It was genuinely less certain at those points, most of all when judging a customer's mood early in a conversation, before the outcome is clear. That confirmed consistency was the right thing to optimise for, so the smaller and more consistent model went to production.

## Checking it against people

Before trusting that choice, the model was validated on real production data, not only the synthetic test set used to select it. In a study of 200 conversations, human reviewers checked the model's output against their own judgment.

Results, as published on the portfolio site:

- **92-96.5%** exact agreement per judgment;
- **98%+** within one point of the human reviewer's score;
- **86%** exact agreement across every dimension checked at once.

The study also surfaced a specific, small and consistent bias: the model skews slightly positive on customer sentiment relative to human reviewers. That bias is documented rather than hidden.

## Known gaps

- A prompt-wording improvement found during evaluation was never promoted into the production run that scored the real conversations.
- Real-world latency on actual transcripts ran meaningfully higher than the synthetic benchmark predicted, because real conversations are longer than the hand-labelled test set. That matters before scaling this to a larger corpus.
- The project is paused, so none of this was extended further.
