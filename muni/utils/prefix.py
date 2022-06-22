import re


def remove_prefix(prefix: str, string: str) -> str:
    match = re.search(f'^{prefix}', string)
    if match is not None:
        return string[len(match.group()):]
    return string


def remove_postfix(postfix: str, string: str) -> str:
    match = re.search(f'{postfix}$', string)
    if match is not None:
        return string[:len(string) - len(match.group())]
    return string
