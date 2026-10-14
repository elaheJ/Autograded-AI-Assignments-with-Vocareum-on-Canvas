"""Check the package with native nbgrader. No benchmark downloads or API keys.

Run a copied version of this file from one package's qa/ directory.
"""
import copy
import contextlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from nbgrader.api import Gradebook

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'manifest.json').read_text())
NAME, ASSIGNMENT = manifest['notebook'], manifest['assignment']
nb = nbformat.read(ROOT / 'instructor' / NAME, as_version=4)
nbformat.validate(nb)
answers = [c for c in nb.cells if c.metadata.nbgrader.solution]
tests = [c for c in nb.cells if c.metadata.nbgrader.grade]
assert len(answers) == 10 and len(tests) == 20
assert sum(c.metadata.nbgrader.points for c in tests) == 100
for answer in answers:
    index = nb.cells.index(answer)
    assert all(nb.cells[j].metadata.nbgrader.grade for j in (index + 1, index + 2))
    assert answer.source.count('### BEGIN SOLUTION') == answer.source.count('### END SOLUTION') == 1

tmp = Path(tempfile.mkdtemp(prefix='tools-agents-nbgrader-qa-'))
env = os.environ.copy()
env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
env.update({'JUPYTER_CONFIG_DIR': str(tmp/'jupyter-config'),
            'JUPYTER_DATA_DIR': str(tmp/'jupyter-data'),
            'JUPYTER_RUNTIME_DIR': str(tmp/'runtime'),
            'JUPYTER_PATH': str(tmp/'share/jupyter'),
            'IPYTHONDIR': str(tmp/'ipython'), 'PYDEVD_DISABLE_FILE_VALIDATION': '1'})
os.environ.update(env)
kernel_dir = tmp/'share/jupyter/kernels/python3'
kernel_dir.mkdir(parents=True)
(kernel_dir/'kernel.json').write_text(json.dumps({
    'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
    'display_name': 'Python 3 QA', 'language': 'python'}))
work = tmp/'work'
work.mkdir()
executed = NotebookClient(copy.deepcopy(nb), timeout=90, kernel_name='python3',
                          resources={'metadata': {'path': str(work)}}).execute()
assert not any(o.output_type == 'error' for c in executed.cells if c.cell_type == 'code'
               for o in c.get('outputs', []))

# Verify teaching definitions and visible checks without a credential-dependent live cell.
teaching = nbformat.read(ROOT / manifest['teaching_notebook'], as_version=4)
nbformat.validate(teaching)
for c in teaching.cells:
    if c.cell_type == 'code':
        compile(c.source, c.id, 'exec')
        if 'live-network' in c.metadata.get('tags', []):
            c.source = 'print("Live retrieval is checked separately; no data substitute is loaded.")'
NotebookClient(teaching, timeout=90, kernel_name='python3', resources={'metadata': {'path': str(work)}}).execute()

source_dir = tmp/'source'/ASSIGNMENT
source_dir.mkdir(parents=True)
shutil.copy(ROOT/'instructor'/NAME, source_dir/NAME)
(tmp/'nbgrader_config.py').write_text(
    "c = get_config()\nc.CourseDirectory.course_id = '" + manifest['course'].lower() + "'\n"
    "c.ExecutePreprocessor.timeout = 90\nc.ExecutePreprocessor.kernel_name = 'python3'\n"
    "c.ClearSolutions.code_stub = {'python': '### YOUR CODE HERE'}\n")


def command(*args):
    result = subprocess.run([sys.executable, '-m', 'nbgrader', *args], cwd=tmp, env=env,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    label = args[-1] if args[-1] != '--force' else 'release'
    (ROOT/'qa'/f'{args[0]}-{label}.log').write_text(result.stdout)
    if result.returncode:
        raise RuntimeError(result.stdout)


command('generate_assignment', ASSIGNMENT, '--force')
release = nbformat.read(tmp/'release'/ASSIGNMENT/NAME, as_version=4)
nbformat.validate(release)
release_text = json.dumps(release)
assert '### BEGIN SOLUTION' not in release_text
assert '### BEGIN HIDDEN TESTS' not in release_text
assert sum('### YOUR CODE HERE' in c.source for c in release.cells if c.cell_type == 'code') == 10
assert all(not c.get('outputs') for c in release.cells if c.cell_type == 'code')
nbformat.write(release, ROOT/'student_preview'/NAME)


def wrong_answer(cell, replacement):
    match = re.search(r'(?m)^([ \t]*)### BEGIN SOLUTION\n', cell.source)
    assert match
    indent = match.group(1)
    pattern = r'(?ms)^' + re.escape(indent) + r'### BEGIN SOLUTION\n.*?^' + re.escape(indent) + r'### END SOLUTION'
    return re.sub(pattern, indent + replacement, cell.source, count=1)


mutants = json.loads((ROOT/'qa/mutants.json').read_text())
mutation_results = []
for n in range(1, 11):
    changed = copy.deepcopy(nb)
    c = next(c for c in changed.cells if c.metadata.nbgrader.grade_id == f'answer-{n:02d}')
    c.source = wrong_answer(c, mutants[str(n)])
    namespace, failures = {}, []
    for c in changed.cells:
        if c.cell_type != 'code':
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(c.source, namespace)
        except Exception:
            if not c.metadata.nbgrader.grade:
                raise
            failures.append(c.metadata.nbgrader.grade_id)
    expected = [f'todo-{n:02d}-basic', f'todo-{n:02d}-robustness']
    assert failures == expected, (n, failures)
    mutation_results.append({'question': n, 'incorrect_answer_rejected_by': failures,
                             'unrelated_criteria_pass': True})

for learner in ('blank', 'perfect', 'wrong05', 'tampered-tests'):
    submitted = copy.deepcopy(release)
    if learner != 'blank':
        for c in submitted.cells:
            if c.metadata.nbgrader.solution:
                master = next(a for a in answers if a.metadata.nbgrader.grade_id == c.metadata.nbgrader.grade_id)
                c.source = master.source
    if learner in ('wrong05', 'tampered-tests'):
        c = next(c for c in submitted.cells if c.metadata.nbgrader.grade_id == 'answer-05')
        c.source = wrong_answer(c, mutants['5'])
    if learner == 'tampered-tests':
        for c in submitted.cells:
            if c.metadata.nbgrader.grade:
                c.source = 'pass\n'
    folder = tmp/'submitted'/learner/ASSIGNMENT
    folder.mkdir(parents=True)
    nbformat.write(submitted, folder/NAME)
    command('autograde', ASSIGNMENT, '--student', learner)

with Gradebook('sqlite:///' + str(tmp/'gradebook.db')) as gb:
    scores = {learner: gb.find_submission(ASSIGNMENT, learner).score
              for learner in ('blank', 'perfect', 'wrong05', 'tampered-tests')}
assert scores == {'blank': 0.0, 'perfect': 100.0, 'wrong05': 90.0, 'tampered-tests': 90.0}, scores

report = {'notebook_schema_valid': True, 'answers': 10, 'test_cells': 20, 'total_points': 100,
          'completed_activity_executed_without_errors': True,
          'teaching_definition_cells_and_visible_checks_executed': True,
          'native_nbgrader_release_strips_solutions_and_hidden_tests': True,
          'native_nbgrader_scores': scores, 'mutation_checks': mutation_results,
          'live_api_and_controller': 'Not run by this validator. Optional live data and paid controller calls require separate instructor setup.',
          'vocareum_platform_status': 'Not tested by this validator; verify publication and submissions in your own course.'}
(ROOT/'qa/validation_report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'mutation_checks'}, indent=2))
