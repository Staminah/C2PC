#  ---------------------------------------------------------------
#  Parser_C2PC.py
#
#  Fleury Anthony, Hirschi Christophe, Schnaebele Marc
#  Parser for our C compiler
#  15/01/2018
#
#  ---------------------------------------------------------------

import ply.yacc as yacc
import AST
from lex import tokens

precedence = (
    ( 'left' , 'PLUS' ),
	( 'left' , 'MINUS' ),
	( 'left' , 'TIMES' ),
	( 'left' , 'DIV' ),
    ('nonassoc', 'IFX'), # Hack de fou : http://epaperpress.com/lexandyacc/if.html
    ('nonassoc', 'ELSE'),
)

func_name = dict()

#  ---------------------------------------------------------------
#  PROGRAM
#  ---------------------------------------------------------------

def p_programme_statement(p):
	''' programme : statement '''
	p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
	''' programme : statement programme '''
	p[0] = AST.ProgramNode([p[1]]+p[2].children)

#  ---------------------------------------------------------------
#  STATEMENT
#  ---------------------------------------------------------------

def p_statement(p):
	''' statement : iteration_statement
        | compound_statement
        | expression_statement
        | selection_statement
        | external_declaration
        | jump_statement '''
	p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = p[1]

def p_compound_statement_01(p):
    '''compound_statement : LBRACE programme RBRACE'''
    p[0] = p[2]

#  ---------------------------------------------------------------
#  ITERATION STATEMENT
#  ---------------------------------------------------------------

def p_iteration_statement_01(p):
    ''' iteration_statement : WHILE LPAREN expression RPAREN statement '''
    p[0] = AST.WhileNode([p[3],p[5]])

def p_iteration_statement_02(p):
    '''iteration_statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement'''
    p[0] = AST.ForNode([p[3], p[4], p[5], p[7]])

#  ---------------------------------------------------------------
#  SElECTION STATEMENT
#  ---------------------------------------------------------------

def p_selection_statement_01(p):
    '''selection_statement : IF LPAREN expression RPAREN statement %prec IFX '''
    p[0] = AST.IfNode([p[3], p[5]])

def p_selection_statement_02(p):
    '''selection_statement : IF LPAREN expression RPAREN statement ELSE statement'''
    p[0] = AST.IfNode([p[3], p[5], p[7]])

#  ---------------------------------------------------------------
#  EXPRESSION
#  ---------------------------------------------------------------

def p_expression_assign(p):
    '''expression : assignment_expression '''
    p[0] = p[1]


#  ---------------------------------------------------------------
#  ASSIGMENT EXPRESSION
#  ---------------------------------------------------------------

def p_assignment_expression_01(p):
    ''' assignment_expression : logical_expression '''
    p[0] = p[1]

def p_assignment_expression_02(p):
    ''' assignment_expression : unary_expression assignment_operator assignment_expression '''
    p[0] = AST.AssignNode(p[2], [p[1] ,p[3]])

def p_assignment_operator(p):
    ''' assignment_operator : ASSIGN
                            | EQ_PLUS
                            | EQ_MINUS
                            | EQ_DIV
                            | EQ_TIMES'''
    p[0] = p[1]

#  ---------------------------------------------------------------
#  LOGICAL EXPRESSION
#  ---------------------------------------------------------------

def p_logical_expression_01(p):
    '''logical_expression : equality_expression'''
    p[0] = p[1]

def p_logical_expression_02(p):
    '''logical_expression : logical_expression DOUBLE_AMPERSAND equality_expression
                          | logical_expression DOUBLE_PIPE equality_expression'''
    p[0] = AST.LogicalNode(p[2],[p[1],p[3]])

#  ---------------------------------------------------------------
#  EQUALITY EXPRESSION
#  ---------------------------------------------------------------

def p_equality_expression_01(p):
    '''equality_expression : relational_expression'''
    p[0] = p[1]

def p_equality_expression_02(p):
    '''equality_expression : equality_expression EQ relational_expression
                           | equality_expression NOT_EQ relational_expression'''
    p[0] = AST.ComparatorNode(p[2], [p[1], p[3]])

#  ---------------------------------------------------------------
#  RELATIONAL EXPRESSION
#  ---------------------------------------------------------------

def p_relational_expression_01(p):
    '''relational_expression : additive_expression'''
    p[0] = p[1]

def p_relational_expression_02(p):
    '''relational_expression : relational_expression LESS additive_expression
                             | relational_expression GREATER additive_expression
                             | relational_expression LESS_EQ additive_expression
                             | relational_expression GREATER_EQ additive_expression'''
    p[0] = AST.ComparatorNode(p[2], [p[1], p[3]])

#  ---------------------------------------------------------------
#  ADDITIVE EXPRESSION
#  ---------------------------------------------------------------

def p_additive_expression_01(p):
    '''additive_expression : additive_expression PLUS mult_expression
    | additive_expression MINUS mult_expression '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_additive_expression_02(p):
    '''additive_expression : mult_expression'''
    p[0] = p[1]

#  ---------------------------------------------------------------
#  MULTIPLICATIVE EXPRESSION
#  ---------------------------------------------------------------

def p_mult_expression_01(p):
    '''mult_expression : mult_expression TIMES postfix_expression
    | mult_expression DIV postfix_expression
    | mult_expression MODULO postfix_expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_mult_expression_02(p):
    '''mult_expression : unary_expression'''
    p[0] = p[1]

