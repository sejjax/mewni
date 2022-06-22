import re
from .prefix import remove_prefix


def multiline(string: str):
    """
    Remove formatting lines and remove new lines from left and right
    :param string:
    :return:
    """
    string = string.rstrip()
    string = string.lstrip('\n')
    match = re.search('^ +', string)
    lines = string.split('\n')

    indent = 0
    if match is not None:
        indent = len(match.group())

    lines = list(map(lambda line: remove_prefix(' ' * indent, line), lines))
    return '\n'.join(lines)