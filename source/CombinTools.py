from nlnum import lrcoef
from Diagram import Diagram
from Tableau import Tableau
from PermAlg import PermAlg
import itertools as iter
from more_itertools import distinct_permutations
import copy
import numpy as np
import pprint
from sympy.combinatorics import Permutation
import sympy as sym
import pdb

'''
copied from:
https://arxiv.org/pdf/0909.2331.pdf
http://jeromekelleher.net/generating-integer-partitions.html
'''
def partitions(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]


def partitionProduct(p1, p2):
    l1 = p1.p
    l2 = p2.p

    totalSum = sum(l1) + sum(l2)
    lambdas = list(partitions(totalSum))
    #because partitions from partitions are increasing
    lambdas = [x[::-1] for x in lambdas]
    coeffs = [lrcoef(l, l1, l2) for l in lambdas]
    return [[l, coeffs[i]] for i,l in enumerate(lambdas) if coeffs[i] != 0]


def printSum(sum):
    for term in sum:
        p,coeff = term
        d = Diagram(p)
        print(coeff)
        print(d.printStr())


def prefix(word):
    for i in range(1, len(word)+1):
        yield word[0:i]


def isYamanouchi(word, allIntsSorted):
    #word should be list of ints

    for pre in prefix(word):
        counts = [pre.count(x) for x in allIntsSorted]
        if sorted(counts, reverse=True) != counts:
            return False
    return True


def placementObeysColumnRule(placement, holes):
    valuesToPlace = sorted(set(placement))
    for val in valuesToPlace:
        columnsWithVal = [hole[1] for i,hole in enumerate(holes) if placement[i]==val]
        #if there are any repeats
        if len(set(columnsWithVal)) != len(columnsWithVal):
            return False
    return True


def validPlacementWords(p1,p2,p):
    assert sum(p1.p) + sum(p2.p) == sum(p.p), "Diagrams do not have valid number of boxes"

    #tableaux of shape p in product p1 x p2
    holes = p1.diagramComplementFrom(p)

    placementWord = []
    for i, rowLen in enumerate(p2.p):
        for j in range(rowLen):
            placementWord.append(i+1)
    allIntsSorted = list(range(1,len(p2.p)+1))

    #more_itertools.distinct_permutations is used because there are typically many
    #identical elements in placementWord
    allPermutations = distinct_permutations(placementWord)

    yamanouchiPlacements = []
    for perm in allPermutations:
        if isYamanouchi(perm, allIntsSorted):
            yamanouchiPlacements.append(perm)
    #yamanouchiPlacements = list(filter(isYamanouchi, distinct_permutations(placementWord)))
    #print('#yam: ' + str(len(yamanouchiPlacements)))

    yamanouchiColumnPlacements = []
    for p in yamanouchiPlacements:
        if placementObeysColumnRule(p,holes):
            yamanouchiColumnPlacements.append(p)
    #print('#yamCol: ' + str(len(yamanouchiColumnPlacements)))

    validPlacements = []
    for p in yamanouchiColumnPlacements:
        if p1.fullPlacementMakesDiagram(p,holes):
            validPlacements.append(p)
    #print('#yamColValid: ' + str(len(validPlacements)))

    return validPlacements


