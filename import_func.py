import re


def Lexer(dict, file='prog.a') -> object:
    file1 = open(file)
    text = file1.read()
    content = text.lstrip()
    strings = content.split(";")
    strObject = []
    lexems = []
    variables = {}



    for i in range(len(strings)):
        currentString = strings[i]
        if currentString != '' and currentString[0] != '/' and currentString[1] != '/':
            copyString = currentString
            words = currentString.split(' ')
            command = words[0].lstrip()
            value = copyString.replace(command, ' ').lstrip()
            if command.lstrip() in dict['func']:
                strObject.append({'func': command})
            else:
                print('Command ' + command + ' not found!')
                return



            if re.search(r'"', value):
                if len(value.replace('"', '').lstrip()) > 0:
                    strObject.append(
                        {
                            'value': {
                                'type': 'string',
                                'value': value.replace('"', '')
                            }
                        }
                    )
            elif re.search(r'"', value) != True:
                try:
                    # number
                    if value != '':
                        strObject.append(
                            {
                                'value': {
                                    'type': 'number',
                                    'value': int(value)
                                }
                            }
                        )
                except:
                    # undefined
                    strObject.append(
                        {
                            'value': {
                                'type': 'undefined',
                                'value': value
                            }
                        }
                    )
        if command == '_str' and words[2] == 'equ':
            variables[words[1]] = [words[3].replace('"', ''), 'str']
        if command == '_num' and words[2] == 'equ':
            variables[words[1]] = [words[3].replace('"', ''), 'num']

        if command == 'END':
            lexems = strObject
            return [lexems, variables]





def parser(lexems, dict, variables) -> object:
    if lexems and len(lexems) != 0:
        for i in range(len(lexems)):
            try:
                funcName = lexems[i]['func']
                funcValue = lexems[i+1]['value']['value']
                valueType = lexems[i+1]['value']['type']#тип значення

                #LOG FUNCTION

                if funcName == 'LOG':
                    if valueType == 'string' or valueType == 'number':
                        print(funcValue) #тут виводимо текст який напряму передається в функцію
                    else:
                        try:
                            print(variables[funcValue][0])#тут виводимо текст з змінної
                        except:
                            print('Variable ' + funcValue + ' not exist!')
                            return

                #LEN FUNCTION


            except:
                pass
