import re
import sys

from Lib import lib

commands = ['module', 'log', 'return', 'byte']
types = ['_int', '_str', '_float', '_bool', 'func', 'const']


class Lexer():
    def tokenize(self, strings, name):
        name = ''
        variables = {}
        reserved_variables = ['__MainModule__']
        tokens = []
        token_list = {
            '/': 'div',
            '*': 'mul',
            '+': 'plus',
            '-': 'min',
            ';': 'new_line',
            '(': 'open_bracket',
            ')': 'closed_bracket',
            ',': 'comma',
            'if': 'IF',
            'else': 'ELSE',
            'elif': 'ELSE_IF',
            'while': 'WHILE',
            '{': 'cur_open_bracket',
            '}': 'cur_closed_bracket',

        }
        for i in range(len(strings)):
            str = strings[i].lstrip().replace('(', ' ( ').replace(')', ' ) ').lstrip().replace(';', ' ; ').replace(',',
                                                                                                                   ' , ').replace(
                'if', ' if ').replace('elif', ' elif ').replace('else', ' else ').replace('while', ' while ').replace(
                'for', ' for ')
            str = re.sub(r'\s+', ' ', str)
            words = str.split(' ')
            line = words[0]
            if str != line + ' | ' and str != '':
                cmd = str.replace(line + ' | ', '').replace('(', ' ( ').split(' ')[0]
                if len(re.findall(cmd, str)) > 1:
                    lib.error(line, f'You cannot use a function "{cmd}" inside function "{cmd}"', name)
                value = str.replace(line + ' | ', '').replace(cmd, '').replace('+', ' + ').replace('-', ' - ').replace(
                    '*', ' * ').replace('/', ' / ')
                val = re.sub(r'\s+', ' ', value).split(' ')
                if cmd in commands:
                    if cmd == 'module':
                        if val[2][0] == '"' and val[2][-1] == '"':
                            name = val[2]
                        elif val[2] in reserved_variables and val[2] == '__MainModule__':
                            name = 'main'
                        else:
                            lib.warning(line, 'undefined module name!', '"undefined"')
                            name = '"undefined"'
                    else:
                        tokens.append({'func ' + line + ' ' + name: cmd})
                        for j in range(len(val)):
                            if val[j] in token_list.keys():
                                tokens.append({token_list[val[j]] + ' ' + line + ' ' + name: val[j]})
                            elif not re.search('[a-zA-Z]', val[j]) and not re.search('[/*+]', val[j]) and val[
                                j] != '' and val[j] != ',':  # number
                                if float(val[j]) % 1 != 0:  # float
                                    tokens.append({'float ' + line + ' ' + name: val[j]})

                                else:
                                    tokens.append({'int ' + line + ' ' + name: val[j]})  # integer

                            elif val[j] != '' and val[j][0] == '"' and val[j][-1] == '"':  # string
                                tokens.append({'str ' + line + ' ' + name: val[j].replace('^', ' ').replace('`', ',')})

                            elif re.search('[a-zA-Z]', val[j]) and val[j] != '' and val[j][0] != '"' and val[j][
                                -1] != '"':  # variable
                                if val[j] in variables.keys():
                                    tokens.append({'var ' + line + ' ' + name: val[j]})
                                elif val[j] in types:
                                    tokens.append({'type ' + line + ' ' + name: val[j]})
                                elif val[j] in commands:
                                    tokens.append({'cmd ' + line + ' ' + name: val[j]})
                                else:
                                    try:
                                        if int(val[j], 16):
                                            tokens.append({'hex ' + line + ' ' + name: val[j]})
                                        else:
                                            pass
                                    except:
                                        if len(val[j].split('x')) == 2:
                                            lib.error(line, 'invalid hex number', name)
                                        else:
                                            lib.error(line, f'undefined var {val[j]}', name)


                            else:
                                if val[j] != '':
                                    lib.error(line, f'undefined token {val[j]}', name)


                else:
                    if cmd in types:
                        if cmd != 'func':
                            if len(val) == 7 and val[1] in types: # constant
                                variables[val[1]] = cmd
                                tokens.append({cmd + ' ' + line + ' ' + name : [val[1], val[3]] })
                                #print(val)
                            else:
                                if len(val) == 6: # variable
                                    variables[val[1]] = cmd

                                    tokens.append({cmd + ' ' + line + ' ' + name : [val[1], val[3]] })
                                elif val[-1] != ';':
                                    lib.error(line, 'expected ";"', name)
                                else:
                                    lib.error(line, 'invalid syntax', name)
                        else:
                            tokens.append({'user_func ' + line + ' ' + name: val[1]})
                            commands.append(val[1])
                            for j in range(len(val)):
                                if val[j] in token_list.keys():
                                    tokens.append({token_list[val[j]] + ' ' + line + ' ' + name: val[j]})
                    elif cmd in token_list.keys():
                        tokens.append({token_list[cmd] + ' ' + line + ' ' + name: cmd})
                    else:
                        lib.error(line, f'undefined function or type {cmd}!', name)
        if lib.errors_ == 0:
            for h in range(len(tokens)):
                #print(tokens[h])
                pass
            return tokens
        else:
            sys.exit()
