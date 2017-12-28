import ply.yacc as yacc
import AST

from lex import tokens

precedence = (
    ( 'left' , 'PLUS' ),
	( 'left' , 'MINUS' ),
	( 'left' , 'TIMES' ),
	( 'left' , 'DIV' ),
    # ('right', 'ELSE'),
    ('nonassoc', 'IFX'), # Hack de fou : http://epaperpress.com/lexandyacc/if.html
    ('nonassoc', 'ELSE'),
)

class ParseError(Exception):
    "Exception raised whenever a parsing error occurs."

    pass

vars = dict()

def p_programme_statement(p):
	''' programme : statement '''
	p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
	''' programme : statement programme '''
	p[0] = AST.ProgramNode([p[1]]+p[2].children)

def p_statement(p):
	''' statement : iteration_statement
        | compound_statement
        | expression_statement
        | selection_statement
        | external_declaration
        | return_statement '''
	p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = p[1]

def p_compound_statement_01(p):
    '''compound_statement : LBRACE programme RBRACE'''
    p[0] = p[2]

def p_iteration_statement_01(p):
    ''' iteration_statement : WHILE LPAREN expression RPAREN statement '''
    p[0] = AST.WhileNode([p[3],p[5]])

def p_iteration_statement_02(p):
    '''iteration_statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement'''
    p[0] = AST.ForNode([p[3], p[4], p[5], p[7]])

def p_selection_statement_01(p):
    '''selection_statement : IF LPAREN expression RPAREN statement %prec IFX '''
    p[0] = AST.IfNode([p[3], p[5]])

def p_selection_statement_02(p):
    '''selection_statement : IF LPAREN expression RPAREN statement ELSE statement'''
    p[0] = AST.IfNode([p[3], p[5], p[7]])

def p_assign(p):
    ''' assignation : ID ASSIGN expression '''
    # if(p[1] not in vars):
    #     p_error(p)
    #     print("hello assign")
    # else:
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_expression_assign(p):
    '''expression : logical_expression '''
    p[0] = p[1]

def p_logical_expression_01(p):
    '''logical_expression : equality_expression'''
    p[0] = p[1]

def p_logical_expression_02(p):
    '''logical_expression : logical_expression DOUBLE_AMPERSAND equality_expression
                           | logical_expression DOUBLE_PIPE equality_expression'''
    p[0] = AST.LogicalNode(p[2],[p[1],p[3]])

def p_equality_expression_01(p):
    '''equality_expression : relational_expression'''
    p[0] = p[1]

def p_equality_expression_02(p):
    '''equality_expression : equality_expression EQ relational_expression
                           | equality_expression NOT_EQ relational_expression'''
    p[0] = AST.ComparatorNode(p[2], [p[1], p[3]])

def p_relational_expression_01(p):
    '''relational_expression : additive_expression
    | assignation '''
    p[0] = p[1]

def p_relational_expression_02(p):
    '''relational_expression : relational_expression LESS additive_expression
                             | relational_expression GREATER additive_expression
                             | relational_expression LESS_EQ additive_expression
                             | relational_expression GREATER_EQ additive_expression'''
    p[0] = AST.ComparatorNode(p[2], [p[1], p[3]])

def p_additive_expression_01(p):
    '''additive_expression : additive_expression PLUS mult_expression
    | additive_expression MINUS mult_expression '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_additive_expression_02(p):
    '''additive_expression : mult_expression'''
    p[0] = p[1]

def p_mult_expression_01(p):
    '''mult_expression : mult_expression TIMES postfix_expression
    | mult_expression DIV postfix_expression
    | mult_expression MODULO postfix_expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_mult_expression_02(p):
    '''mult_expression : unary_expression'''
    p[0] = p[1]

def p_unary_expression_01(p):
    '''unary_expression : postfix_expression'''
    p[0] = p[1]

