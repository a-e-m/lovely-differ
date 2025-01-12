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
    if len(payload) > 1:
        payload = MULTI_LINE_PAYLOAD.format('\n'.join(payload))
    else:
        payload = SINGLE_LINE_PAYLOAD.format('\n'.join(payload))
    return PATTERN_PATCH.format(target, pattern, position, payload)