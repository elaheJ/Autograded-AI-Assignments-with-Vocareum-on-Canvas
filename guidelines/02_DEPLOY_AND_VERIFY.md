# Publish and verify a Vocareum notebook

For an instructor or assistant with authorized access to the intended course
Edition: October 14, 2026

## Outcome

Deploy the prepared assignment to the correct Vocareum part, verify the student
release, and record actual submission results. Connect an existing Canvas integration
only when requested. Use the package's WEB_AGENT_HANDOFF.txt for assignment-specific
filenames, rubric, runtime requirements, and expected test scores.

## Before starting

Identify the target course, assignment, and part from the instructor's request.
Verify access to the actual package files, not just paths on another computer.
Extract an instructor ZIP into an accessible workspace before selecting uploads.
Use supported tools and their access rules. If browser automation is unavailable,
a human instructor can perform these same steps.

Read the conversion evidence. If a solved publishing source or required answer is
missing, return the package for preparation under Handoff 1. Do not publish a blank
student preview as the instructor source or invent solutions in the platform UI.

## 1. Inspect the target and preserve existing work

Confirm the course, assignment, part, current notebook, lab type, runtime, grading
script, rubric, and whether learners have started. Preserve copies of files and
settings being replaced. Keep stable criterion IDs and platform filenames when
needed for an update. Create a new assignment or part when that is the requested
outcome. Preserve unrelated due dates, rosters, grade-release policy, and LMS links.

Publishing may replace a grading script. Establish how any custom grading behavior
will be retained before proceeding. Existing criteria may remain after publication;
reconcile the active maximum and obsolete criteria without discarding grade history.

## 2. Prepare the learner and grader environments

Use the Vocareum Notebook lab type for this native workflow. Select the required
CPU/GPU runtime and persistent dependency configuration supported by that course.
Verify imports and assets separately for learners and the grader. A successful
instructor terminal installation is not evidence of grader readiness.

For required GPU or live workloads, verify compatible libraries, storage, model
access, prior artifacts, execution limits, and the authorized resource budget.
Use approved secret management rather than notebook cells or learner files.
Inspect the current interface rather than assuming every institution has the same
menus or permissions. Report a missing capability precisely and finish unaffected
preparation where possible.

## 3. Place files by purpose and visibility

The Vocareum folder guide describes these roles:
  /voc/work         Individual development and learner workspaces
  /voc/data         Shared inputs, read-only to learners
  /voc/startercode  Starter files copied to a learner's initial workarea
  /voc/docs         Learner-facing README/instructions
  /voc/private      Instructor-only assets
  /voc/scripts      Instructor grading scripts
  /voc/course       Course-wide material available to grading scripts

Upload the solved source to the instructor's work folder through Configure
Workspace, or the equivalent control shown in the current interface. Put shared
learner inputs in data, with the exact relative subdirectories expected by the
notebook. Avoid unintended data/data nesting. Place approved instructions in docs
when used by the assignment. Use the package manifest for every destination.

Do not place answer keys, instructor source, private tests, build scripts, QA files,
or the complete package ZIP in startercode or learner data. A folder hidden in the
learner file tree can still be accessible through the terminal.

## 4. Verify cell roles and the solved source

Open the instructor notebook and compare grading roles, marker regions, answer/test
adjacency, IDs, and weights with the package rubric. Repair missing imported roles
using the supported grading interface. Preserve required setup and cell magics.
Restart the kernel and execute the solved source in order. Verify shared-data reads,
output destinations, and scored checks. Saved output is not a fresh execution.

## 5. Publish from the instructor source

Use Publish Notebook on the solved source. Inspect the dialog and select only the
intended learner files before starting publication. The workflow produces a stripped
starter notebook, creates or updates rubric criteria, and generates a grading script.
Verify the result against the manifest, including the active point total and the
requested grading-on-submission behavior. Keep manual criteria distinct.

Publication does not make an assignment available in Canvas by itself. Shared inputs
read through ../data must remain in data; a copy in startercode does not satisfy that
path. Keep optional companions separate from private source and grading assets.

## 6. Inspect what a learner actually receives

Inspect the published starter notebook and a fresh authorized test workarea.
Check editable answers, supplied setup, public checks, cell locks, paths, attachments,
and instructions. Confirm that solutions and hidden assertions are absent. Inspect
feedback for accidental exposure too. Instructor view alone is insufficient.

