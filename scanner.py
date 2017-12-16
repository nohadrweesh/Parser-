def check_last_token_type(token, token_type):
    if len(token) > 0 and token.isspace() == False:
        if token_type == 2:
            if token in reserved_words:
                scanner_tokens.append((token, 'reserved word'))
                output_file.write(token + "  :reserved word\n")
            else:
                scanner_tokens.append((token, 'identifier'))
                output_file.write(token + "  :identifier\n")
        elif token_type == 3:
            scanner_tokens.append((token, 'number'))
            output_file.write(token + "  :number\n")
        elif token_type == 4:
            if token in special_symbols:
                scanner_tokens.append((token, 'special symbol'))
                output_file.write(token + "  :special symbol\n")

inpFile = 'tiny_sample_code.txt'
outFile = 'scanner_output.txt'

# variables
reserved_words = ['if', 'then', 'else', 'end', 'repeat', 'until', 'read', 'write']
special_symbols = ['+', '-', '/', '*', '=', '<', '(', ')', ';', ':', ':=']

scanner_tokens = []

with open(inpFile, 'r')as input_file:
    with open(outFile, 'w')as output_file:

        content = input_file.read()
        token = ''
        token_type = -1  # 1-->comment  2-->identifier  3-->number  4-->simple special symbol
        #print(content)
        for char in content:

            if token_type == 1 and char != '}':
                continue
            elif token_type == 1 and char == '}':
                token_type = -1
                continue

            if char == '{':
                if token_type != -1:
                    check_last_token_type(token, token_type)
                    token = ''
                token_type = 1
            elif char.isalpha():  # and (token_type == -1 or token_type == 2):
                if token_type != 2 and token_type != -1:
                    check_last_token_type(token, token_type)
                    token = ''

                token_type = 2
                token += char
            elif char .isspace():  # check token type
                check_last_token_type(token, token_type)

                token = ''
                token_type = -1

            elif char in special_symbols:
                if token_type != 4:
                    check_last_token_type(token, token_type)
                    token = ''
                token_type = 4
                token += char
            elif char.isdigit():  # and (token_type==-1 or token_type==3):
                if token_type != 3 and token_type != -1:
                    check_last_token_type(token, token_type)
                    token = ''
                token_type = 3
                token += char
        check_last_token_type(token, token_type)


