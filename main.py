def tokenize(s):
    s = s.replace(" ", "")
    return list(s)


class LLParser_V1:
    def __init__(self):
        self.lookahead = None
        self.tokens = None

    def error(self, code=0):
        MESSAGES = {
            0: "General Error",
            1: "Wrong LA for S rule"

        }
        message = MESSAGES[code] if code in MESSAGES.keys() else MESSAGES[0]
        message = f"{message} | LA:{self.lookahead} | TOKENS: {self.tokens}"
        raise Exception(message)

    def parse(self, s):
        self.tokens = tokenize(s)
        self.lookahead = self.tokens.pop(0)
        self.S()
        return True

    def consume(self, token):
        if token == self.lookahead:
            if len(self.tokens) > 0:
                self.lookahead = self.tokens.pop(0)
            else:
                self.lookahead = None
                self.tokens = None
        else:
            self.error(0)

    def S(self):
        if self.lookahead in ['a', '(']:
            self.E()
            self.consume('#')
        else:
            self.error(1)

    def E(self):
        if self.lookahead in ['a', '(']:
            self.T()
            self.X()
        else:
            self.error(2)

    def T(self):
        if self.lookahead in ['a']:
            self.consume('a')
        elif self.lookahead in ['(']:
            self.consume('(')
            self.E()
            self.consume(')')
        else:
            self.error(3)

    def X(self):
        if self.lookahead in ['+']:
            self.Z()
        elif self.lookahead in [')', '#']:
            pass
        else:
            self.error(4)

    def Z(self):
        if self.lookahead in ['+']:
            self.consume('+')
            self.T()
            self.X()
        else:
            self.error(5)


class Node:
    def __init__(self, ntype="node", value=None, children=None):
        self.ntype = ntype
        self.value = value
        self.children = children

    def repr(self, n=0):
        self_repr = f"{self.ntype}"
        if self.value is not None:
            self_repr = f"{self_repr} : {self.value}"
        if self.children is not None:
            children_repr = ''.join(f"\n{' ' * (n + 1)}{x.repr(n + 1)}" for x in self.children)
            self_repr = f"{self_repr}{children_repr}"
        return self_repr

    def __repr__(self):
        return self.repr()

    #
    #   BUG!
    #
    def eval(self):

        result = ''
        if self.ntype == 'term' and self.value == 'a':
            return '1'
        elif self.ntype == 'term' and self.value == '+':
            return '+'
        elif self.ntype == 'term' and self.value == '#':
            return ''
        elif self.ntype in 'SEXZ':
            esquerda = self.children[0].eval()
            try:
                direita = self.children[1].eval()
            except:
                direita = ''
            result = esquerda + direita

        # result é a string recontruida com a a tomar os valor de 1
        self.value = eval(result)
        return result


class LLParser:
    def __init__(self):
        self.lookahead = None
        self.tokens = None

    def error(self, code=0):
        MESSAGES = {
            0: "General Error",
            1: "Wrong LA for S rule"

        }
        message = MESSAGES[code] if code in MESSAGES.keys() else MESSAGES[0]
        message = f"{message} | LA:{self.lookahead} | TOKENS: {self.tokens}"
        raise Exception(message)

    def parse(self, s):
        self.tokens = tokenize(s)
        self.lookahead = self.tokens.pop(0)
        return self.S()

    def consume(self, token):
        if token == self.lookahead:
            if len(self.tokens) > 0:
                self.lookahead = self.tokens.pop(0)
            else:
                self.lookahead = None
                self.tokens = None
        else:
            self.error(0)

    def S(self):
        if self.lookahead in ['a', '(']:
            e = self.E()
            self.consume('#')
            return Node(ntype="S", children=[e, Node(ntype="term", value='#')])
        else:
            self.error(1)

    def E(self):
        if self.lookahead in ['a', '(']:
            t = self.T()
            x = self.X(t)
            return Node(ntype="E", children=[x])
        else:
            self.error(2)

    def T(self):
        if self.lookahead in ['a']:
            self.consume('a')
            return Node(ntype="term", value='a')
        elif self.lookahead in ['(']:
            self.consume('(')
            e = self.E()
            self.consume(')')
            return Node(
                ntype="T",
                children=[
                    Node(ntype='term', value='('),
                    e,
                    Node(ntype='term', value=')')])
        else:
            self.error(3)

    def X(self, t):
        if self.lookahead in ['+']:
            z = self.Z()
            return Node(ntype="X", children=[t, z])
        elif self.lookahead in [')', '#']:
            return Node(ntype="X", children=[t])
        else:
            self.error(4)

    def Z(self):
        if self.lookahead in ['+']:
            self.consume('+')
            t = self.T()
            x = self.X(t)
            return Node(ntype="Z", children=[Node(ntype="term", value="+"), x])
        else:
            self.error(5)


s = "a+a#"
parser = LLParser()
ir = parser.parse(s)
print(ir)
ir.eval()
print(ir.value)
