import sys

from Lib import lib


class CodeGen:
    main = False
    def generate(self, sl):
        out = open('out.s', 'w')
        types = ['int', 'str', 'float']
        constants = []

        for i in range(len(sl)):
            cmd = str(sl[i]).replace('(', '')

            if cmd == 'return':
                if isinstance(sl[i + 1], dict):
                    keys = sl[i + 1].keys()
                    tok = list(keys)[0].split(' ')[0]
                    out.write(f'mov eax, {sl[i + 1][tok]}\n')
                else:
                    print(type(sl[i + 1]))
            elif cmd == 'byte':
                if isinstance(sl[i + 1], dict):
                    keys = sl[i + 1].keys()
                    tok = list(keys)[0].split(' ')[0]
                    out.write(f'db {sl[i + 1][tok]}\n')
                else:
                    print(type(sl[i + 1]))
            elif isinstance(sl[i], dict):
                cmd = sl[i]
                keys = sl[i].keys()
                tok = list(keys)[0].split(' ')[0]
                val = cmd[tok]
                if tok == 'user_func':
                    if val != 'Main':
                        out.write(f'%macro {val} 0\n')
                    else:
                        out.write("    global _main\n"
                                         "extern  _GetStdHandle@4\n"
                                         "extern  _WriteFile@20\n"
                                         "extern  _ExitProcess@4\n"
                                         "section .text\n"
                                         "_main:"
                                  )
                        self.main = True
                elif tok == '_int':
                    out.write(f'{val[0]} db {val[1]} \n')
                elif tok in types:
                    pass
                else:
                    #out.write('_start:\n')
                    pass
            else:
                if cmd[0] == '_':
                    out.write(cmd.replace('_', '').replace('(', '') + '\n')
                if cmd == 'stop_usr_fun' and self.main != True:
                    out.write('%endmacro\n')

        if lib.errors_ == 0:
            return
        else:
            sys.exit()
