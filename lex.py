#  ---------------------------------------------------------------
#  lex.py
#
#  Fleury Anthony, Hirschi Christophe, Schnaebele Marc
#  Lexical Anaylizer for our C compiler
#  27/11/2017
#
#  Original author : https://github.com/gotchacode/mini_c
#  ---------------------------------------------------------------

import ply.lex as lex
import re

#  ---------------------------------------------------------------
#  TOKEN LIST
#  ---------------------------------------------------------------

tokens = (
    # Reserved words
    'SHORT',
    'CHAR',
    'DOUBLE',
    'FLOAT',
    'INT',
    'LONG',
    'VOID',
    'IF',
    'ELSE',
    'FOR',
    'WHILE',
    'RETURN',
    'BREAK',
    'CONTINUE',

    # Special characters
    'COMMA',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'ASSIGN',
    'GREATER',
    'LESS',
    'EQ',
    'NOT_EQ',
    'GREATER_EQ',
    'LESS_EQ',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIV',
    'MODULO',
    'EXCLAMATION',
    'EQ_PLUS',
    'EQ_MINUS',
    'EQ_TIMES',
    'EQ_DIV',
    'DOUBLE_AMPERSAND',
    'DOUBLE_PIPE',


    # Complex tokens
    'ID',
    'FNUMBER',
    'INUMBER',
    'STRING',
    'CHARACTER',
    )

#  ---------------------------------------------------------------
#  RESERVED WORDS
#  ---------------------------------------------------------------

reserved_words = {
    'short' : 'SHORT',
    'char' : 'CHAR',
    'double' : 'DOUBLE',
    'float' : 'FLOAT',
    'int' : 'INT',
    'long' : 'LONG',
    'void' : 'VOID',
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'return' : 'RETURN',
    'break' : 'BREAK',
    'continue' : 'CONTINUE'
}

#  ---------------------------------------------------------------
#  SPECIAL CHARACTERS
#  ---------------------------------------------------------------

t_COMMA = r','
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_EQ = r'=='
t_NOT_EQ = r'!='
t_GREATER_EQ = r'>='
t_LESS_EQ = r'<='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/(?!\*)'
t_MODULO = r'%'
t_EXCLAMATION = r'!'
t_EQ_PLUS = r'\+='
t_EQ_MINUS = r'-='
t_EQ_TIMES = r'\*='
t_EQ_DIV = r'/='
t_DOUBLE_AMPERSAND = r'&&'
t_DOUBLE_PIPE = r'\|\|'

#  ---------------------------------------------------------------
#  COMPLEX TOKENS
#  ---------------------------------------------------------------

def t_ID(t):
    # Identifiants en tous genre (noms fonctions, variables, ...)
    # Commence par une seule lettre en min ou maj
    # suivie de zéro ou plusieurs caractères quelconques ( \w ---> a-z, A-Z, 0-9, including the _ (underscore))
    r'[A-Za-z_][\w]*'
    # Si le mot détecté est présent dans la liste des mots réservés, il est déclaré en tant que tel
    # Sinon c'est un ID
    if t.value in reserved_words:
        t.type = reserved_words[t.value]
    return t

def t_FNUMBER(t):
    # Nombres flottants
    # ((0(?!\d))|([1-9]\d*)) :  Permet de s'assurer que le nombre commence soit par 0 tout seul ou alors un nombre quelconque
    # (\.\d+) : Un point suivi d'au moins un ou plusieurs caractères numériques
    r'((0(?!\d))|([1-9]\d*))(\.\d+)'
    return t

def t_INUMBER(t):
    # Nombres entiers
    # 0(?!\d) : Zéro tout seul suivi d'aucun autre nombre
    # ([1-9]\d*) : Ou alors un nombre entre 1 et 9 suivi de zero ou plusieurs autres nombres
    r'0(?!\d)|([1-9]\d*)'
    return t

def t_CHARACTER(t):
    # Caractère tout seul entre apostophes
    r"'\w'"
    return t

def t_STRING(t):
    # Chaines de caractères entre guillemets
    # [^\n]* : Tout caractères sauf un retour chariot ou backslach, zero ou plusieurs fois
    r'"[^\n\\]*"'
    return t

#  ---------------------------------------------------------------
#  IGNORED TOKENS
#  ---------------------------------------------------------------

def t_WHITESPACE(t):
    # Espaces ou tabulations
    r'[ \t]+'
    pass

def t_NEWLINE(t):
    # Retours chariots
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    # Commentaires commençant par /* et finissant par */
    # *? : Lazy, s'arrête quand il rencontre le premier */
    r'/\*[\w\W]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

#  ---------------------------------------------------------------
#  ERROR HANDLING
#  ---------------------------------------------------------------

def t_error(t):
    print("Line %d." % (t.lineno,) + "")
    if t.value[0] == '"':
        print("Unterminated string literal.")
        if t.value.count('\n') > 0:
            t.lexer.skip(t.value.index('\n'))
    elif t.value[0:2] == '/*':
        print("Unterminated comment.")
        if t.value.count('\n') > 0:
            t.lexer.skip(t.value.index('\n'))
    else:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

#  ---------------------------------------------------------------
#  MAIN LEXER FUNCTIONALITY
#  ---------------------------------------------------------------

lex.lex()

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))

#  ---------------------------------------------------------------
#  End of clex.py
#  ---------------------------------------------------------------
