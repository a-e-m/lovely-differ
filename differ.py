import argparse
import subprocess
from dataclasses import dataclass, field
from collections import Counter
from pathlib import Path
from typing import Optional

import whatthepatch

import patches

HEADER = '''[manifest]
version = "1.0.0"
dump_lua = true
priority = 0
'''

@dataclass
class Replacement:
    anchor_lines: list[str]
    new_lines: list[str] = field(default_factory=list)
    remove_old: bool = False
    before: bool = False
    start_index: Optional[int] = None

def get_previous_unique_line(commit_hash, base_path, file_path, replace_changes, new_changes, group_start):
    lines = []
    line_counts = Counter()
    file = subprocess.check_output(['git', 'show', f'{commit_hash}:{file_path}'], cwd=base_path, universal_newlines=True)
    for line in file.splitlines():
        lines.append(line.strip())
        line_counts[line.strip()] += 1

    line_index = group_start.old - 2

    # if group_start.new:
    #   line_index -= 1

    while True:
        line = lines[line_index].strip()

        replace_changes.insert(0, whatthepatch.patch.Change(None, None, line, None))
        new_changes.insert(0, whatthepatch.patch.Change(None, None, line, None))

        if line_counts[line] == 1:
            break
        line_index -= 1

def get_diffs(path_to_dir, output, commit_hash, patch_file):
    command = ['git', 'diff']
    if commit_hash:
        command.append(commit_hash)
    if patch_file:
        with open(patch_file, 'rt', encoding='utf-8') as file:
            patch = file.read()
    else:
        patch = subprocess.check_output(command, cwd=path_to_dir, universal_newlines=True)
    with open(output, 'wt', encoding='utf-8') as patch_file:
        patch_file.write(HEADER)
        for diff in whatthepatch.parse_patch(patch):
            groups = []
            current_group = []
            last_change = None
            new_file = diff.header.new_path
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

            for group in reversed(groups):
                print()
                replace_changes = []
                new_changes = []
                group_start = group[0]
                print('group_start', group_start)
                for change in group:
                    if change.old:
                        # line removed
                        replace_changes.append(change)
                    if change.new:
                        # line added
                        new_changes.append(change)

                
                for change in replace_changes:
                    print('-' + change.line, group_start == change, change.old)
                for change in new_changes:
                    print('+' + change.line, group_start == change, change.new)


                get_previous_unique_line(commit_hash, Path(path_to_dir), old_file, replace_changes, new_changes, group_start)

                patch_file.write(patches.pattern_patch(new_file, replace_changes, 'at', new_changes))

    print(f'Generated {output}')
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='LovelyDiffer',
        description='Outputs patches for Lovely based on git diffs',
    )
    parser.add_argument('git_repo_directory')
    parser.add_argument('commit_hash', nargs='?', default=None)

    parser.add_argument('-o', '--output', default='lovely.toml')
    parser.add_argument('-p', '--patch_file')

    args = parser.parse_args()
    get_diffs(args.git_repo_directory, args.output, args.commit_hash, args.patch_file)