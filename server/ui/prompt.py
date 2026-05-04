def print_colored(text, color='white'):
    colors = {
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'cyan': '36',
        'white': '37',
    }
    code = colors.get(color, '37')
    print(f"\033[{code}m{text}\033[0m")
