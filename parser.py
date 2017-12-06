import ply.yacc as yacc
import AST

from lex import tokens

precedence = (
    ( 'left' , 'PLUS' ),
	( 'left' , 'TIMES' ),
	( 'left' , 'DIV' ),
	( 'left' , 'MINUS' )
)

vars = {}

def p_programme_statement(p):
	''' programme : statement SEMICOLON'''
	p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
	''' programme : statement SEMICOLON programme '''
	p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_statement(p):
	''' statement : assignation '''
         # | structure '''
	p[0] = p[1]

# def p_structure(p):
#     ''' structure : WHILE expression LBRACE programme RBRACE '''
#     p[0] = AST.WhileNode([p[2],p[4]])

def p_assign(p):
	''' assignation : ID ASSIGN expression '''
	p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_expression_var(p):
	''' expression : ID '''
	p[0] = AST.TokenNode(p[1])

def p_expression_num(p):
    ''' expression : INUMBER
        | FNUMBER '''
    p[0] = AST.TokenNode(p[1])

def p_expression_par(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_op(p):
    '''expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIV expression '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_error(p) :
	if p is not None:
		print("Erreur de syntaxe à la ligne %s"%(p.lineno))
		parser.errok()
	else:
		print("Unexpected end of input")

def parse(program):
    return yacc.parse(program)

parser = yacc.yacc(outputdir = 'generated', debug=1)

if __name__ == "__main__" :

    import sys

    prog = open(sys.argv[1]).read()
    result = parse(prog)

    if result:
        print (result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
