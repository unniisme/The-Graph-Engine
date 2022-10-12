
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

    INVALID_STATE = 0
    INVALID_TRANSITION = 1
    NON_CLOSURE = 2


    def __init__(self, ercode, defaulter = None):
        if (ercode == AutomataError.INVALID_STATE):
            print ("Invalid State")
        elif (ercode == AutomataError.INVALID_TRANSITION):
            print ("Invalid Transition")
        elif (ercode == AutomataError.NON_CLOSURE):
            print ("Invalid Automata")



if __name__=="__main__":

    Q = {0,1}
    sig = "01"
    delt = {}

    for q in Q:
        for a in sig:
            if q not in delt:
                delt[q] = {}
            print(f'del{(q,a)} = ', end="")
            delt[q][a] = int(input())

    dfa = stringDFA(Q, sig, delt, 0, {1})

    print(dfa.CheckAccept(input()))