import dataclasses
from enum import Enum,auto

class TokenType(Enum):
    # Single-character tokens
    LEFT_PARTEN = auto()
    RIGHT_PARTEN= auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT =auto()
    MINUS=auto()
    PLUS= auto()
    SEMICOLON=auto()
    SLASH = auto()
    STAR =auto()

    # one or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    #Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER= auto()

    #keyWords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FOR = auto()
    FUN = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF=auto()

@dataclasses.dataclass
class Token:
   type:TokenType
   lexeme: str
   literal: object
   line:int