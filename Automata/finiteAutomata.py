import itertools

class Uniq:

    x = 100000

    def setVal(x):
        Uniq.x = x

    def getVal():
        Uniq.x += 1
        return Uniq.x

class FiniteAutomata:
    
    def __init__(self, Q : set, sigma : set, transitionTable : dict, s, F : set):
        self.Q = Q
        self.sigma = sigma
        self.transitionTable = transitionTable
        self.s = s
        self.F = F

    def delta(self, q, a):
        pass

    def deltaCap(self, q, s : list):
        pass

    def CheckAccept(self, s : list):
        pass

class DFA(FiniteAutomata):

    def __init__(self, Q : set, sigma : set, transitionTable : dict, s, F : set):
        for q in Q:
            try:
                for x in sigma:
                    if transitionTable[q][x] not in Q:
                        raise AutomataError(AutomataError.NON_CLOSURE)
            except KeyError:
                raise AutomataError(AutomataError.NON_CLOSURE)
            except AutomataError as e:
                raise e
            except Exception as e:
                raise e

        self.Q = Q
        self.sigma = sigma
        self.transitionTable = transitionTable
        self.s = s
        self.F = F       



    def delta(self, q, a):
        if q not in self.Q:
            raise AutomataError(AutomataError.INVALID_STATE)
        if a not in self.sigma:
            raise AutomataError(AutomataError.INVALID_TRANSITION)

        return self.transitionTable[q][a]

    def delta_cap(self, q, s : list):
        if len(s) == 1:
            return self.delta(q, s[0])
        if len(s) == 0:
            return q
        
        return self.delta(self.delta_cap(q, s[:-1]), s[-1])

    def CheckAccept(self, x):
        return self.delta_cap(self.s, x) in self.F


    def CheckEq(M1, M2):
        """
        Check if 2 DFAs are equal.
        Note that the names of states have to be equal.
        Does not check for polymorphism
        """
        if M1.Q != M2.Q:
            return False

        if M1.sigma != M2.sigma:
            return False

        if M1.s != M2.s:
            return False

        if M1.F != M2.F:
            return False

        for a in M1.sigma:
            for q in M1.Q:
                if M1.delta(q, a) != M2.delta(q,a):
                    return False
                    
        return True


    def MinimizeDFA(dfa):
        marked = {}
        partitions = {}
        partitionTransitions = {}
        for p in dfa.Q:
            for q in dfa.Q:
                if (p in F) and (q not in F):
                    marked.add({p,q})

        oldmarked = {}

        while oldmarked != marked:
            oldmarked = marked.copy()

            for a in dfa.sigma:
                for p in dfa.Q:
                    for q in dfa.Q:
                        if {p,q} in marked:
                            continue

                        if {dfa.delta(p, a), dfa.delta(q, a)} in marked:
                            marked.add({p,q})
                        else:
                            pass
                        ##Finnish  


    def __str__(self):
        out = "Start: " + str(self.s) + "\tAccept: " + str(self.F) + "\n"
        for q in self.Q:
            out += str(q)
            out += "\n"

            for a in self.sigma:
                out += "\t" + str(a) + " : " + str(self.delta(q,a))
                out += "\n"
        return out


class stringDFA(DFA):

    def __init__(self, Q : set, sigma : str, transitionTable : dict, s, F : set):

        super().__init__(Q, set([i for i in sigma]), transitionTable, s, F)

    def delta_cap(self, q, s : str):
        if len(s) == 1:
            return self.delta(q, s)
        if len(s) == 0:
            return q
        
        return self.delta(self.delta_cap(q, s[:-1]), s[-1])


class AutomataError(Exception):

    INVALID_STATE = "Invalid State"
    INVALID_TRANSITION = "Invalid Transition"
    NON_CLOSURE = "Invalid Automata"


    def __init__(self, ercode, defaulter = None):
        self.defaulter = defaulter


class NFA(FiniteAutomata):

    def __init__(self, Q : set, sigma : set, transitionTable : set, S : set, F : set):
        self.Q = Q
        self.sigma = sigma.union({None})  #None being epsilon
        self.transitionTable = transitionTable
        self.S = S
        self.F = F 

    def delta(self, q, a = None) -> set:
        if q not in self.Q:
            raise AutomataError(AutomataError.INVALID_STATE)
        if a not in self.sigma:
            raise AutomataError(AutomataError.INVALID_TRANSITION)

        if a == None:
            # Epsilon case
            if a in self.transitionTable[q]:
                return self.transitionTable[q][a].union({q})
            return {q}
        if a not in self.transitionTable[q]:
            # Phi case
            return set([])


        return self.transitionTable[q][a]

    
    def delta_cap(self, A : set, s : list):
        if len(s) == 0:
            for q in A:
                A = A.union(self.delta(q))
            return A
        
        B = set([])
        for q in self.delta_cap(self.delta_cap(A,[]), s[:-1]):
            B = B.union(self.delta(q, s[-1]))

        return B.union(self.delta_cap(B, []))

    def CheckAccept(self, s : list):
        if self.delta_cap(self.S, s).intersection(self.F) == set([]):
            return False
        return True

    #Kleene Algebra
    def Concat(N1, N2):
        """
        Currently assumes that state names are already different. Screws up otherwise
        """
        if N1.sigma != N2.sigma:
            raise AutomataError

        transitionTable = N1.transitionTable.copy()
        transitionTable.update(N2.transitionTable)
        for q in N1.F:
            if None in transitionTable[q].keys():
                transitionTable[q][None].update(N2.S)
            else:
                transitionTable[q][None] = N2.S

        return NFA(set.union(N1.Q,N2.Q), N1.sigma, transitionTable, N1.S, N2.F)

    def Union(N1, N2):
        if N1.sigma != N2.sigma:
            raise AutomataError

        newState = Uniq.getVal()
        Q = set.union(N1.Q, N2.Q).union({newState})
        transitionTable = N1.transitionTable.copy()
        transitionTable.update(N2.transitionTable)
        transitionTable[newState] = {None : set.union(N1.S, N2.S)}

        return NFA(Q, N1.sigma, transitionTable, {newState}, set.union(N1.F,N2.F))

    def Closure(N1):
        newState = Uniq.getVal()
        Q = N1.Q.union({newState})
        transitionTable = N1.transitionTable.copy()
        transitionTable[newState] = {None : N1.S}
        for q in N1.F:
            if None in transitionTable[q].keys():
                transitionTable[q][None].update(N1.S)
            else:
                transitionTable[q][None] = N1.S

        return NFA(Q, N1.sigma, transitionTable, {newState}, N1.F.union({newState}))



    def __str__(self):
        out = "Start: " + str(self.S) + "\tAccept: " + str(self.F) + "\n"
        for q in self.Q:
            out += str(q)
            out += "\n"

            for a in self.sigma:
                out += "\t" + str(a) + " : " + str(self.delta(q,a))
                out += "\n"
        return out


def NFAtoDFA(nfa : NFA) -> DFA:
    subsets = []
    transitionTable = {}
    for i in range(len(Q)+1):
        subsets += [set(i) for i in itertools.combinations(nfa.Q, i)]   

    s = subsets.index(nfa.S)
    
    F = set()
    for i, subset in enumerate(subsets):
        if subset.intersection(nfa.F) != set([]):
            F.add(i)

    for i,A in enumerate(subsets):
        transitionTable[i] = {}
        for x in nfa.sigma:
            transitionTable[i][x] = subsets.index(nfa.delta_cap(A, [x]))

    return DFA(list(range(len(subsets))), nfa.sigma.difference({None}), transitionTable, s, F)




if __name__=="__main__":

    Uniq.setVal(-1)
    Q = [Uniq.getVal() for i in range(2)]
    sig = {"0", "1"}
    delt1 = {Q[0] : {"0" : {0}, "1":{0,1}}, Q[1] : {}}
    nfa1 = NFA(set(Q), sig, delt1, {Q[0]}, {Q[1]})

    Q = [Uniq.getVal() for i in range(3)]
    delt2 = {Q[0] : {"0" : {Q[1], Q[0]}, 
                    "1" : {Q[0]}},
            Q[1] : {"1" : {Q[2]}},
            Q[2] : {"0" : {Q[2]},
                    "1" : {Q[2]}}}
    nfa2 = NFA(Q, sig, delt2, {Q[0]}, {Q[2]})

    nfa = nfa1.Closure()

    print(nfa1)
    print(nfa2)
    print(nfa)

    print(nfa.CheckAccept(input()))