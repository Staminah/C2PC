import AST
from AST import addToClass

tabcounter = 0

def getIndent():
	tab = ""
	for i in range(0, tabcounter):
		tab += "\t"
	return tab

# noeud de programme
# retourne la suite d'opcodes de tous les enfants
@addToClass(AST.ProgramNode)
def compile(self):
	bytecode = ""
	for c in self.children:
		bytecode += c.compile()
	return bytecode

# noeud terminal
@addToClass(AST.TokenNode)
def compile(self):
	bytecode = ""
	bytecode += "%s" % self.tok
	return bytecode

# noeud d'assignation de variable
@addToClass(AST.AssignNode)
def compile(self):
	tabs = getIndent()
	bytecode = ""
	bytecode += tabs
	bytecode += "%s = %s\n" % (self.children[0].tok, self.children[1].compile())
	# bytecode += self.children[1].compile()
	return bytecode

# noeud d'affichage
@addToClass(AST.PrintNode)
def compile(self):
	tabs = getIndent()
	global tabcounter
	bytecode = ""
	bytecode += tabs + "print("
	bytecode += self.children[0].compile()
	bytecode += ")"
	return bytecode

# noeud d'opération arithmétique
@addToClass(AST.OpNode)
def compile(self):
	bytecode = ""
	bytecode += "(" + self.children[0].compile()
	bytecode += self.op
	bytecode += self.children[1].compile() + ")"
	return bytecode

# noeud de boucle while
@addToClass(AST.WhileNode)
def compile(self):
	tabs = getIndent()
	global tabcounter
	bytecode = ""
	bytecode += tabs + "while " + self.children[0].compile() + ":\n"
	tabcounter += 1
	bytecode += self.children[1].compile()
	tabcounter -= 1
	return bytecode

# noeud de boucle for
@addToClass(AST.ForNode)
def compile(self):
	tabs = getIndent()
	global tabcounter
	bytecode = ""
	bytecode += tabs + self.children[0].compile()
	bytecode += tabs + "while " + self.children[1].compile() + ":\n"
	tabcounter += 1
	bytecode += self.children[3].compile()
	bytecode += self.children[2].compile()
	tabcounter -= 1

	# Version pythonique complexe avec un vrai for (traite < et <=)
	bytecode += "'''\n"
	if (type(self.children[0]) is AST.AssignNode):
		bytecode += tabs + "for " + self.children[0].children[0].compile() + " in xrange(" + self.children[0].children[1].compile() + ", "
	if (type(self.children[1]) is AST.ComparatorNode):
		if (self.children[1].op == "<"):
			bytecode += self.children[1].children[1].compile() + ", "
		elif (self.children[1].op == "<="):
			number = int(self.children[1].children[1].compile()) + 1
			bytecode += "{}, ".format(number)
	if (type(self.children[2]) is AST.AssignNode):
		bytecode += self.children[2].children[1].children[1].compile() + "):\n"
	tabcounter += 1
	bytecode += self.children[3].compile()
	tabcounter -= 1
	bytecode += "'''\n"

	return bytecode

# noeud de test if
@addToClass(AST.IfNode)
def compile(self):
	tabs = getIndent()
	global tabcounter
	bytecode = ""
	bytecode += tabs + "if " + self.children[0].compile() + ":\n"
	tabcounter += 1
	bytecode += self.children[1].compile()
	tabcounter -= 1
	if(len(self.children) > 2):
		bytecode += tabs + "else:\n"
		tabcounter += 1
		bytecode += tabs + self.children[2].compile()
		tabcounter -= 1

	return bytecode

# noeud de comparaison
@addToClass(AST.ComparatorNode)
def compile(self):
	bytecode = ""
	bytecode += "(" + self.children[0].compile()
	bytecode += self.op
	bytecode += self.children[1].compile() + ")"
	return bytecode


if __name__ == "__main__":
    from parser_C2PC import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print(ast)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.py'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)
