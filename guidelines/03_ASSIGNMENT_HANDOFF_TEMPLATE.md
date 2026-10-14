# Assignment deployment handoff template

Complete this form and save it as WEB_AGENT_HANDOFF.txt inside the assignment package.
Edition: October 14, 2026

## Assignment and scope

```text
Title:
Audience and learning objectives:
Package revision/date:
Requested outcome: new assignment / update existing assignment:
Authorized scope: deployment / publication / test submissions / Canvas connection:
Vocareum course, assignment, part, and links:
Designated disposable test identity or instructor test workspace:
Canvas destination, if requested:
Relevant existing settings or custom grading behavior to preserve:
```

## Files and destinations

Use package-relative source paths. Supply actual filenames, not placeholders.

```text
Instructor publishing source:
Required platform notebook filename:
Source -> destination -> learner-visible or instructor-only:
Student preview (inspection only; not the publishing source):
Learner data and expected relative paths:
Learner instructions:
Optional companions:
Private assets:
Manifest/checksums, if provided:
```

## Runtime

```text
Lab type:
Python/kernel:
Learner dependencies and persistent setup:
Grader dependencies and persistent setup:
CPU/GPU, memory, storage, and time limits:
Required model files, live services, or prior artifacts:
Authorized resource budget, if applicable:
Credential setup method, if required (never include actual secret values):
```

## Grading contract

```text
Answer cells and expected learner work:
Read-only setup and required cell magics:
Criterion IDs, weights, and associated answer cells:
Automatic maximum:
Manual maximum and review process:
Active total:
Obsolete criteria handling for an update:
Submission/grading behavior:
Expected blank score:
Expected solved automatic score:
Named wrong-answer cases and expected criterion losses:
Tampering test and expected outcome:
```

## Evidence from preparation

```text
Tools/versions and commands used:
Solved-source execution result:
Native release generation result:
Blank/solved/wrong/tampered observed local scores:
Learner release inspection result:
Evidence paths within qa:
Checks NOT RUN and reasons:
```

## Platform steps and remaining checks

```text
Ordered upload, environment, publication, and learner inspection steps:
Required actual Vocareum submission cases:
Feedback and visibility checks:
Intended demonstration workspace starting state:
Canvas launch and grade-return checks, if requested:
Known compatibility limits and exact remaining prerequisites:
```

## Deployment report to complete after platform work

```text
State: PREPARED / UPLOADED / PUBLISHED / SUBMISSION TESTED
Target and notebook filename:
Learner/grader environment results:
Expected vs. observed platform scores by test case:
Learner release and feedback inspection evidence:
Canvas launch result:
Canvas grade return: VERIFIED / NOT VERIFIED / NOT REQUESTED
Remaining work and required next action:
```

Report only checks actually run. Keep public sharing evidence free of credentials,
private answer keys, and identifiable learner information. A prepared package, a
published notebook, and a verified returned Canvas grade are separate outcomes.
