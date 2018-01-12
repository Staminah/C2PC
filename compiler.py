import AST
from AST import addToClass

context = ["main"]
contextcounter = 0

tabcounter = 0
types_dict = {'int':'int',
			  'short':'int',
	          'long':'int',
	          'char':'char',
			  'string':'char',
	          'float':'float',
	          'double':'float'}

vars_tab = {}
vars_tab[context[contextcounter]] = {}

# indentation python
def getIndent():
	tab = ""
	for i in range(0, tabcounter):
		tab += "\t"
	return tab

# noeud de programme
@addToClass(AST.ProgramNode)
def compile(self):
	pycode = ""
	for c in self.children:
		pycode += c.compile()
	return pycode

# noeud terminal
@addToClass(AST.TokenNode)
def compile(self):
	pycode = ""
	pycode += "%s" % self.tok
	return pycode

# noeud d'assignation de variable
@addToClass(AST.AssignNode)
def compile(self):
	# -- types
	if (type(self.children[0]) is AST.DeclarationNode):
		vars_tab[context[contextcounter]][self.children[0].tok] = self.children[0].type.lower()
	self.type = type_checking(self.children[0], self.children[1])
	# -- code python
	tabs = getIndent()
	pycode = ""
	pycode += tabs
	pycode += "%s %s %s\n" % (self.children[0].tok, self.op, self.children[1].compile())
	return pycode

# noeud d'affichage
@addToClass(AST.PrintNode)
def compile(self):
	tabs = getIndent()
	pycode = ""
	pycode += tabs + "print("
	pycode += self.children[0].compile()
	pycode += ")"
	return pycode

# noeud d'opération arithmétique
@addToClass(AST.OpNode)
def compile(self):
	global vars_tab
	global context
	global contextcounter

	pycode = ""
	# Binaire
	if (len(self.children) == 2):
		# -- types
		if self.children[0].type == None and self.children[0].tok in vars_tab[context[contextcounter]]:
			self.children[0].type = vars_tab[context[contextcounter]][self.children[0].tok]
		elif self.children[1].type == None and self.children[1].tok in vars_tab[context[contextcounter]]:
			self.children[1].type = vars_tab[context[contextcounter]][self.children[1].tok]
		self.type = type_checking(self.children[0], self.children[1])
		# -- code python
		pycode += "(" + self.children[0].compile() + " "
		pycode += self.op
		pycode += " " + self.children[1].compile() + ")"

	# Unaire
	elif (len(self.children) == 1):
		if self.op == "!":
			pycode += "not " + self.children[0].compile()
		elif self.op == "+":
			pycode += self.children[0].compile()
		else:
			pycode += self.op + self.children[0].compile()
	return pycode

# noeud de boucle while
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

# noeud de boucle for
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

# noeud de test if
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

# noeud de comparaison
@addToClass(AST.ComparatorNode)
def compile(self):
	pycode = ""
	pycode += "(" + self.children[0].compile() + " "
	pycode += self.op
	pycode += " " + self.children[1].compile() + ")"
	return pycode

# noeud de return
@addToClass(AST.ReturnNode)
def compile(self):
	tabs = getIndent()
	pycode = ""
	if (len(self.children) > 0):
		pycode += tabs + "return " + self.children[0].compile() + "\n"
	else:
		pycode += tabs + "return\n"

	return pycode

# noeud break
@addToClass(AST.BreakNode)
def compile(self):
	tabs = getIndent()
	pycode = ""
	pycode += tabs + "break\n"
	return pycode

# noeud continue
@addToClass(AST.ContinueNode)
def compile(self):
	tabs = getIndent()
	pycode = ""
	pycode += tabs + "continue\n"
	return pycode

# noeud de déclaration
@addToClass(AST.DeclarationNode)
def compile(self):
	tabs = getIndent()
	global context
	global contextcounter
	global tabcounter
	global vars_tab

	number = 0
	pycode = ""
	if not self.func:
		vars_tab[context[contextcounter]][self.tok] = self.type.lower()
		pycode += tabs + self.tok + " = None\n"
	else:
		contextcounter += 1
		context.append(self.tok)
		vars_tab[context[contextcounter]] = {}

		pycode += tabs + "def " + self.tok + "("
		if (len(self.children) > 1):
			pycode += self.children[0].compile()
			number += 1
		pycode += "):\n"
		tabcounter += 1
		pycode += tabs + self.children[number].compile()
		tabcounter -= 1
		pycode += "\n"

		del vars_tab[context[contextcounter]]
		context.pop(contextcounter)
		contextcounter -= 1
	return pycode

# noeud de paramètres
@addToClass(AST.ParamListNode)
def compile(self):
	# -- types
	global context
	global contextcounter
	global vars_tab
	for c in self.children:
		vars_tab[context[contextcounter]][c.tok] = c.type.lower()
	# -- code python
	pycode = ""
	for c in self.children[:-1]:
		pycode += c.tok + ", "
	pycode += self.children[-1].tok
	return pycode

# noeud d'arguments
@addToClass(AST.ArgListNode)
def compile(self):
	pycode = ""
	for c in self.children[:-1]:
		pycode += c.tok + ", "
	pycode += self.children[-1].tok
	return pycode

# noeud d'appel de méthodes
@addToClass(AST.FunctionExpressionNode)
def compile(self):
	pycode = ""
	if (len(self.children) > 0):
		pycode += self.tok + "(" + self.children[0].compile() + ")"
	else:
		pycode += self.tok + "()"
	return pycode

def type_checking(firstChild, secondChild):
	global vars_tab
	global contextcounter
	global context
	error = False

	if firstChild.type == None:
		if (len(firstChild.children) == 2) and (type(firstChild) is AST.OpNode):
			firstChild.type = type_checking(firstChild.children[0], firstChild.children[1])
		elif (len(firstChild.children) == 1) and (type(firstChild) is AST.OpNode):
			if firstChild.children[0].type != None:
				firstChild.type = firstChild.children[0].type
			elif firstChild.children[0].tok in vars_tab[context[contextcounter]]:
				firstChild.type = vars_tab[context[contextcounter]][firstChild.children[0].tok]
			else:
				error = True
		elif firstChild.tok in vars_tab[context[contextcounter]]:
			firstChild.type = vars_tab[context[contextcounter]][firstChild.tok]
	if secondChild.type == None:
		if (len(secondChild.children) == 2) and (type(secondChild) is AST.OpNode):
			secondChild.type = type_checking(secondChild.children[0], secondChild.children[1])
		elif (len(secondChild.children) == 1) and (type(secondChild) is AST.OpNode):
			if secondChild.children[0].type != None:
				secondChild.type = secondChild.children[0].type
			elif secondChild.children[0].tok in vars_tab[context[contextcounter]]:
				secondChild.type = vars_tab[context[contextcounter]][secondChild.children[0].tok]
			else:
				error = True
		elif secondChild.tok in vars_tab[context[contextcounter]]:
			secondChild.type = vars_tab[context[contextcounter]][secondChild.tok]

	if (type(secondChild) is AST.FunctionExpressionNode):
		if firstChild.type != None:
			return firstChild.type.lower()
		else:
			error = True
	elif firstChild.type in types_dict and secondChild.type in types_dict:
		if types_dict[firstChild.type] == types_dict[secondChild.type]:
			return firstChild.type.lower()
		else:
			error = True
	else:
		error = True

	if error:
		print("There are some assignations/operations with different types in " + context[contextcounter] + " context.\nCompilation aborted.")
		sys.exit(0)

if __name__ == "__main__":
    from parser_C2PC import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print(ast)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.py'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)
