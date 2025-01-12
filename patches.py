PATTERN_PATCH = """
[[patches]]
[patches.pattern]
target = "{}"
pattern = "{}"
position = "{}"
payload = {}
match_indent = true
times = 1
"""

SINGLE_LINE_PAYLOAD = "'{}'"

MULTI_LINE_PAYLOAD = """'''
{}
'''"""

def pattern_patch(target, pattern, position, payload):
    lines = len(payload)
    payload = '\n'.join(line.strip() for line in payload)
    if lines > 1:
        payload = MULTI_LINE_PAYLOAD.format(payload)
    else:
        payload = SINGLE_LINE_PAYLOAD.format(payload)
    return PATTERN_PATCH.format(target, pattern.strip(), position, payload)