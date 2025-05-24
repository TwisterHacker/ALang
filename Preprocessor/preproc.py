import sys

import Preprocessor.preproc
from Lib import lib


class Preproceassor():
    def preprocessor(self, strings, name):  # name : file name
        strings_new = []
        str_obj = []
        std_libs = ['string.lib', 'math.lib', 'std.lib']
        constants = []
        for i in range(len(strings)):  # lines
            strings_new.append(f'{i + 1} | {strings[i]}')

        for j in range(len(strings_new)):
            str = ' '.join(strings_new[j].split())  # current string
            words = str.split(' ')
            try:
                cmd = words[2]
                if cmd[0] == '_':
                    line = words[0].lstrip().replace('|', '').lstrip()
                    val_ = str.replace(')', '').replace(line, '').replace(';', '').lstrip().split(' ')
                    val = words[3].replace(';', '')
                    if cmd == '_include':
                        file = val.replace('"', '')
                        try:
                            strings_inc = lib.open_file(val.replace('"', ''))
                            preproc_srings = Preprocessor.preproc.Preproceassor.preprocessor(self, strings_inc, file)
                            str_obj = preproc_srings + str_obj
                            strings_new[j] = ''
                        except FileNotFoundError:
                            if file in std_libs:
                                strings_inc = lib.open_file('std_lib/' + file)
                                preproc_srings = Preprocessor.preproc.Preproceassor.preprocessor(self, strings_inc, file)
                                str_obj = preproc_srings + str_obj
                                strings_new[j] = ''
                            else:
                                lib.error(line, f'File {file} not found', name)
                        except RecursionError:
                            pass


                    if cmd == '_define':
                        try:
                            constants.append((val_[2], val_[3]))
                            strings_new[j] = ''
                        except IndexError:
                            lib.error(line, 'Syntax error', name)

                if cmd[0] == '@':  # comment
                    strings_new[j] = ''

            except IndexError:
                pass
        if lib.errors_ == 0:
            str_obj = str_obj + strings_new
            return str_obj
        else:
            sys.exit()
