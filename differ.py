import argparse
import subprocess
from dataclasses import dataclass, field

import whatthepatch

import patches

HEADER = '''[manifest]
version = "1.0.0"
dump_lua = true
priority = 0
'''

@dataclass
class Replacement:
    old_line: str
    new_lines: list[str] = field(default_factory=list)
    remove_old: bool = False

def get_diffs(path_to_dir, output):
    patch = subprocess.check_output(['git', 'diff'], cwd=path_to_dir, universal_newlines=True)
    for diff in whatthepatch.parse_patch(patch):
        groups = []
        current_group = []
        last_change = None
        old_file = diff.header.old_path

        for change in diff.changes:
            if not change.line.strip():
                continue
            if not change.new:
                # line deleted
                current_group.append(change)
            elif not change.old:
                # line added or replaced
                if not current_group and last_change:
                    current_group.append(last_change)
                current_group.append(change)
            else:
                if current_group:
                    groups.append(current_group)
                current_group = []
            last_change = change
        if current_group:
            groups.append(current_group)

        with open(output, 'wt', encoding='utf-8') as patch_file:
            patch_file.write(HEADER)
            for group in groups:
                replacements = []
                current_replacement = None
                for change in group:
                    if change.old:
                        if current_replacement:
                            replacements.append(current_replacement)
                        current_replacement = Replacement(change.line, remove_old=not change.new)
                    if not change.old:
                        current_replacement.new_lines.append(change.line)
                if current_replacement:
                    replacements.append(current_replacement)
                
                for replacement in replacements:
                    position = 'at' if replacement.remove_old else 'after'
                    
                    patch_file.write(patches.pattern_patch(old_file, replacement.old_line, position, replacement.new_lines))
        print(f'Generated {output}')
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='LovelyDiffer',
        description='Outputs patches for Lovely based on git diffs',
    )
    parser.add_argument('git_repo_directory')
    parser.add_argument('-o', '--output', default='lovely.toml')
    args = parser.parse_args()
    get_diffs(args.git_repo_directory, args.output)