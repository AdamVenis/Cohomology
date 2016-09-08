from itertools import product, combinations, permutations

class Group():
    def __init__(self, table):
        self.table = table
        self.size = len(table)
        self.elements = range(len(table))

    def op(self, a, b):
        return self.table[a][b]

    def commutative(self):
        for a, b in combinations(self.elements, 2):
            if self.op(a, b) != self.op(b, a):
                return False
        return True


class Func():
    def __init__(self, source, target, mapping):
        self.source = source
        self.target = target
        self.mapping = mapping

    def of(self, x):
        return self.mapping[x]

    def associative(self):
        pass

    def homomorphism(self):
        for a, b in product(self.source.elements, repeat=2):
            if self.target.op(self.of(a), self.of(b)) != self.of(self.source.op(a, b)):
                return False
        return True

    def cocycle(self, action):
        for a, b in product(self.source.elements, repeat=2):
            #print('a,b', a,b)
            #print(self.of(self.source.op(a, b)))
            #print(self.target.op(action.of(a).of(self.of(b)), self.of(a)))

            if (self.of(self.source.op(a, b)) !=
                self.target.op(action.of(a).of(self.of(b)),
                                               self.of(a))):
                return False
        return True

class Action():
    def __init__(self, source, target, mapping):
        # mapping::source->Aut(target)
        self.source = source
        self.target = target
        self.mapping = mapping

    def of(self, x):
        return self.mapping[x]

def cocycles(G, A, action):
    for mapping in product(A.elements, repeat=G.size):
        func = Func(G, A, mapping)
        if func.cocycle(action):
            yield func

def Zmod(n):
    return Group([[(i + j) % n for i in range(n)]
                              for j in range(n)])

def S(n):
    # produces an object representing the symmetric group
    # on n letters.
    # ordering of elements is weird
    # e.g. S3 as <s,t|s^2=t^3=stst=1> is ordered as
    # [1, s, st^2, t, t^2, st]
    def compose(s, t):
        return tuple(s[i] for i in t)

    perms = list(permutations(range(n)))
    mapping = [[0 for i in range(len(perms))] for j in range(len(perms))]
    for i, p1 in enumerate(perms):
        for j, p2 in enumerate(perms):
            p3 = compose(p1, p2)
            mapping[i][j] = perms.index(p3)
    return Group(mapping)

def constant_func(source, target, element):
    return Func(source, target, [element] * source.size)

def identity_func(obj):
    return Func(obj, obj, obj.elements)

def P01():
    # returns 1-cocycles for the group cohomology of G with coefficients in A
    G = Zmod(2)
    A = Zmod(6)
    action = Action(G, A, constant_func(G, None, identity_func(A)).mapping)
    return cocycles(G, A, action)

def P02():
    # returns 1-cocycles for the group cohomology of G with coefficients in A
    G = Zmod(2)
    A = Zmod(6)
    action_mapping = [identity_func(A),
                      Func(A, A, [(A.size - i) % A.size for i in range(A.size)])]
    action = Action(G, A, action_mapping)
    return cocycles(G, A, action)

def P03():
    # returns 1-cocycles for the group cohomology of G with coefficients in A
    G = S(3)
    # s = complex conjugation: acts as flip
    # t = multiply cbrt(2) -> w*cbrt(2): acts trivially
    A = Zmod(6)

    conjugation_action = Func(A, A, [(A.size - i) % A.size for i in range(A.size)])
    action_mapping = [identity_func(A),
                      conjugation_action,
                      conjugation_action,
                      identity_func(A),
                      identity_func(A),
                      conjugation_action]
    action = Action(G, A, action_mapping)
    return cocycles(G, A, action)

P03()