from lexer import lex
from parser import parse

def start():
    while True:
        line = input(">> ")

        if line == "":
            return
        
        for statement in parse(line):
            print(statement)

if __name__ == '__main__':
    print("Hello! This is the Monkey programming language!")
    print("Feel free to type in commands.")
    start()