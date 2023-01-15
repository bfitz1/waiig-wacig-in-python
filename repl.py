import sys

from lexer import lex
from parser import parse
from evaluator import Eval
from mobject import inspect
from environment import Environment

def start():
    env = Environment()
    while True:
        line = input(">> ")

        if line == "":
            return
        
        evaluated = Eval(env, parse(line))

        if evaluated:
            print(inspect(evaluated))

if __name__ == '__main__':
    print("Hello! This is the Monkey programming language!")
    print("Feel free to type in commands.")

    try:
        start()
    except KeyboardInterrupt:
        print("Quitting. Goodbye!")
        sys.exit(0)