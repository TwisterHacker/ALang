import os
from datetime import datetime

import colorama as color

from AsmGenerator.generator import CodeGen
from Lexer.lexer import Lexer
from Lib import lib
from Parser.parser import Parser
from Preprocessor.preproc import Preproceassor

steps = True

start_time = datetime.now()

strings = lib.open_file('Files/prog.a')

name = 'prog.a'

if __name__ == '__main__':
    preproc = Preproceassor()
    lexer = Lexer()
    parser = Parser()
    generator = CodeGen()
    if steps == True:
        strings = preproc.preprocessor(strings, name)
        print(color.Fore.LIGHTWHITE_EX + color.Back.GREEN + color.Style.BRIGHT + 'Preprocessing completed!' + color.Fore.RESET + color.Back.RESET)
        tokens = lexer.tokenize(strings, name)
        print(color.Fore.LIGHTWHITE_EX + color.Back.GREEN + color.Style.BRIGHT + 'Tokenization completed!' + color.Fore.RESET + color.Back.RESET)
        sl = parser.parse(tokens)
        print(color.Fore.LIGHTWHITE_EX + color.Back.GREEN + color.Style.BRIGHT + 'Parsing completed!' + color.Fore.RESET + color.Back.RESET)
        generator.generate(sl)
        print(color.Fore.LIGHTWHITE_EX + color.Back.GREEN + color.Style.BRIGHT + 'Generating code completed!' + color.Fore.RESET + color.Back.RESET)
        os.system('nasm -f win64 test.asm -o test.obj ')
        os.system('GoLink.exe test.obj')
        print(color.Fore.LIGHTWHITE_EX + color.Back.GREEN + color.Style.BRIGHT + 'Compiling ASM code completed!' + color.Fore.RESET + color.Back.RESET)
    else:
        strings = preproc.preprocessor(strings, name)
        tokens = lexer.tokenize(strings, name)
        sl = parser.parse(tokens)
        generator.generate(sl)
        os.system('nasm -f win32 out.s -o out.obj -l myfile.lst ')
        os.system('GoLink.exe out.obj')

print(datetime.now() - start_time)