#  ---------------------------------------------------------------
#  UNARY EXPRESSION
#  ---------------------------------------------------------------

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

#  ---------------------------------------------------------------
#  POSTFIX EXPRESSION
#  ---------------------------------------------------------------

def p_postfix_expression_01(p):
    '''postfix_expression : primary_expression'''
    p[0] = p[1]

def p_postfix_expression_02(p):
    '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
    if(p[1].tok not in func_name):
        p_error(p)
    else:
        node = AST.FunctionExpressionNode(p[1].tok)
        node.setFunc(True)
        node.addChildren(p[3])
        p[0] = node

def p_postfix_expression_03(p):
    '''postfix_expression : postfix_expression LPAREN RPAREN'''
    if(p[1].tok not in func_name):
        p_error(p)
    else:
        p[0] = AST.FunctionExpressionNode(p[1].tok)
        p[0].setFunc(True)

#  ---------------------------------------------------------------
#  ARGUMENTS LIST
#  ---------------------------------------------------------------

def p_argument_expression_list_01(p):
    '''argument_expression_list : expression'''
    p[0] = AST.ArgListNode(p[1])

def p_argument_expression_list_02(p):
    '''argument_expression_list : argument_expression_list COMMA expression'''
    p[1].addChildren(p[3])
    p[0] = p[1]


#  ---------------------------------------------------------------
#  PRIMARY EXPRESSION
#  ---------------------------------------------------------------

def p_primary_expression_var(p):
    ''' primary_expression : ID '''
    p[0] = AST.TokenNode(p[1])

def p_primary_expression_num_integer(p):
    ''' primary_expression : INUMBER '''
    p[0] = AST.TokenNode(p[1])
    p[0].setType('int')

def p_primary_expression_num_float(p):
    ''' primary_expression : FNUMBER '''
    p[0] = AST.TokenNode(p[1])
    p[0].setType('float')

def p_primary_expression_char(p):
    '''primary_expression : CHARACTER'''
    p[0] = AST.TokenNode(p[1])
    p[0].setType('char')

def p_primary_expression_par(p):
    '''primary_expression : LPAREN expression RPAREN '''
    p[0] = p[2]

def p_primary_expression_string(p):
    '''primary_expression : STRING'''
    p[0] = AST.TokenNode(p[1])
    p[0].setType('string')

#  ---------------------------------------------------------------
#  JUMP STATEMENT
#  ---------------------------------------------------------------

def p_return_01(p):
    ''' jump_statement : RETURN SEMICOLON '''
    p[0] = AST.ReturnNode()

def p_return_02(p):
    ''' jump_statement : RETURN expression SEMICOLON '''
    p[0] = AST.ReturnNode(p[2])

def p_break(p):
    ''' jump_statement : BREAK SEMICOLON '''
    p[0] = AST.BreakNode()

def p_continue(p):
    ''' jump_statement : CONTINUE SEMICOLON '''
    p[0] = AST.ContinueNode()

#  ---------------------------------------------------------------
#  DECLARATION
#  ---------------------------------------------------------------

def p_type_specifier(p):
    '''type_specifier : INT
                      | CHAR
                      | FLOAT
                      | SHORT
                      | LONG
                      | DOUBLE
                      | VOID '''
    p[0] = p[1]

def p_declaration_specifier(p):
    ''' declaration_specifier : type_specifier '''
    p[0] = p[1]

def p_initilizer(p):
    ''' initializer : assignment_expression '''
    p[0] = p[1]

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration'''
    p[0] = p[1]

def p_function_definition_01(p):
    '''function_definition : declaration_specifier declarator compound_statement'''
    if(p[2].tok in func_name):
        p_error(p)
    else:
        func_name[p[2].tok] = "func"
        p[2].setType(p[1])
        p[2].addChildren(p[3])
        p[0] = p[2]
        # -- Suppr. des paramètres --
        if (len(p[2].children) > 0):
            if (type(p[2].children[0]) is AST.ParamListNode):
                for c in p[2].children[0].children:
                    func_name.pop(c.tok, None)

def p_declaration_01(p):
    '''declaration : declaration_specifier init_declarator SEMICOLON'''
    if type(p[2]) is AST.AssignNode:
        p[2].children[0].setType(p[1])
    else:
        p[2].setType(p[1])
    p[0] = p[2]

def p_init_declarator_01(p):
    ''' init_declarator : declarator'''
    p[0] = p[1]

def p_init_declarator_02(p):
    ''' init_declarator : declarator ASSIGN initializer'''
    p[0] = AST.AssignNode(p[2], [p[1], p[3]])

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

def p_direct_declarator_04(p):
    '''direct_declarator : ID LBRACKET RBRACKET'''
    p[0] = AST.DeclarationNode(p[1])
    p[0].setArray(True)

#  ---------------------------------------------------------------
#  PARAMETERS LIST
#  ---------------------------------------------------------------

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

#  ---------------------------------------------------------------
#  ERRORS
#  ---------------------------------------------------------------

def p_error(p) :
	if p is not None:
		print("Erreur de syntaxe à la ligne %s"%(p.lineno))
		parser.errok()
	else:
		print("Unexpected end of input")

#  ---------------------------------------------------------------
#  PARSE
#  ---------------------------------------------------------------

def parse(program):
    return yacc.parse(program)

parser = yacc.yacc(outputdir = 'generated')

#  ---------------------------------------------------------------
#  MAIN PARSER ACTIVITY
#  ---------------------------------------------------------------

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
