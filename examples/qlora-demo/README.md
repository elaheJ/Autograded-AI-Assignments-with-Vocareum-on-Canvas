# QLoRA four-question demo

A short CPU activity for a Canvas-to-Vocareum round trip. Students complete ordinary notebook code blocks: a quantization dictionary, an adapter dictionary, a statement that prints the supplied model, and calculations that print total and trainable parameter counts.

The supplied tiny model is a Python stand-in. This activity does not load a language model, instantiate BitsAndBytes or PEFT, train adapters, or require a GPU. It isolates configuration and inspection skills from expensive model execution.

## Files and grading

Publish from [`instructor/344-fa26-qlora-demo-activity.ipynb`](instructor/344-fa26-qlora-demo-activity.ipynb). Inspect the [student preview](student_preview/344-fa26-qlora-demo-activity.ipynb) and keep the provided `%%capture` lines in Q3 and Q4. Students do not define functions.

Each question earns 10 visible and 15 additional points, for 100 total. Passing a visible check does not establish full credit. The [rubric](instructor/rubric.json) and [manifest](manifest.json) document the eight active criteria.

The original live course used a legacy filename, `344_FA26_QLoRA_Design_Autograded.ipynb`. This repository uses the explicit four-question filename above for new deployments. Preserve an existing platform filename and reconcile obsolete criteria when updating a previously deployed assignment.

## Validate and deploy

Install the shared QA requirements from the [repository README](../../README.md), then run:

```bash
python examples/qlora-demo/qa/verify_package.py
```

Expected native scores:

| Synthetic submission | Score |
| --- | --- |
| Blank | 0/100 |
| Complete | 100/100 |
| Q4 unfinished, other answers complete | 75/100 |
| Q4 with incorrect hard-coded counts but correct labels | 85/100 |
| Blank with altered supplied tests | 0/100 |
| Q4 unfinished with altered supplied tests | 75/100 |

Additional mutation checks cover incorrect settings, missing fields, incomplete layer output, and incorrect count methods. The validator executes the solved notebook, generates the student release, and records `qa/validation_report.json`. No platform access is used.

Follow [WEB_AGENT_HANDOFF.txt](WEB_AGENT_HANDOFF.txt) and adapt [Canvas instructions](canvas-instructions.md). For a short demonstration, start with a blank designated test workspace, run setup, complete one question, check it, and submit. One fully correct answer with the other three blank should earn 25/100; verify that case in your own course before a live demo.
