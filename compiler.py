#  ---------------------------------------------------------------
#  compiler.py
#
#  Fleury Anthony, Hirschi Christophe, Schnaebele Marc
#  Compiler file to Python for our C compiler
#  15/01/2018
#
#  Original author : M. Amiguet (HE-Arc)
#  ---------------------------------------------------------------

import AST
from AST import addToClass

#  ---------------------------------------------------------------
#  GLOBAL VARIABLES
#  ---------------------------------------------------------------

# Compteur global d'indentations python
tabcounter = 0

# Tableau des relations entre types
types_dict = {'int':'int',
			  'short':'int',
	          'long':'int',
	          'char':'char',
			  'string':'char',
	          'float':'float',
	          'double':'float'}

# Variables globales pour les contextes et leurs assignations de variables
context = ["main"]
contextcounter = 0
contexterror = False
vars_tab = {}
vars_tab[context[contextcounter]] = {}

#  ---------------------------------------------------------------
#  INDENTATION MANGEMENT
#  ---------------------------------------------------------------

# Indentations python
def getIndent():
	'''Méthode qui retourne le nombre d'indentations en string'''
	tab = ""
	for i in range(0, tabcounter):
		tab += "\t"
	return tab

#  ---------------------------------------------------------------
#  COMPILING METHODS
#  ---------------------------------------------------------------

# Noeud de programme
@addToClass(AST.ProgramNode)
def compile(self):
	pycode = ""
	for c in self.children:
		pycode += c.compile()
	return pycode

# Noeud terminal
@addToClass(AST.TokenNode)
def compile(self):
	pycode = ""
	pycode += "%s" % self.tok
	return pycode

# Noeud d'assignation de variable
@addToClass(AST.AssignNode)
def compile(self):
	# Gestion des types
	if (type(self.children[0]) is AST.DeclarationNode):
		vars_tab[context[contextcounter]][self.children[0].tok] = self.children[0].type.lower()
	self.type = type_checking(self.children[0], self.children[1])
	# Gestion du code python
	tabs = getIndent()
	pycode = ""
	pycode += tabs
	pycode += "%s %s %s\n" % (self.children[0].tok, self.op, self.children[1].compile())
	return pycode

# Noeud d'opération arithmétique
@addToClass(AST.OpNode)
def compile(self):
	global vars_tab
	global context
	global contextcounter
	pycode = ""
	# Opération binaire
	if (len(self.children) == 2):
		# Gestion des types
		if self.children[0].type == None and self.children[0].tok in vars_tab[context[contextcounter]]:
			self.children[0].type = vars_tab[context[contextcounter]][self.children[0].tok]
		elif self.children[1].type == None and self.children[1].tok in vars_tab[context[contextcounter]]:
			self.children[1].type = vars_tab[context[contextcounter]][self.children[1].tok]
		self.type = type_checking(self.children[0], self.children[1])
		# Gestion du code python
		pycode += "(" + self.children[0].compile() + " "
		pycode += self.op
		pycode += " " + self.children[1].compile() + ")"
	# Opération unaire
	elif (len(self.children) == 1):
		if self.op == "!":
			pycode += "not " + self.children[0].compile()
		elif self.op == "+":
			pycode += self.children[0].compile()
		else:
			pycode += self.op + self.children[0].compile()
	return pycode

# Noeud de boucle while
@addToClass(AST.WhileNode)
def compile(self):
	tabs = getIndent()
	global tabcounter
	pycode = ""
	pycode += tabs + "while " + self.children[0].compile() + ":\n"
	tabcounter += 1
	pycode += self.children[1].compile()
	tabcounter -= 1
	return pycode

