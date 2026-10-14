"""Validate portable references, notebooks, and manifests without network access."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    checked = 0
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(x in path.parts for x in ('.git', '.venv', '__pycache__')):
            continue
        if path.suffix not in ('.md', '.txt', '.json', '.ipynb', '.py', '.yml') or path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding='utf-8')
        assert '/Users/' not in text and '/home/' not in text, f'Personal path in {path}'
        assert 'canvas.illinoisstate.edu' not in text and 'labs.vocareum.com/main/vnav.php' not in text, f'Course-specific URL in {path}'
        if path.suffix == '.json':
            json.loads(text)
        if path.suffix == '.md':
            assert text.count('```') % 2 == 0, f'Unpaired code fence in {path}'
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if target.startswith(('https://', 'http://', '#', 'mailto:')):
                    continue
                assert (path.parent / target.split('#')[0]).exists(), f'Broken link {target} in {path}'
        checked += 1
    for example in (ROOT/'examples').iterdir():
        manifest = json.loads((example/'manifest.json').read_text())
        name = manifest['notebook']
        source = json.loads((example/'instructor'/name).read_text())
        preview = json.loads((example/'student_preview'/name).read_text())
        source_ids = [c['metadata']['nbgrader']['grade_id'] for c in source['cells']]
        assert len(source_ids) == len(set(source_ids)), example
        tests = [c for c in source['cells'] if c['metadata']['nbgrader']['grade']]
        assert sum(c['metadata']['nbgrader']['points'] for c in tests) == manifest['total_points'], example
        assert sum(c['metadata']['nbgrader']['solution'] for c in source['cells']) == manifest['questions'], example
        for notebook in (source, preview):
            assert all(not c.get('outputs') and c.get('execution_count') is None for c in notebook['cells']), example
        preview_text = json.dumps(preview)
        assert 'BEGIN SOLUTION' not in preview_text and 'BEGIN HIDDEN TESTS' not in preview_text, example
    print(f'Checked {checked} portable text resources, Markdown links, and both example manifests/previews.')

if __name__ == '__main__':
    main()
