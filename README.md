# Autograded AI Assignments with Vocareum on Canvas

Reusable instructor guidelines and two worked examples for preparing Jupyter notebooks, publishing them as autograded Vocareum assignments, and connecting them to Canvas.

The workflow is agent-agnostic. Give the instructions to Claude Code, Codex, another coding assistant, or a human collaborator with the required file, Python, and authorized platform access. The guides are ordinary Markdown and text files; no skill installation is required.

## Start here

1. Read the [starting guide and intake form](guidelines/START_HERE.md).
2. Use [Prepare a notebook](guidelines/01_PREPARE_NOTEBOOK.md) to create the solved publishing source, student preview, rubric, and validation evidence.
3. Complete the [assignment handoff template](guidelines/03_ASSIGNMENT_HANDOFF_TEMPLATE.md).
4. Follow [Deploy and verify](guidelines/02_DEPLOY_AND_VERIFY.md) in your own Vocareum course. Connect the intended Canvas assignment when requested.

The [plain-text resources](resources/text/) contain the same guidelines in a format you can attach or paste directly into an assistant. [Contributor guidance](CONTRIBUTING.md) explains how to keep the formats aligned.

## Worked examples

| Example | What students practice | Grading | Execution |
| --- | --- | --- | --- |
| [Arena Tools](examples/arena-tools/README.md) | Ten short Python functions for cleaning, filtering, ranking, and reporting model-rating evidence | 10 questions; 4 visible + 6 additional points each; 100 total | CPU; offline grading; optional live Arena data and optional model tool calling |
| [QLoRA four-question demo](examples/qlora-demo/README.md) | Quantization and adapter dictionaries, model inspection, and computed parameter counts | 4 questions; 10 visible + 15 additional points each; 100 total | CPU; tiny supplied model; no training, GPU, download, or API key |

These examples illustrate two answer styles: small functions and ordinary notebook code blocks. Their question counts and grading weights are examples, not defaults for other assignments. The QLoRA activity records configuration values; it does not perform QLoRA fine-tuning.

## Which files to use

Each example includes:

- `instructor/`: the solved notebook used to publish and generate grading artifacts, plus its rubric.
- `student_preview/`: the stripped learner notebook for inspection and distribution; never use it as the instructor publishing source.
- `manifest.json`: exact filenames, criteria, weights, and runtime requirements.
- `WEB_AGENT_HANDOFF.txt`: deployment instructions for a new course.
- `canvas-instructions.md`: learner-facing text to adapt into your Canvas assignment.
- `qa/verify_package.py`: reproducible checks using native nbgrader, synthetic submissions, and no enrolled learner records.
- `requirements-qa.txt`: dependencies for authoring and local validation, separate from the notebook's minimal grading requirements.

**The instructor examples contain solutions and private grading checks.** Publish from the instructor source and distribute the generated learner version through Vocareum. The complete repository is an instructor resource, so it is unsuitable as student startercode.

## Run the local checks

Use Python 3.11 or 3.12 in an isolated environment. From the repository root on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r examples/qlora-demo/requirements-qa.txt
python examples/arena-tools/qa/verify_package.py
python examples/qlora-demo/qa/verify_package.py
python scripts/check_repository.py
```

Both examples use the same pinned QA dependencies. On Windows, create the environment with `py -3 -m venv .venv`, then activate it with `.venv\Scripts\Activate.ps1` in PowerShell. Run the remaining `python` commands unchanged.

The validators execute solved notebooks, generate student releases, and check blank, complete, wrong-answer, and altered-test cases. Arena also checks all ten deliberately incorrect answers. QLoRA checks partial-credit cases that pass visible checks but fail additional checks. Generated logs stay local and are ignored by Git.

The [GitHub Actions workflow](.github/workflows/validate.yml) runs both example validators and the repository checks. Local results are recorded in each example's `qa/validation_report.json`; the CI result is recorded on the Actions tab.

## Publish in Vocareum and connect Canvas

Use [Deploy and verify](guidelines/02_DEPLOY_AND_VERIFY.md) and the selected example's handoff. Supply your own course and part identifiers. The examples include no institution-specific links, sign-in details, or learner records.

Upload the solved notebook to the instructor work area, then use **Publish Notebook** to generate the learner files and grading artifacts. Check the active rubric total and actual test submissions. In Canvas, use the institution's configured Vocareum integration and an **External Tool** assignment mapping, with matching points. Test launch and grade return with an authorized test identity.

Local nbgrader success does not establish successful Vocareum publication or Canvas grade return. Report those results separately. Existing learner work can persist after republishing; use a designated test workspace when checking a clean student release.

## Sources and licensing

The guidelines and example code are licensed under [MIT](LICENSE), as authorized by the repository owner. See [attribution](ATTRIBUTION.md) for platform documentation, the Arena data source, and QLoRA background. External documentation, datasets, models, and dependencies retain their own terms. No model-rating dataset snapshot or pretrained model weights are distributed here.

The examples retain their original course labels and notebook filenames for traceability. Adapt titles, learning objectives, runtime requirements, and rubrics for your own audience.