# Noeud de boucle for
@addToClass(AST.ForNode)
def compile(self):
	tabs = getIndent()
	global tabcounter
	pycode = ""
	pycode += tabs + self.children[0].compile()
	pycode += tabs + "while " + self.children[1].compile() + ":\n"
	tabcounter += 1
	pycode += self.children[3].compile()
	pycode += self.children[2].compile()
	tabcounter -= 1

	# Version pythonique complexe avec un vrai for (traite juste < et <=)
	# if (type(self.children[0]) is AST.AssignNode):
	# 	pycode += tabs + "for " + self.children[0].children[0].compile() + " in xrange(" + self.children[0].children[1].compile() + ", "
	# if (type(self.children[1]) is AST.ComparatorNode):
	# 	if (self.children[1].op == "<"):
	# 		pycode += self.children[1].children[1].compile() + ", "
	# 	elif (self.children[1].op == "<="):
	# 		number = int(self.children[1].children[1].compile()) + 1
	# 		pycode += "{}, ".format(number)
	# if (type(self.children[2]) is AST.AssignNode):
	# 	pycode += self.children[2].children[1].children[1].compile() + "):\n"
	# tabcounter += 1
	# pycode += self.children[3].compile()
	# tabcounter -= 1
	return pycode

# Noeud de test if
@addToClass(AST.IfNode)
def compile(self):
	tabs = getIndent()
	global tabcounter
	pycode = ""
	pycode += tabs + "if " + self.children[0].compile() + ":\n"
	tabcounter += 1
	pycode += self.children[1].compile()
	tabcounter -= 1
	if(len(self.children) > 2):
		pycode += tabs + "else:\n"
		tabcounter += 1
		pycode += self.children[2].compile()
		tabcounter -= 1
	return pycode

# Noeud de comparaison
@addToClass(AST.ComparatorNode)
def compile(self):
	pycode = ""
	pycode += "(" + self.children[0].compile() + " "
	pycode += self.op
	pycode += " " + self.children[1].compile() + ")"
	return pycode

# Noeud de return
@addToClass(AST.ReturnNode)
def compile(self):
	tabs = getIndent()
	pycode = ""
	if (len(self.children) > 0):
		pycode += tabs + "return " + self.children[0].compile() + "\n"
	else:
		pycode += tabs + "return\n"
	return pycode

# Noeud de saut break
@addToClass(AST.BreakNode)
def compile(self):
	tabs = getIndent()
	pycode = ""
	pycode += tabs + "break\n"
	return pycode

# Noeud de saut continue
@addToClass(AST.ContinueNode)
def compile(self):
	tabs = getIndent()
	pycode = ""
	pycode += tabs + "continue\n"
	return pycode

# Noeud de déclaration
@addToClass(AST.DeclarationNode)
def compile(self):
	tabs = getIndent()
	global context
	global contextcounter
	global tabcounter
	global vars_tab
	number = 0
	pycode = ""
	# Si ce n'est pas une fonction
	if not self.func:
		# Gestion des types
		vars_tab[context[contextcounter]][self.tok] = self.type.lower()
		pycode += tabs + self.tok + " = None\n"
	# Si c'est une fonction
	else:
		# Gestion des types
		contextcounter += 1
		context.append(self.tok)
		vars_tab[context[contextcounter]] = {}
		# Gstion du code python
		pycode += tabs + "def " + self.tok + "("
		if (len(self.children) > 1):
			pycode += self.children[0].compile()
			number += 1
		pycode += "):\n"
		tabcounter += 1
		pycode += tabs + self.children[number].compile()
		tabcounter -= 1
		pycode += "\n"
		# Suppression du contexte crée après le parcours des enfants du noeud
		del vars_tab[context[contextcounter]]
		context.pop(contextcounter)
		contextcounter -= 1
	return pycode

# Noeud de paramètres
@addToClass(AST.ParamListNode)
def compile(self):
	global context
	global contextcounter
	global vars_tab
	# Gestion des types
	for c in self.children:
		vars_tab[context[contextcounter]][c.tok] = c.type.lower()
	# Gestion du code python
	pycode = ""
	for c in self.children[:-1]:
		pycode += c.tok + ", "
	pycode += self.children[-1].tok
	return pycode

