import colorama as color

errors_ = 0

def error( line, txt, name):
    text = f'Error in module {name} on line {line}:\t\t'
    print(
        color.Fore.LIGHTWHITE_EX + color.Back.RED + color.Style.BRIGHT + text + txt + color.Fore.RESET + color.Back.RESET )
    global errors_
    errors_ += 1

def warning( line, txt, name):
    text = f'Warning in module {name} on line {line}:\t\t'
    print(
        color.Fore.YELLOW + color.Style.DIM + text + txt + color.Fore.RESET)

def open_file(file='prog.a'):
    file1 = open(file)
    text = file1.read()
    file1.close()
    content = text.lstrip()
    strings = content.split('\n')
    return strings