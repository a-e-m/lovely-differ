PATTERN_PATCH = """
[[patches]]
[patches.pattern]
target = "{}"
pattern = {}
position = "{}"
payload = {}
match_indent = true
times = 1
"""

SINGLE_LINE_PAYLOAD = "'''{}'''"

MULTI_LINE_PAYLOAD = """'''
{}
'''"""

def get_formatted_code(code):
    lines = len(code)
    code = '\n'.join(line.line for line in code)
    if lines > 1:
        return MULTI_LINE_PAYLOAD.format(code)
    else:
        return SINGLE_LINE_PAYLOAD.format(code)

def pattern_patch(target, pattern, position, payload):
    return PATTERN_PATCH.format(target, get_formatted_code(pattern), position, get_formatted_code(payload))