# Noeud d'arguments
@addToClass(AST.ArgListNode)
def compile(self):
	pycode = ""
	for c in self.children[:-1]:
		pycode += c.tok + ", "
	pycode += self.children[-1].tok
	return pycode

# Noeud d'appel de méthodes
@addToClass(AST.FunctionExpressionNode)
def compile(self):
	pycode = ""
	if (len(self.children) > 0):
		pycode += self.tok + "(" + self.children[0].compile() + ")"
	else:
		pycode += self.tok + "()"
	return pycode

#  ---------------------------------------------------------------
#  TYPE MANAGEMENT
#  ---------------------------------------------------------------

def type_checking(firstChild, secondChild):
	'''Méthode de contrôle des types entre deux enfants et retourne le type des
	noeuds s'ils correspondent ou affiche une erreur avec une interruption du programme.
	'''
	global vars_tab
	global contextcounter
	global contexterror
	global context
	# Si le premier enfant est de type inconnu, on va rechercher son type
	if firstChild.type == None:
		type_finding(firstChild)
	# Si le second enfant est de type inconnu, on va rechercher son type
	if secondChild.type == None:
		type_finding(secondChild)
	# Si le second enfant est un appel de méthodes
	if (type(secondChild) is AST.FunctionExpressionNode):
		# On retourne le type de l'enfant
		if firstChild.type != None:
			return firstChild.type.lower()
		# Sinon on a une erreur
		else:
			contexterror = True
	# On vérifie alors les types des deux enfants avec le tableau des relations
	if firstChild.type in types_dict and secondChild.type in types_dict:
		# S'ils correspondent, on retourne le type
		if types_dict[firstChild.type] == types_dict[secondChild.type]:
			return firstChild.type.lower()
		# Sinon on a une drôle d'erreur
		else:
			contexterror = True
	# Sinon on a une erreur
	else:
		contexterror = True
	# Si une erreur est détectée, le programme affiche le contexte dans lequel l'erreur se trouve et termine le programme
	if contexterror:
		print("There are some assignations/operations with different types in " + context[contextcounter] + " context.\nCompilation aborted.")
		sys.exit(0)

def type_finding(unknownChild):
	'''Méthode de recherche d'un type pour un noeud donné'''
	global vars_tab
	global contextcounter
	global contexterror
	global context
	# Si c'est un noeud d'opération binaire, on applique la fonction recursivement
	if (len(unknownChild.children) == 2) and (type(unknownChild) is AST.OpNode):
		unknownChild.type = type_checking(unknownChild.children[0], unknownChild.children[1])
	# Si c'est un noeud d'opération unaire, on va chercher le type de l'enfant
	elif (len(unknownChild.children) == 1) and (type(unknownChild) is AST.OpNode):
		# Si l'enfant a un type, on donne ce type au parent
		if unknownChild.children[0].type != None:
			unknownChild.type = unknownChild.children[0].type
		# Sinon on va voir s'il appartient aux variables existantes
		elif unknownChild.children[0].tok in vars_tab[context[contextcounter]]:
			unknownChild.type = vars_tab[context[contextcounter]][unknownChild.children[0].tok]
		# Sinon on a à faire à quelque chose d'autre
		else:
			contexterror = True
	# Si ce n'est pas un noeud d'opération, on va voir s'il appartient aux variables existantes
	elif unknownChild.tok in vars_tab[context[contextcounter]]:
		unknownChild.type = vars_tab[context[contextcounter]][unknownChild.tok]

#  ---------------------------------------------------------------
#  MAIN COMPIER ACTIVITY
#  ---------------------------------------------------------------

if __name__ == "__main__":
    from parser_C2PC import parse
    import sys, os
	# Lecture du programme C et création de l'AST
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print(ast)
	# Création du code python d'après les noeuds de l'AST
    compiled = ast.compile()
	# Création d'un nouveau fichier et écriture de code python à l'intérieur
    name = os.path.splitext(sys.argv[1])[0] + '.py'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)
