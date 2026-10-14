# Vocareum notebook handoffs for instructors

A portable workflow for preparing, publishing, and testing autograded notebooks
Edition: October 14, 2026

## Purpose

Turn an existing Jupyter notebook into a Vocareum Notebook assignment with clear
student instructions, reproducible grading, and verified learner files. These
handoffs work across disciplines and institutions. The instructor supplies the
learning objectives, reference answers, grading decisions, and target course.

These are plain-text instructions you can give to Claude Code, Codex, another
coding assistant, or a human collaborator. They do not depend on an assistant-specific
plugin, slash command, installed skill, instruction filename, or local directory.
An assistant still needs the capabilities and permissions required for its assigned stage. Naming an
assistant does not imply that it can control a browser or access Vocareum.

## The two stages

1. Prepare the assignment.
   Give [01_PREPARE_NOTEBOOK.md](01_PREPARE_NOTEBOOK.md) and the source files to a
   collaborator who can read and edit notebooks and run Python. The result is a
   solved instructor source, a stripped student preview, grading evidence, and an
   assignment-specific WEB_AGENT_HANDOFF.txt.

2. Publish and verify the assignment.
   Give [02_DEPLOY_AND_VERIFY.md](02_DEPLOY_AND_VERIFY.md) and that completed package to a
   collaborator with authorized instructor access to the intended Vocareum course.
   The result is a published learner notebook and tested platform submissions.
   If requested, this stage also connects and tests an existing Canvas integration.

One assistant may complete both stages when it has both sets of capabilities.
Otherwise, transfer the files and evidence between collaborators. A path on one
computer does not transfer a file to another computer or cloud session. If browser
control is unavailable, an instructor can follow Stage 2 manually.

## What to provide

Copy this intake form into your request. Fill what you know; omit irrelevant fields.

```text
Assignment title:
Audience and prerequisites:
Learning objectives:
Source notebook and reference answers:
Required learner data and permission to distribute it:
Output location or attached-file destination:
Rubric and automatic/manual point totals:
Runtime requirements, including CPU/GPU and Python/packages:
Required live services, model downloads, or prior learner artifacts:
Expected execution time and available resource budget:
New assignment or update to an existing assignment:
Vocareum course, assignment, and part identifiers or links:
Canvas course/assignment link, if connection is requested:
Authorized test account or disposable instructor test workspace:
Requested scope: prepare only / deploy and test / also connect Canvas:
```

Do not paste passwords, API keys, or student records into the intake form. Use your
institution's approved authentication and secret-management methods when needed.

## Copyable request for stage 1

```text
"Use 01_CONVERT_NOTEBOOK_TO_VOCAREUM_AUTOGRADED.txt to prepare the attached
notebook for Vocareum Notebook. Follow the completed intake form. Preserve the
original and learning objectives. Create the publishing source, student preview,
required learner files, rubric, validation evidence, and WEB_AGENT_HANDOFF.txt.
Use 03_ASSIGNMENT_HANDOFF_TEMPLATE.txt for that handoff. Report checks actually
run and any missing prerequisites. This request is for preparation only."
```

## Copyable request for stage 2

```text
"Use 02_SET_UP_NOTEBOOK_ON_VOCAREUM.txt and the package's WEB_AGENT_HANDOFF.txt
to deploy and test this assignment at the specified Vocareum destination. Preserve
unrelated settings and learner work. Use the designated test workspace. Report
actual submission results and learner visibility. Connect Canvas only if included
in my requested scope."
```

## How to use the package

Keep the four text resources together when attaching the original handoffs, or use the linked Markdown guides in this repository. Replace angle-bracket placeholders with actual
values when preparing an assignment. Follow the instructor's specific directions
and the assistant's governing tool and access rules. Read relevant local project
instructions when present; the package does not require a particular instruction
filename. Continue authorized work and ask only for information or authorization
that is genuinely missing.

The guides assume Vocareum Notebook's native notebook grading workflow, not every
Vocareum lab product. They do not assume a question count, point total, public/hidden
split, model, or cloud provider. Optional examples in the guides are illustrative.
No external example package or institution-specific course is needed.

Readiness progresses through PREPARED, UPLOADED, PUBLISHED, and SUBMISSION TESTED.
A successful local run is preparation evidence; it does not establish a successful
Vocareum deployment or a returned Canvas grade. Use precise status in every report.

## For sharing

Share this repository with instructors and collaborators. Its worked examples
intentionally contain reference solutions and grading checks for instructor use.
Distribute the generated student version when teaching an assessed activity. Keep
private course assessments, credentials, and learner records out of public uploads.
The complete instructor package is separate from student starter files.
Check rights to redistribute any source notebook, dataset, or model asset used in
an assignment. This guide does not grant rights to those separate materials.

## References and maintenance

Each stage links to primary documentation for its workflow. Documentation was
reviewed on October 14, 2026; menu labels and institutional configurations may vary.
That review is not a claim of deployment testing at every institution or with every
assistant. Recheck relevant guidance when the platform or grading tools change.