#now gives std tableaux
def tableauxInProduct(p1,p2,p):
    validPlacements = validPlacementWords(p1, p2, p)
    t1 = Tableau(canonical=True, partition=p1.p)
    t2 = Tableau(canonical=True, partition=p2.p, start=sum(p1.p)+1)
    holes = p1.diagramComplementFrom(p)

    #initially place the canonical grid of t1 in the grid of t
    t1Grid = t1.getGrid()
    t = Tableau(flat=True, partition=p.p)
    tGrid = t.getGrid()

    for idx, val in np.ndenumerate(t1Grid):
        tGrid[idx] = val

    tableaux = []
    for placement in validPlacements:
        t2Copy = copy.deepcopy(t2)
        tGridCopy = copy.deepcopy(tGrid)


        #   \/\/ all of this is ridiculous \/\/
        holesWithRowPlacements = [[h[0], h[1], placement[i]] for i, h in enumerate(holes)]
        sortPow = max(max([x[1] for x in holes]),max([x[0] for x in holes]))
        #sort by placement row, then hole row, then by hole column
        sorterFunc = lambda x: sortPow**(2*x[2]) + sortPow**(1*x[0]) + x[1]
        holesWithRowPlacements = sorted(holesWithRowPlacements, key=sorterFunc)
        #print(placement)
        #print(holesWithRowPlacements)

        for holeWithRowPlacement in holesWithRowPlacements:
            holeRow, holeCol, rowPlacement = holeWithRowPlacement
            tGridCopy[holeRow, holeCol] = t2Copy.popFromRowLeft(rowPlacement-1)


        tFinal = Tableau.tableauFromGrid(tGridCopy)
        #print(tFinal.printStr())
        tableaux.append(tFinal)
    return tableaux

#tableauxProduct in  normal orientation
def tableauxProduct(p1, p2):
    totalBoxes = sum(p1.p) + sum(p2.p)
    parts = partitions(totalBoxes)
    tabs = []
    for part in parts:
        sortPart = sorted(part, reverse=True)
        #print(sortPart)
        if lrcoef(sortPart, p1.p, p2.p) != 0:
            tabs.extend(tableauxInProduct(p1,p2,Diagram(sortPart)))
    return tabs


#see start of ch. 5 Cvitanovic
#this is (5.2)
def reverseTableauxProduct(p, revP):
    assert sum(revP.p) >= sum(p.p), "Reversed rep. needs to have more boxes than normal rep"
    leftOverBoxes = sum(revP.p) - sum(p.p)
    parts = partitions(leftOverBoxes)
    tabs = []
    for part in parts:
        sortPart = sorted(part, reverse=True)
        if lrcoef(revP.p, sortPart, p.p) != 0:
            tabs.extend(tableauxInProduct(Diagram(sortPart), p, revP))
    return tabs

#perm \subset largerSet
#everything in largerset \ perm is left in the original order
#perm should have a natural order e.g. ints
def permutationInsideLargerSet(perm, largerSet):
    orderedPerm = sorted(perm)
    largePerm = copy.deepcopy(largerSet)
    indexesToPermute = [i for x,i in enumerate(largerSet) if x in perm]
    for pos, index in enumerate(indexesToPermute):
        largePerm[index] = perm[pos]
    return largePerm

def eval3j(d1, d2, d12, vPerm):
    assert sum(d1.p) + sum(d2.p) == sum(d12.p), "Boxes need to add up!"
    totalBoxes = sum(d12.p)

    #makeVperm the right kind of object
    vPermAlg = PermAlg([[1,vPerm]])
    vPermAlg.makeSubgroupOf(totalBoxes-1)
    vPermInvAlg = PermAlg([[1,~vPerm]])
    vPermInvAlg.makeSubgroupOf(totalBoxes-1)

    yp1 = d1.youngProj()
    yp2 = d2.youngProj()
    yp12 = d12.youngProj()

    #just making sure
    yp1.makeSubgroupOf(totalBoxes-1)
    yp2.makeSubgroupOf(totalBoxes-1)

    #yp2 needs boosted out of the way of yp1
    #print(yp2.e)
    yp2.boost(sum(d1.p))
    #print(yp2.e)

    #print(yp1.e)
    print(yp2.e)
    print(yp12.e)
    print(vPermAlg.e)


    total3j = yp1 * yp2 * vPermAlg * yp12 * vPermInvAlg
    #return total3j.trace()
    return total3j

def eval3jTab(d1, d2, t12):
    d12 = Diagram(t12.partition())
    vPerm = t12.permutation()
    return eval3j(d1, d2, d12, vPerm)

