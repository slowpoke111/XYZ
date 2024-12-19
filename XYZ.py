from typing import *
import sys
from TokenType import TokenType
from Parser import Parser
from Scanner import Scanner
from Expr import Expr
from ASTprinter import ASTprinter

class XYZ:

    hadError:bool = False

    def main(args:List[str]) -> None:
        if len(args)>1:
            print("Usage: XYZ [script]")
            sys.exit(64)
        elif len(args)==1:
            runFile(args[0])
        else:
            runPrompt()
    
    def runFile(path:str) -> None:
        with open(path,"rb") as f:
            byte:List[bytes] = f.read()
        
        run(str(byte,"utf-8"))
        if hadError:
            sys.exit(65)

    def runPrompt() -> None:
        while True:
            line:str = input("> ")
            if line==None or line=="exit":
                break
            run(line)
            hadError = False
    
    def run(source:str) -> None:
        parser:Parser = Parser(Scanner(source).scanTokens())
        expr:Expr = parser.parse()

        if hadError: return

        print(ASTprinter().print(expr))
    
    def error(line:int,message:str) -> None:
        report(line,"",message)
    
    def error(token:str,message:str) -> None:
        if token.type == TokenType.EOF:
            report(token.line," at end",message)
        else:
            report(token.line,f" at '{token.lexeme}'",message)
    
    def report(line:int,where:str,message:str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        hadError = True