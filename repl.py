from lexer import Lexer

def start():
    while True:
        line = input(">> ")

        if line == "":
            return
        
        for token in Lexer(line):
            print(token)

        