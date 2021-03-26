from sympy.combinatorics import Permutation
import sympy as sym
import copy

#dedscribes a sum of coeff*permutation terms
#[[coeff1,perm1], [coeff2,perm2]...]
class PermAlg(object):
    def __init__(self, initTerms):
        self.e = initTerms

    def __mul__(self, other):
        new = []
        for selfTerm in self.e:
            for otherTerm in other.e:
                newTermCoeff = selfTerm[0]*otherTerm[0]
                newTermPerm = selfTerm[1]*otherTerm[1]
                #newTermPerm = otherTerm[1]*selfTerm[1]
                new.append([newTermCoeff, newTermPerm])

        newAlg = PermAlg(new)
        #maybe dont do this \/ \/
        #newAlg.collectTerms()
        return newAlg

    #makes self a subgoup of a larger (oreq) perm group than self
    #remember Permutation(n) = Id_(sym(n+1))
    def makeSubgroupOf(self, int):
        for term in self.e:
            term[1] = term[1]*Permutation(int)

    #"moves" every permutation up int times
    #e.g. perm(2)(boost
    def boost(self, N):
        #normalises containing group of all perms to largest group
        largestGroup = max([term[1].size for term in self.e]) - 1
        self.makeSubgroupOf(largestGroup)

        cycle1 = list(range(1, largestGroup+1))
        cycle1.append(0)
        cycle1Perm = Permutation(cycle1)
        cycleNPerm = cycle1Perm**N

        for term in self.e:
            term[1] = (~cycleNPerm)*term[1]*cycleNPerm

    def add(self, term):
        self.e.append(term)

    #traces of SU(N) indices
    def trace(self):
        N = sym.Symbol('N')
        runningSum = sym.sympify(0)
        for term in self.e:
            runningSum += term[0] * N**(len(term[1].full_cyclic_form))
        return runningSum

    def multCoeff(self, coeff):
        for term in self.e:
            term[0] = term[0] * coeff

    #groups terms by perm
    def collectTerms(self):
        allPerms = list(set([x[1] for x in self.e]))
        iWherePermOccurs = []
        for perm in allPerms:
            indexes = []
            for i, term in enumerate(self.e):
                if term[1]==perm:
                    indexes.append(i)
            iWherePermOccurs.append(indexes)
        newExp = []
        for k, perm in enumerate(allPerms):
            oldCoeffs = [self.e[i][0] for i in iWherePermOccurs[k]]
            newCoeff = sum(oldCoeffs)
            #print(newCoeff)
            newExp.append([newCoeff,perm])

        self.e = copy.copy(newExp)
