# Lovely differ

This is a Python that's meant to generate diffs for [Lovely](https://github.com/ethangreen-dev/lovely-injector). It does this by generating Lovely patches based on Git diffs

# Installation

You'll need to install [`whatthepatch`](https://pypi.org/project/whatthepatch/) using `pip` or a similar tool (I personally have been using [`uv`](https://github.com/astral-sh/uv))

# Usage
`python3 differ.py PATH_TO_GIT_DIRECTORY`. This will print the Lovely patches to stdout

# Notes

Currently this only generates patches for existing files with changes, and does not look at new files