#d = diagram
#t = tableau
#this will be readable ONLY with Cvitanovic pg100 (6j symbols)
def eval6jTab(dX, dW, dV, tU, tZ, tY):
    assert sum(dX.p) + sum(dW.p) == sum(tU.partition()), "boxes must add!"
    assert sum(dV.p) + sum(dW.p) == sum(tZ.partition()), "boxes must add!"
    assert sum(dX.p) + sum(dW.p) + sum(dV.p) == sum(tY.partition()), "boxes must add!"

    #total boxes is a totally bad name
    #should be totalLines
    totalBoxes = sum(tY.partition())

    dU = Diagram(tU.partition())
    dZ = Diagram(tZ.partition())
    dY = Diagram(tY.partition())
    vU = Permutation(tU.permutation())
    vZ = Permutation(tZ.permutation())
    vY = Permutation(tY.permutation())

    vPermU = PermAlg([[1,vU]])
    vPermUInv = PermAlg([[1,~vU]])
    vPermZ = PermAlg([[1,vZ]])
    vPermZInv = PermAlg([[1,~vZ]])
    vPermY = PermAlg([[1,vY]])
    vPermYInv = PermAlg([[1,~vY]])

    ypX = dX.youngProj()
    ypW = dW.youngProj()
    ypV = dV.youngProj()
    ypU = dU.youngProj()
    ypZ = dZ.youngProj()
    ypY = dY.youngProj()

    ypX.makeSubgroupOf(totalBoxes-1)
    ypW.makeSubgroupOf(totalBoxes-1)
    ypV.makeSubgroupOf(totalBoxes-1)
    ypU.makeSubgroupOf(totalBoxes-1)
    ypZ.makeSubgroupOf(totalBoxes-1)
    ypY.makeSubgroupOf(totalBoxes-1)

    nX = sum(dX.p)
    nW = sum(dW.p)
    ypW.boost(nX)
    ypV.boost(nX+nW)
    ypZ.boost(nX)
    vPermZ.boost(nX)

    print(ypX.e)

    #total6j = ypU*vPermUInv*ypX*ypW*ypV*vPermZ*ypZ*vPermY*ypY*vPermYInv
    total6j = ypY*vPermYInv*ypZ*ypX*vPermZInv*ypV*ypW*vPermU*ypU*vPermY
    return total6j

def check6j0():
    tY = Tableau([[1,3],[2],[4]])
    tU = Tableau([[1,2],[3]])
    tZ = Tableau([[1],[2]])
    dX = Diagram([1,1])
    dW = Diagram([1])
    dV = Diagram([1])

    x = eval6jTab(dX, dW, dV, tU, tZ, tY)
    return x

def check6j1():
    tY = Tableau([[1,3],[2]])
    tU = Tableau([[1],[2]])
    tZ = Tableau([[1],[2]])
    dX = Diagram([1])
    dW = Diagram([1])
    dV = Diagram([1])

    x = eval6jTab(dX, dW, dV, tU, tZ, tY)
    return x

def check3j0():
    d1 = Diagram([2,1])
    d2 = Diagram([2,1])
    d12 = Diagram([3,3])
    t = Tableau([[1,2,4],[3,5,6]])
    vPerm = Permutation(t.permutation())
    x = eval3j(d1, d2, d12, vPerm)
    return x
def check3j1():
    d1 = Diagram([1])
    d2 = Diagram([1])
    d12 = Diagram([2])
    t = Tableau([[1,2]])
    vPerm = Permutation(t.permutation())
    x = eval3j(d1, d2, d12, vPerm)
    return x

def check(p1,p2):
    testSuccess = True
    knownProduct = partitionProduct(p1,p2)

    for term in knownProduct:
        partition, coeff = term
        d = Diagram(partition)
        print("----------\nTerm:\n" + d.printStr() + "")
        myCoeff = myLRCoeff(p1,p2,d)
        if myCoeff != coeff:
            testSuccess=False

    print("Test succeeded?:")
    print(testSuccess)
