''' Petit module utilitaire pour la construction, la manipulation et la
représentation d'arbres syntaxiques abstraits.

Sûrement plein de bugs et autres surprises. À prendre comme un
"work in progress"...
Notamment, l'utilisation de pydot pour représenter un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. Ca marche, mais le layout n'est
pas toujours optimal...
'''

import pydot

class Node:
    count = 0
    node_type = 'Node (unspecified)'
    shape = 'ellipse'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self,next):
        self.next.append(next)

    def addChildren(self,child):
        self.children.append(child)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of node_type %r: %r\n" % (prefix,type(c),c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.node_type

    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
            label = edgeLabels and len(self.children)-1
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
                #Workaround for a bug in pydot 1.0.2 on Windows:
                #dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.16\bin\dot.exe'})
            return dot

    def threadTree(self, graph, seen = None, col=0):
            colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
            if not seen: seen = []
            if self in seen: return
            seen.append(self)
            new = not graph.get_node(self.ID)
            if new:
                graphnode = pydot.Node(self.ID,label=repr(self), shape=self.shape)
                graphnode.set_style('dotted')
                graph.add_node(graphnode)
            label = len(self.next)-1
            for i,c in enumerate(self.next):
                if not c: return
                col = (col + 1) % len(colors)
                color = colors[col]
                c.threadTree(graph, seen, col)
                edge = pydot.Edge(self.ID,c.ID)
                edge.set_color(color)
                edge.set_arrowsize('.5')
                # Les arrêtes correspondant aux coutures ne sont pas prises en compte
                # pour le layout du graphe. Ceci permet de garder l'arbre dans sa représentation
                # "standard", mais peut provoquer des surprises pour le trajet parfois un peu
                # tarabiscoté des coutures...
                # En commantant cette ligne, le layout sera bien meilleur, mais l'arbre nettement
                # moins reconnaissable.
                edge.set_constraint('false')
                if label:
                    edge.set_taillabel(str(i))
                    edge.set_labelfontcolor(color)
                graph.add_edge(edge)
            return graph

class ProgramNode(Node):
    node_type = 'Program'

class TokenNode(Node):
    node_type = 'token'
    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok

    def __repr__(self):
        return repr(self.tok)

class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self,children)
        self.op = op
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1

    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)

class AssignNode(OpNode):
    node_type = 'AssignmentExrpession'

    def __repr__(self):
        return "%s" % (self.op)

class PrintNode(Node):
    node_type = 'print'

class WhileNode(Node):
    node_type = 'while'

class ForNode(Node):
    node_type = 'for'

class IfNode(Node):
    node_type = 'if'

class ReturnNode(Node):
    node_type = 'return'

class ComparatorNode(OpNode):
    node_type = 'ComparatorExpression'
    pass

class LogicalNode(OpNode):
    node_type = 'LogicalExpression'
    pass

class DeclarationNode(Node):
    node_type = 'DeclarationExpression'
    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok
        self.type = type
        self.func = False
        self.array = False

    def __repr__(self):
        add_str = ""
        if(self.func):
            add_str = "( )"
        if(self.array):
            add_str = "[ ]"
        return "%s %s%s" % (self.type, self.tok, add_str)

    def setFunc(self, val):
        self.func = val

    def setArray(self, val):
        self.array = val

    def setType(self, val):
        self.type = val

class FunctionExpressionNode(DeclarationNode):
    def __repr__(self):
        func_str = ""
        if(self.func):
            func_str = "( )"
        return "%s%s" % (self.tok, func_str)

class EntryNode(Node):
    node_type = 'ENTRY'
    def __init__(self):
        Node.__init__(self, None)

class ParamListNode(Node):
    node_type = 'ParamList'

class ArgListNode(Node):
    node_type = 'ArgList'

def addToClass(cls):
    ''' Décorateur permettant d'ajouter la fonction décorée en tant que méthode
    à une classe.

    Permet d'implémenter une forme élémentaire de programmation orientée
    aspects en regroupant les méthodes de différentes classes implémentant
    une même fonctionnalité en un seul endroit.

    Attention, après utilisation de ce décorateur, la fonction décorée reste dans
    le namespace courant. Si cela dérange, on peut utiliser del pour la détruire.
    Je ne sais pas s'il existe un moyen d'éviter ce phénomène.
    '''
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator
