"""Synthetic nbgrader release/scoring checks; no learner or platform access."""
import contextlib
from datetime import date
import copy
import importlib.metadata
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from nbgrader.api import Gradebook
from IPython.utils.capture import CapturedIO

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'manifest.json').read_text())
NAME, ASSIGNMENT = MANIFEST['notebook'], MANIFEST['assignment']
MASTER = nbformat.read(ROOT / 'instructor' / NAME, as_version=4)


def grade_locally(notebook):
    namespace, scores = {}, {}
    for cell in notebook.cells:
        if cell.cell_type != 'code':
            continue
        meta = cell.metadata.nbgrader
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                if cell.source.startswith('%%capture '):
                    first, body = cell.source.split('\n', 1)
                    output, errors = io.StringIO(), io.StringIO()
                    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                        exec(body, namespace)
                    namespace[first.split()[1]] = CapturedIO(output, errors)
                else:
                    exec(cell.source, namespace)
            passed = True
        except Exception:
            passed = False
        if meta.grade:
            scores[meta.grade_id] = meta.points if passed and cell.source.strip() else 0
    return scores


def replace_answer(notebook, question, source):
    next(c for c in notebook.cells if c.metadata.nbgrader.grade_id == f'q{question}-answer').source = source


def main():
    nbformat.validate(MASTER)
    ids = [c.metadata.nbgrader.grade_id for c in MASTER.cells]
    assert len(ids) == len(set(ids))
    answers = [c for c in MASTER.cells if c.metadata.nbgrader.solution]
    tests = [c for c in MASTER.cells if c.metadata.nbgrader.grade]
    assert len(answers) == 4 and len(tests) == 8
    assert sum(c.metadata.nbgrader.points for c in tests) == 100
    assert all(not c.get('outputs') and c.get('execution_count') is None for c in MASTER.cells)
    for answer in answers:
        index = MASTER.cells.index(answer)
        assert MASTER.cells[index + 1].metadata.nbgrader.points == 10
        assert MASTER.cells[index + 2].metadata.nbgrader.points == 15
        assert answer.source.count('### BEGIN SOLUTION') == answer.source.count('### END SOLUTION') == 1
        stripped = re.sub(r'(?ms)^([ \t]*)### BEGIN SOLUTION.*?^[ \t]*### END SOLUTION', r'\1### YOUR CODE HERE', answer.source)
        if stripped.startswith('%%capture '):
            stripped = stripped.split('\n', 1)[1]
        compile(stripped, 'vocareum-comment-only-blank', 'exec')
        assert 'def ' not in answer.source
    assert sum(grade_locally(MASTER).values()) == 100

    # Each wrong answer loses exactly its own 25 points.
    mutation_scores = {}
    for q, source in enumerate(('bnb_config = {}', 'lora_settings = {}',
                                '%%capture layer_output\npass', '%%capture size_output\npass'), 1):
        mutated = copy.deepcopy(MASTER)
        replace_answer(mutated, q, source + '\n')
        scores = grade_locally(mutated)
        assert sum(scores.values()) == 75, (q, scores)
        assert scores[f'q{q}-basic'] == scores[f'q{q}-additional'] == 0
        mutation_scores[f'wrong_q{q}'] = 75

    # Plausible mistakes that pass the example still lose hidden credit.
    mistakes = {
        'q1_wrong_quant_type': (1, 'bnb_config = {"load_in_4bit": True, "bnb_4bit_quant_type": "fp4", "bnb_4bit_use_double_quant": True}\n'),
        'q1_missing_double_quant': (1, 'bnb_config = {"load_in_4bit": True, "bnb_4bit_quant_type": "nf4"}\n'),
        'q1_integer_boolean': (1, 'bnb_config = {"load_in_4bit": True, "bnb_4bit_quant_type": "nf4", "bnb_4bit_use_double_quant": 1}\n'),
        'q2_wrong_alpha': (2, 'lora_settings = {"r": 8, "lora_alpha": 8, "lora_dropout": 0.05}\n'),
        'q2_missing_dropout': (2, 'lora_settings = {"r": 8, "lora_alpha": 16}\n'),
        'q3_incomplete_layout': (3, '%%capture layer_output\nprint("DemoModel(\\n  qkv_proj: Linear(8, 24)\\n  o_proj: Linear(8, 8)\\n)")\n'),
        'q4_hardcoded_counts': (4, '%%capture size_output\ntotal_parameters = 120\ntrainable_parameters = 20\nprint("Total parameters: 120\\nTrainable parameters: 20")\n'),
        'q4_only_first_trainable': (4, '%%capture size_output\ntotal_parameters = sum(p.numel() for p in model.parameters())\ntrainable_parameters = next((p.numel() for p in model.parameters() if p.requires_grad), 0)\nprint(f"Total parameters: {total_parameters}")\nprint(f"Trainable parameters: {trainable_parameters}")\n'),
        'q4_counts_parameters_instead_of_elements': (4, '%%capture size_output\ntotal_parameters = len(list(model.parameters()))\ntrainable_parameters = sum(p.requires_grad for p in model.parameters())\nprint(f"Total parameters: {total_parameters}")\nprint(f"Trainable parameters: {trainable_parameters}")\n'),
    }
    for label, (q, source) in mistakes.items():
        mutated = copy.deepcopy(MASTER)
        replace_answer(mutated, q, source)
        scores = grade_locally(mutated)
        assert scores[f'q{q}-basic'] == 10 and scores[f'q{q}-additional'] == 0
        assert sum(scores.values()) == 85, (label, scores)
        mutation_scores[label] = 85

    with tempfile.TemporaryDirectory(prefix='qlora-demo-nbgrader-') as directory:
        work = Path(directory)
        env = os.environ.copy()
        env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
        for variable, folder in [('JUPYTER_CONFIG_DIR', 'config'), ('JUPYTER_DATA_DIR', 'data'),
                                 ('JUPYTER_RUNTIME_DIR', 'runtime'), ('IPYTHONDIR', 'ipython')]:
            env[variable] = str(work / folder)
        env['JUPYTER_PATH'] = str(work / 'share/jupyter')
        env['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
        os.environ.update(env)
        kernel = work / 'share/jupyter/kernels/python3'
        kernel.mkdir(parents=True)
        (kernel / 'kernel.json').write_text(json.dumps({'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'], 'display_name': 'QLoRA Demo QA', 'language': 'python'}))
        executed = NotebookClient(copy.deepcopy(MASTER), timeout=90, kernel_name='python3', resources={'metadata': {'path': str(work)}}).execute()
        assert not any(o.output_type == 'error' for c in executed.cells if c.cell_type == 'code' for o in c.outputs)
        source_dir = work / 'source' / ASSIGNMENT
        source_dir.mkdir(parents=True)
        nbformat.write(MASTER, source_dir / NAME)
        (work / 'nbgrader_config.py').write_text("c = get_config()\nc.CourseDirectory.course_id = 'it344'\nc.ExecutePreprocessor.timeout = 90\nc.ExecutePreprocessor.kernel_name = 'python3'\nc.ClearSolutions.code_stub = {'python': '### YOUR CODE HERE'}\n")

        def run(label, *args):
            result = subprocess.run([sys.executable, '-m', 'nbgrader', *args], cwd=work, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
            (ROOT / 'qa' / f'{label}.log').write_text(result.stdout)
            if result.returncode:
                raise RuntimeError(result.stdout)

        run('generate_assignment', 'generate_assignment', ASSIGNMENT, '--force')
        release = nbformat.read(work / 'release' / ASSIGNMENT / NAME, as_version=4)
        nbformat.validate(release)
        for cell in release.cells:
            assert 'BEGIN SOLUTION' not in cell.source and 'BEGIN HIDDEN TESTS' not in cell.source
            assert not cell.get('outputs') and cell.get('execution_count') is None
            if cell.metadata.nbgrader.solution:
                assert 'YOUR CODE HERE' in cell.source and 'def ' not in cell.source
            if cell.metadata.nbgrader.grade_id.endswith('-additional'):
                assert not cell.source.strip()
        assert sum(grade_locally(release).values()) == 0
        nbformat.write(release, ROOT / 'student_preview' / NAME)
        nbformat.write(release, ROOT / NAME)
        perfect = copy.deepcopy(release)
        master_answers = {c.metadata.nbgrader.grade_id: c.source for c in answers}
        for cell in perfect.cells:
            if cell.metadata.nbgrader.solution:
                cell.source = master_answers[cell.metadata.nbgrader.grade_id]
        wrong = copy.deepcopy(perfect)
        replace_answer(wrong, 4, '%%capture size_output\npass\n')
        tampered_wrong = copy.deepcopy(wrong)
        tampered_blank = copy.deepcopy(release)
        for notebook in (tampered_wrong, tampered_blank):
            for cell in notebook.cells:
                if cell.metadata.nbgrader.grade:
                    cell.source = 'assert True\n'
        hardcoded = copy.deepcopy(perfect)
        replace_answer(hardcoded, 4, mistakes['q4_hardcoded_counts'][1])
        cases = {'blank': (release, 0), 'perfect': (perfect, 100), 'wrong_q4': (wrong, 75),
                 'tampered_wrong_q4': (tampered_wrong, 75), 'tampered_blank': (tampered_blank, 0),
                 'hardcoded_q4': (hardcoded, 85)}
        actual_scores = {}
        for learner, (notebook, expected) in cases.items():
            submitted = work / 'submitted' / learner / ASSIGNMENT
            submitted.mkdir(parents=True)
            nbformat.write(notebook, submitted / NAME)
            run(f'autograde-{learner}', 'autograde', ASSIGNMENT, '--student', learner)
            with Gradebook('sqlite:///' + str(work / 'gradebook.db')) as gradebook:
                score = gradebook.find_submission(ASSIGNMENT, learner).score
            assert score == expected, (learner, score, expected)
            actual_scores[learner] = score
            print(f'{learner}: {score}/100', flush=True)
    report = dict(status='passed', date=date.today().isoformat(), python=sys.version.split()[0],
                  nbgrader=importlib.metadata.version('nbgrader'), questions=4,
                  graded_criteria=8, points=100, completed_notebook_executed=True,
                  student_preview_generated_by='nbgrader generate_assignment',
                  solutions_and_hidden_tests_stripped=True, comment_only_blanks_compile=True,
                  answer_style='ordinary notebook code blocks; no student-defined functions',
                  native_nbgrader_scores=actual_scores, mutation_scores=mutation_scores,
                  actual_vocareum_submission_tested=False)
    (ROOT / 'qa/validation_report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Release stripping, grading independence, hidden checks, and test restoration passed.')


if __name__ == '__main__':
    main()