Starter files are copied when a learner first opens a workarea. Republishing does
not replace that learner's existing work. Prefer a fresh designated test workspace.
A platform reset permanently replaces the workarea; use it only within explicit
reset authorization and applicable tool confirmation rules. Preserve real learner
work. Updates to shared read-only inputs can affect learners immediately.

## 7. Test actual submissions

Use only the designated instructor test workspace or authorized disposable account.
Follow the package's expected scores; there is no default question count or total.
Run blank, solved, and deliberately wrong-answer cases with clean state as needed.
Test altered checks when supported. Submit each case, wait for grading, and record
criterion scores and feedback. Run All is not a submission grading test.

Report automatic points separately from pending manual review. If a case fails,
inspect available logs for missing packages/data, path mismatches, execution errors,
incorrect roles, stale release, or unsupported runtime assumptions. Fix the source
or configuration, republish when needed, and retest affected cases. Do not inflate
scores, hide a broken test, or manually award full credit to disguise a failure.

Restore the designated demonstration workspace to its intended starting state after
testing, preserving recoverable test copies. Reopen it to check for persisted answers.
Do not reset an enrolled student's workspace to achieve a clean demo.

## 8. Provide clear learner instructions

Use a descriptive heading, a short learning-purpose paragraph, a numbered launch /
complete / check / submit sequence, and a point explanation. Name the actual
published notebook and answer cells. Explain any setup, required variable names or
cell magics, public-check limits, and runtime prerequisites. Link only available
learner resources. Do not expose reference answers in an assignment description.

Suggested structure, with assignment-specific values:
  <Descriptive learning task>
  <What students practice and what they produce.>
  1. Launch the Vocareum lab from the course assignment.
  2. Complete <answer cells> in <published notebook>, editing only <allowed areas>.
  3. Run <setup and checks> in order and use feedback to revise the work.
  4. Save and Submit in Vocareum; review the score breakdown.
  <Total and criterion weights; manual grading if any; required runtime/resources.>

A visible check may cover only part of a question's points. Explain this when
additional checks are used. Use descriptive links and plain-text feedback; do not
rely only on color to communicate a result.

## 9. Connect Canvas only if requested

Use the institution's existing authorized integration. If installation or access
is missing, record the administrator prerequisite rather than inventing credentials
or changing institution-wide configuration as part of assignment setup.

Create or edit the intended Canvas assignment with matching points. Set Submission
Type to External Tool, then use Find to select the specific Vocareum assignment
through the configured integration. Preserve the mapped part and intended opening
behavior. Add the learner instructions. Save and publish within the requested scope.

For grade return, use an assignment mapping that supports it; a navigation or module
link alone is not proof of grade passback. Test the Canvas launch with the designated
test identity, submit in Vocareum, and verify that identity's score in Canvas when
available. A Canvas test-student preview may not support an external tool in the
same way as an enrolled user. If you test only an instructor preview, say so. Do not
access another learner's work to demonstrate the integration.

## 10. Report the result

Return a concise report with:
- Course, assignment, part, link, and published notebook filename.
- Files and destinations; learner/grader runtime and dependency results.
- Automatic/manual totals and preserved custom grading behavior.
- Expected and observed scores for every case actually submitted.
- Learner visibility and feedback evidence, without identifying student records.
- Optional companions and any remaining prerequisites.
- Canvas mapping, launch, and grade-return results if included in scope.
- Exact remaining work and status: PREPARED / UPLOADED / PUBLISHED /
  SUBMISSION TESTED; report CANVAS GRADE RETURN VERIFIED separately.

## Done when

The intended part has the correct published learner files, environment, rubric, and
verified actual submission grading. Any requested Canvas work has its own recorded
outcome. Distinguish incomplete platform tests from successful local checks.

## Primary references

Vocareum notebook grading and publishing:
<https://help.vocareum.com/en/articles/9341352-setting-up-grading-in-vocareum-notebook>
Vocareum folders and learner update behavior:
<https://help.vocareum.com/en/articles/9341349-navigating-the-vocareum-files-browser>
Canvas integration, assignment mapping, and grade return:
<https://help.vocareum.com/en/articles/5085436-lti-1-3-setup-guide-for-canvas>

Documentation reviewed October 14, 2026. Menu labels and institutional permissions
may differ. Verify behavior in the intended course rather than assuming it is proven.
