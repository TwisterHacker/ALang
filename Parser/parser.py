import sys

from Lib import lib


class Parser():
    def parse(self, tokens):
        commands = ['module', 'log', 'return', 'byte', 'hex']
        types = ['int', 'str', 'float', 'hex', '_int']

        sl = []  # syntax list

        func = False
        func_name = None
        user_func = False
        var = if_, elif_, else_, while_, = False, False, False, False
        cmd = False

        for i in range(len(tokens)):
            keys = tokens[i].keys()
            tok = list(keys)[0].split(' ')[0]
            # val = tokens[i][tok].split(' ')[0]
            line = list(keys)[0].split(' ')[1]
            name = list(keys)[0].split(' ')[2]
            val = tokens[i][list(keys)[0]]
            if tok == 'func':
                if val in commands:
                    func_name = val
                    func = True
                else:  # running user function
                    func_name = '_' + val
                    func = True
            if tok == 'open_bracket' and func:
                sl.append(func_name + '(')
            if tok == 'closed_bracket':
                func_name = None
                sl.append(')')
                func = False
            if tok == 'new_line':
                if func == True:
                    lib.error(line, 'expected ")"', name)
                sl.append('end')  # ;
            if tok == 'user_func':
                sl.append({'user_func': val})
                if val == 'main':
                    pass
                else:
                    user_func = True
            if tok == 'cur_closed_bracket':
                if user_func == True:
                    sl.append('stop_usr_fun')
                    user_func = False
                else:
                    pass
            if tok in types:
                sl.append({tok: val})
        print(sl)

        if lib.errors_ == 0:
            return sl
        else:
            sys.exit()
