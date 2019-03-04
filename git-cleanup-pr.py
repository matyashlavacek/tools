#!/usr/bin/env python3
"""
Use this script after merging branch in git.
This script gets name of current branch and if it is other branch than main,
it will checkout master, pull latest changes and deletes the branch you
were previously on.

For convenience set alias in bash profile, e.g.:
alias gg='python3 ~/tools/git-cleanup-pr.py'
"""
import collections
import subprocess
import sys

Result = collections.namedtuple('Result', ['rc', 'stdout', 'stderr'])


def git(cmd):
    cmd = f'git -c color.ui=always {cmd}'
    args = cmd.split(' ')
    process = subprocess.run(
        args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return Result(
        process.returncode, process.stdout.decode().strip(),
        process.stderr.decode().strip())


def main():
    git_branch_result = git('branch')
    if git_branch_result.rc != 0:
        print(git_branch_result.stderr)
        return 1
    main_branch_result = git('symbolic-ref refs/remotes/origin/HEAD')
    main_branch = main_branch_result.stdout.split('/').pop()
    branches = git_branch_result.stdout.replace(' ', '').split('\n')
    current_branch = None
    for branch in branches:
        if branch.startswith('*'):
            current_branch = branch[1:]
            if current_branch == main_branch:
                print(f'Already on `{main_branch}`. Pulling.')
                print(git('pull').stdout)
                return 0
            print(f'Now on `{current_branch}`')
    print(git(f'checkout {main_branch}').stdout)
    print(git('pull').stdout)
    print(git(f'branch -d {current_branch}').stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
