
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSleftTIMESleftDIVleftMINUSSHORT CHAR DOUBLE FLOAT INT LONG VOID IF ELSE FOR WHILE RETURN COMMA SEMICOLON LPAREN RPAREN LBRACE RBRACE ASSIGN GREATER LESS EQ NOT_EQ GREATER_EQ LESS_EQ PLUS MINUS TIMES DIV MODULO CARET DOT EQ_PLUS EQ_MINUS EQ_TIMES EQ_DIV ID FNUMBER INUMBER STRING CHARACTER programme : statement SEMICOLON programme : statement SEMICOLON programme  statement : assignation  assignation : ID ASSIGN expression  expression : ID  expression : INUMBER\n        | FNUMBER expression : LPAREN expression RPARENexpression : expression PLUS expression\n    | expression MINUS expression\n    | expression TIMES expression\n    | expression DIV expression '
    
_lr_action_items = {'ID':([0,5,6,12,13,14,15,16,],[4,4,8,8,8,8,8,8,]),'$end':([1,5,7,],[0,-1,-2,]),'SEMICOLON':([2,3,8,9,10,11,18,19,20,21,22,],[5,-3,-5,-4,-6,-7,-9,-10,-11,-12,-8,]),'ASSIGN':([4,],[6,]),'INUMBER':([6,12,13,14,15,16,],[10,10,10,10,10,10,]),'FNUMBER':([6,12,13,14,15,16,],[11,11,11,11,11,11,]),'LPAREN':([6,12,13,14,15,16,],[12,12,12,12,12,12,]),'PLUS':([8,9,10,11,17,18,19,20,21,22,],[-5,13,-6,-7,13,-9,-10,-11,-12,-8,]),'MINUS':([8,9,10,11,17,18,19,20,21,22,],[-5,14,-6,-7,14,14,-10,14,14,-8,]),'TIMES':([8,9,10,11,17,18,19,20,21,22,],[-5,15,-6,-7,15,15,-10,-11,-12,-8,]),'DIV':([8,9,10,11,17,18,19,20,21,22,],[-5,16,-6,-7,16,16,-10,16,-12,-8,]),'RPAREN':([8,10,11,17,18,19,20,21,22,],[-5,-6,-7,22,-9,-10,-11,-12,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programme':([0,5,],[1,7,]),'statement':([0,5,],[2,2,]),'assignation':([0,5,],[3,3,]),'expression':([6,12,13,14,15,16,],[9,17,18,19,20,21,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programme","S'",1,None,None,None),
  ('programme -> statement SEMICOLON','programme',2,'p_programme_statement','parser.py',16),
  ('programme -> statement SEMICOLON programme','programme',3,'p_programme_recursive','parser.py',20),
  ('statement -> assignation','statement',1,'p_statement','parser.py',24),
  ('assignation -> ID ASSIGN expression','assignation',3,'p_assign','parser.py',33),
  ('expression -> ID','expression',1,'p_expression_var','parser.py',37),
  ('expression -> INUMBER','expression',1,'p_expression_num','parser.py',41),
  ('expression -> FNUMBER','expression',1,'p_expression_num','parser.py',42),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_par','parser.py',46),
  ('expression -> expression PLUS expression','expression',3,'p_expression_op','parser.py',50),
  ('expression -> expression MINUS expression','expression',3,'p_expression_op','parser.py',51),
  ('expression -> expression TIMES expression','expression',3,'p_expression_op','parser.py',52),
  ('expression -> expression DIV expression','expression',3,'p_expression_op','parser.py',53),
]