def p_unary_expression_02(p):
    '''unary_expression : MINUS unary_expression'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_unary_expression_03(p):
    '''unary_expression : PLUS unary_expression'''
    p[0] = p[2]

def p_unary_expression_04(p):
    '''unary_expression : EXCLAMATION unary_expression'''
    p[0] = AST.OpNode(p[1], [p[2]])


def p_primary_expression_var(p):
    ''' primary_expression : ID '''
    p[0] = AST.TokenNode(p[1])

def p_primary_expression_num(p):
    ''' primary_expression : INUMBER
        | FNUMBER '''
    p[0] = AST.TokenNode(p[1])

def p_primary_expression_par(p):
    '''primary_expression : LPAREN expression RPAREN '''
    p[0] = p[2]

def p_return_01(p):
    ''' return_statement : RETURN SEMICOLON '''
    p[0] = AST.ReturnNode()

def p_return_02(p):
    ''' return_statement : RETURN expression SEMICOLON '''
    p[0] = AST.ReturnNode(p[2])

# -------------------------------------

def p_postfix_expression_01(p):
    '''postfix_expression : primary_expression'''
    p[0] = p[1]

def p_postfix_expression_02(p):
    '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
    if(p[1].tok not in vars):
        p_error(p)
        print("hello postfix ID : ", p[1].tok)
    else:
        node = AST.FunctionExpressionNode(p[1].tok)
        node.setFunc(True)
        node.addChildren(p[3])
        p[0] = node

def p_postfix_expression_03(p):
    '''postfix_expression : postfix_expression LPAREN RPAREN'''
    if(p[1].tok not in vars):
        p_error(p)
        print("hello postfix ID : ", p[1].tok)
    else:
        p[0] = AST.FunctionExpressionNode(p[1].tok)
        p[0].setFunc(True)

# def p_postfix_expression_04(p):
#     '''postfix_expression : postfix_expression LBRACKET expression RBRACKET'''
#     p[0] = ArrayExpression(t[1], t[3])

def p_argument_expression_list_01(p):
    '''argument_expression_list : expression'''
    p[0] = AST.ArgListNode(p[1])

def p_argument_expression_list_02(p):
    '''argument_expression_list : argument_expression_list COMMA expression'''
    p[1].addChildren(p[3])
    p[0] = p[1]

# ----------------------------------

def p_type_specifier(p):
    '''type_specifier : INT
                      | CHAR
                      | FLOAT '''
    p[0] = p[1]

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration'''
    p[0] = p[1]

def p_function_definition_01(p):
    '''function_definition : type_specifier declarator compound_statement'''
    if(p[2].tok in vars):
        print("hello Declaration Func")
        p_error(p)
    else:
        print("AJOUT DE --- DANS FUNC : ", p[2].tok)
        vars[p[2].tok] = "func"
        p[2].setType(p[1])
        p[2].addChildren(p[3])
        p[0] = p[2]
        # -- Suppr. des paramètres --
        if (len(p[2].children) > 0):
            if (type(p[2].children[0]) is AST.ParamListNode):
                for c in p[2].children[0].children:
                    vars.pop(c.tok, None)

def p_declaration_01(p):
    '''declaration : type_specifier declarator SEMICOLON'''
    # if(p[2].tok in vars):
    #     print("hello Declaration Var")
    #     p_error(p)
    # else:
    #     print("AJOUT DE --- DANS VARS : ", p[2].tok)
    #     vars[p[2].tok] = "var"
    p[2].setType(p[1])
    p[0] = p[2]

def p_declarator_01(p):
    '''declarator : direct_declarator'''
    p[0] = p[1]

def p_direct_declarator_01(p):
    '''direct_declarator : ID'''
    p[0] = AST.DeclarationNode(p[1])

def p_direct_declarator_02(p):
    '''direct_declarator : direct_declarator LPAREN parameter_list RPAREN'''
    p[1].setFunc(True)
    p[1].addChildren(p[3])
    p[0] = p[1]

def p_direct_declarator_03(p):
    '''direct_declarator : direct_declarator LPAREN RPAREN'''
    p[1].setFunc(True)
    p[0] = p[1]

def p_parameter_list_01(p):
    '''parameter_list : parameter_declaration'''
    p[0] = AST.ParamListNode(p[1])

def p_parameter_list_02(p):
    '''parameter_list : parameter_list COMMA parameter_declaration'''
    p[1].addChildren(p[3])
    p[0] = p[1]

def p_parameter_declaration(p):
    '''parameter_declaration : type_specifier declarator'''
    # NOTE: this is the same code as p_declaration_01!
    p_declaration_01(p)

def p_error(p) :
	if p is not None:
		print("Erreur de syntaxe à la ligne %s"%(p.lineno))
		parser.errok()
	else:
		print("Unexpected end of input")

def parse(program):
    return yacc.parse(program)

parser = yacc.yacc(outputdir = 'generated')

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
