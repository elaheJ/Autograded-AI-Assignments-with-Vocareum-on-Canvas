# Arena Tools example

Students complete ten short functions that clean model names, select categories, filter vote counts, find models, rank ratings, limit a shortlist, inspect confidence intervals, validate lookup arguments, and attach source evidence.

## Files and grading

Publish from [`instructor/244_FA26_Arena_Tools_Autograded.ipynb`](instructor/244_FA26_Arena_Tools_Autograded.ipynb). The [student preview](student_preview/244_FA26_Arena_Tools_Autograded.ipynb) contains ten unfinished functions and visible checks, with no reference solutions or hidden assertions. Each question earns 4 visible and 6 additional points, for 100 total. The [rubric](instructor/rubric.json) and [manifest](manifest.json) identify the criteria.

The complete [teaching notebook](teaching/244-FA26-Arena-Tools.ipynb) is an instructor companion with worked functions and optional live practice. It contains answers, so distribute it according to your teaching plan rather than as the unfinished assessment.

## Runtime

Grading uses Python 3.10 or newer and the standard library on CPU. Leave `RUN_LIVE` and `RUN_LLM` false for submission. The optional live lookup needs network access and `requirements-live.txt`; the optional model controller additionally needs an approved provider configuration. No live call is made by the validator.

The notebook uses small software test fixtures to assess behavior. They are not stored model benchmark observations. Live ratings can change, so retain the source, publication date, and retrieval timestamp when using the classroom activity.

## Validate and deploy

Install the shared QA requirements as described in the [repository README](../../README.md), then run:

```bash
python examples/arena-tools/qa/verify_package.py
```

Expected native scores: blank 0/100, complete 100/100, wrong Q5 90/100, and wrong Q5 with altered supplied tests 90/100. Ten direct mutation checks verify that a wrong answer affects its own two criteria.

The validator executes the solved assessment and the teaching definitions/checks, regenerates the preview with nbgrader, and writes `qa/validation_report.json`. It deliberately skips live retrieval and controller calls. Vocareum and Canvas verification remain separate.

Follow [WEB_AGENT_HANDOFF.txt](WEB_AGENT_HANDOFF.txt) for a new deployment and adapt [Canvas instructions](canvas-instructions.md) for learners. See [sources and attribution](../../ATTRIBUTION.md) for the external data source.
