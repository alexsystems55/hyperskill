def rec_match(pattern: str, input_string: str) -> bool:
    """
    Recursive function to find the matching pattern
    """
    # Pattern is over
    if not pattern:
        return True
    # Input string is over
    if not input_string:
        return pattern == "$"
    # Escape character processing
    if pattern[0] == "\\":
        if pattern[1] == input_string[0]:
            return rec_match(pattern[2:], input_string[1:])
        return False
    # ? meta character
    if pattern.find("?") == 1:
        if pattern[0] == input_string[0] or pattern[0] == ".":
            return rec_match(pattern[2:], input_string[1:])
        else:
            return rec_match(pattern[2:], input_string)
    # * meta character
    if pattern.find("*") == 1:
        if pattern[0] == input_string[0]:
            return rec_match(pattern, input_string[1:])
        elif pattern[0] == ".":
            shift = input_string.count(input_string[0])
            return rec_match(pattern[2:], input_string[shift:])
        else:
            return rec_match(pattern[2:], input_string)
    # + meta character
    if pattern.find("+") == 1:
        if pattern[0] == input_string[0]:
            return rec_match(pattern.replace("+", "*", 1), input_string[1:])
        elif pattern[0] == ".":
            shift = input_string.count(input_string[0])
            return rec_match(pattern[2:], input_string[shift:])
        else:
            return rec_match(pattern[0] + pattern[2:], input_string)
    # regular characters
    if pattern[0] == input_string[0] or pattern[0] == ".":
        return rec_match(pattern[1:], input_string[1:])
    return False


def search(pattern: str, input_string: str) -> bool:
    """
    Searching for a pattern in the input_string and call recursive function when needed
    """
    # No pattern to match
    if not pattern:
        return True
    # Match at the beginning
    if pattern.startswith("^"):
        return rec_match(pattern[1:], input_string)
    # Search in longer input_string
    for shift in range(len(input_str)):
        if rec_match(pattern, input_string[shift:]):
            return True
    # Nothing matched
    return False


# Main
regex, input_str = input().split("|")
print(search(regex, input_str))
