from typing import *
from TokenClass import Token
from TokenType import TokenType
import XYZ

class Scanner:
    source:str
    tokens:List[Token]

    start:int = 0 # Start of the current lexeme
    current:int = 0# Current character being considered
    line:int = 1

    keywords:Dict[str,TokenType] = {
        "and":TokenType.AND,
        "class":TokenType.CLASS,
        "else":TokenType.ELSE,
        "false":TokenType.FALSE,
        "for":TokenType.FOR,
        "fun":TokenType.FUN,
        "if":TokenType.IF,
        "nil":TokenType.NIL,
        "or":TokenType.OR,
        "print":TokenType.PRINT,
        "return":TokenType.RETURN,
        "super":TokenType.SUPER,
        "this":TokenType.THIS,
        "true":TokenType.TRUE,
        "var":TokenType.VAR,
        "while":TokenType.WHILE
    }

    def __init__(self, source:str):
        self.source = source

    def scanTokens(self) -> List[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF,"",None,self.line))
        return self.tokens
    
    def isAtEnd(self) -> bool:
        return self.current>=len(self.source)
    
    def scanToken(self)->None:
        c:str = self.advance()

        match c:
            case '(': self.addToken(TokenType.LEFT_PAREN)
            case ')': self.addToken(TokenType.RIGHT_PAREN)
            case '{': self.addToken(TokenType.LEFT_BRACE)
            case '}': self.addToken(TokenType.RIGHT_BRACE)
            case ',': self.addToken(TokenType.COMMA)
            case '.': self.addToken(TokenType.DOT)
            case '-': self.addToken(TokenType.MINUS)
            case '+': self.addToken(TokenType.PLUS)
            case ';': self.addToken(TokenType.SEMICOLON)
            case '*': self.addToken(TokenType.STAR)

            case '!':
                self.addToken(TokenType.EXCLAMATION_EQUAL if self.match('=') else TokenType.EXCLAMATION)
            case '=':
                self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<':
                self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>':
                self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)


            case '/':
                if self.match('/'):
                    while self.peek()!='\n' and not self.isAtEnd():
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)

            case ' ', '\r', '\t': pass
            case '\n': self.line+=1


            case '"': self.string()


            case _: 
                if isDigit(c):
                    self.number()
                elif isAlpha(c):
                    self.identifier()
                else:
                    XYZ.error(self.line,"Unexpected character."); 

    def advance(self) -> str:
        self.current+=1
        return self.source[self.current-1]

    def addToken(self, type:TokenType) -> None:
        addToken(type,None)
    
    def addToken(self, type:TokenType, literal:object) -> None:
        text:str = self.source[self.start:self.current]
        self.tokens.append(Token(type,text,literal,self.line) )
    
    def match(self, expected:str) -> bool:
        if self.isAtEnd(): return False
        if self.source[self.current]!=expected: return False

        self.current+=1
        return True
    
    def peek(self) -> str: #does not consume the character
        if self.isAtEnd(): return '\0'
        return self.source[self.current]
    
    def string(self) -> None:
        while self.peek()!='"' and not self.isAtEnd():
            if self.peek()=='\n': self.line+=1 #support multiline strings
            self.advance()
        
        if self.isAtEnd():
            XYZ.error(self.line,"Unterminated string.")
            return
        
        self.advance()
        value:str = self.source[self.start+1:self.current-1]
        self.addToken(TokenType.STRING,value)
    
    def isDigit(self, c:str) -> bool:
        return c>='0' and c<='9'
    
    def number(self, c:str) -> None:
        while self.isDigit(self.peek()):
            self.advance()
        
        if self.peek()=='.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()
        
        self.addToken(TokenType.NUMBER,float(self.source[self.start:self.current]))
    
    def peekNext(self) -> str:
        if self.current+1>=len(self.source): return '\0'
        return self.source[self.current+1]
    
    def identifier(self) -> None:
        while isAlphaNumeric(self.peek()):
            self.advance()
        
        text:str = self.source[self.start:self.current]
        type:TokenType = self.keywords.get(text,TokenType.IDENTIFIER)

        self.addToken(type)
    
    def isAlpha(self, c:str) -> bool:
        return (c>='a' and c<='z') or (c>='A' and c<='Z') or c=='_'
    
    def isAlphaNumeric(self, c:str) -> bool:
        return isAlpha(c) or isDigit(c)