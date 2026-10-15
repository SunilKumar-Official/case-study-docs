# Conversation Intelligence Platform

A pipeline that turns raw support-chat transcripts into verified facts about each conversation, then uses a local language model to judge what facts cannot: whether the issue was resolved, how frustrated the customer was, and how good the service was. The model is chosen and checked by measurement, not assumption.

This folder is documentation only. There is no code, prompt, model file or conversation text here, and no names from the business the platform was built for.

Case study on the portfolio site: <https://sunilkumar-official.github.io/projects/conversation-intelligence-platform/>

## The problem

Judging the meaning of a conversation with keyword rules gives confident answers that are often wrong, which is worse than not measuring at all. Bringing in a language model fixes that and creates a new problem: which model, and how do you know you can trust it?

## What I built

- **A deterministic layer first.** Code computes every fact that can be computed: timing, turn structure, message statistics, language signals, channel and metadata. Each fact comes from a small module that is a pure function of the conversation, so it gives the same answer every time and is tested against the whole corpus.
- **An evidence object for the model.** A curated, on-demand view of those facts plus a clean transcript. It deliberately contains no judgments, because judgments are what the model produces.
- **A language-model layer.** One call per conversation to a model that runs locally, on the CPU, with no cloud API. The output is a structured record: whether the conversation and the issue were resolved, the conversation type, three 1-5 ratings (frustration, satisfaction, agent quality), a confidence score per judgment, and a short reasoning that cites the evidence.
- **An evaluation.** Model sizes benchmarked against hand-labelled ground truth, and the chosen model validated against human reviewers before it scored production data.

Headline results, as published on the portfolio site: 3,500+ production conversations scored, 200 conversations validated by humans, and 92-96.5% exact agreement with the human reviewers.

## What is in this folder

| File | What it covers |
|---|---|
| [architecture.md](architecture.md) | The layers, the rule that keeps them separate, how data moves, and why each design choice was made |
| [evaluation-method.md](evaluation-method.md) | How the three ratings are defined, how they are tied to evidence, and how the model is checked against people |

A test-suite summary will be added once its source material is reviewed.

## Scope and limits

- The platform is currently paused. What exists is a complete, evaluated pipeline from raw conversations to scored records.
- The model skews slightly positive on customer sentiment compared with human reviewers. That bias is measured and documented, not hidden.
- This is a batch job. It runs unattended and is not designed for live, per-conversation scoring.
