# Catalog quality and metadata

The catalog is a deterministic map of one practitioner's public stars and original projects. Classification is a discovery aid, not an endorsement or a guarantee of project quality. Community suggestions have a separate [review record](community-reviews.md).

## Classification evidence

`config.toml` defines the taxonomy and weights: strong topics score 3, weak topics 1, name keywords 2 and description keywords 1. Existing caps limit keyword contributions. The highest score wins; ties follow category order. A zero score everywhere goes to `triage`. Manual overrides take precedence.

Every repository in `data/repos.json` includes this additive `classification` object:

| Field | Meaning |
| --- | --- |
| `method` | `rules`, `override` or `unmatched` |
| `review_needed` | Whether any review reason applies |
| `reasons` | Array of the codes below, in the listed order when both rule reasons apply |
| `score` | Integer rule score of the selected category |
| `runner_up` | Best positive-scoring other category, or `null`; ties follow taxonomy order |
| `runner_up_score` | Integer score of that category, or 0 |
| `margin` | Selected category's score minus the runner-up score |

For rules, `low_score` means the winning score is below `review_min_score` (default 3); `close_scores` means another category has a positive score and the margin is below `review_min_margin` (default 2). Thresholds are non-negative integers in `[scoring]`; older configurations use the defaults. Exact threshold equality does not trigger review. Flags preserve the winning category.

An unmatched project has only `unmatched`. An override is a trusted curator decision and has no rule-based review reasons. An override to `triage` has `manual_triage`, including a deliberate hold outside the GenAI taxonomy. An override can have a zero score or negative margin because its category was chosen manually. Scores and margins are heuristic evidence, **not calibrated probabilities**.

Existing `category`, `tags`, `score`, `key_topics` and `classified_by` fields remain available. The older `classified_by` value `none` corresponds to the new `method: unmatched`. README rows visibly flag review cases, and its summary counts all projects needing review. Missing new metadata in older datasets means unassessed, not a trusted classification.

Paperless-ngx is manually categorized as `automation`: its purpose is document management and productivity. Its `machine-learning` and `ocr` topics otherwise tie in unrelated primary categories. AzuraCast is held in `triage`: a radio management suite's description mentioning a web app does not establish a GenAI role.

## Project stage and maintenance

Every repository has `maturity: {stage, source, note}`. The default is `{"stage":"unknown","source":null,"note":""}`. `unknown` means unassessed. Supported stages are `unknown`, `experimental`, `alpha`, `beta` and `stable`. Stage is never inferred from stars, push age, version numbers or descriptive marketing terms.

To annotate a stage, add an explicit upstream source in `config.toml`:

```toml
[maturity."owner/project"]
stage = "beta"
source = "https://github.com/owner/project/blob/commit/README.md"
note = "Upstream labels this release beta."
```

Each non-unknown stage requires a valid HTTPS source; notes are strings. Prefer a commit-pinned document or version-specific release. Describe the source's scope: the two current `stable` annotations refer to stable release channels in [Paperless documentation](https://github.com/paperless-ngx/paperless-ngx/blob/138160cbda97796ffbc8c7048139c728210c020d/docs/administration.md) and [AzuraCast documentation](https://www.azuracast.com/docs/getting-started/updates/release-channels/), not every development or rolling build. These annotations are not security audits or production guarantees.

`health` remains independent: `active` is a push within 90 days; `maintained` is within 365 days; `dormant` is older. Archived repositories are `archived` regardless of push age, and a missing push date is `unknown`. Language and license come from GitHub metadata; a missing value stays empty. Neither missing metadata nor a recent push establishes project maturity.

Curated stage annotations and classification overrides belong to the configured catalog. Adaptation to a different repository clears both, including copies under the same owner; an exact case-insensitive configured repository match preserves them.

## Reproducibility

`scripts/build.py` owns README and JSON generation. Change the generator or configuration rather than editing generated rows. `tests/fixture.json` contains raw GitHub-shaped input for isolated builds. `tests/classification_reference.json` adds actual Paperless/AzuraCast metadata and strong, weak, tied, absent and exact-threshold signals; `tests/test_build.py` retains the original 20 reference classifications and checks the metadata contracts, validation and fork behavior.

A presentation-only rebuild of a normalized cache must preserve `generated_at`, repository statistics, momentum, project membership and the bytes of `data/history.json`. It is not a fresh GitHub fetch. Use raw GitHub payloads with `--fixture`; an existing normalized `data/repos.json` is not a fixture. Read and write all generated text explicitly as UTF-8.
