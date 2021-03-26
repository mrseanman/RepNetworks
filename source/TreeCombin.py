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




#partitions such that the minimum value is >= I
#not including (n)
def partI(n, I):
    for part in partitions(n):
        if (min(part) >= I) and (len(part)>1):
            yield part


#partitions such that the len(part)%==0
def partDivI(n,I):
    for part in partitions(n):
        if I%len(part)==0:
            yield part

#number of conjugacy classes of trees joining n stray edges
def thetaOld(n):
    if n<4:
        return 1
    runningSum = 0
    for sigma in partI(n,3):
        runningProd = 1
        for lbd in sigma:
            for delta in partDivI(lbd,2):
                runningProd *= theta(lbd)
        runningSum += runningProd

    return runningSum

def theta(n):
    if n<4:
        return 1
    runningSum = 0
    for split in splits(n):
        runningSum += theta(split[0]) * theta(split[1])
    return runningSum


def splits(n):
    if n==1:
        yield [0,1]
    for i in range(1,int(n/2)+1):
        yield [i,n-i]

def B(k):
    if k<4:
        return 1
    if k%2==0:
        runningSum = 0
        for split in splits(k):
            a,b = split
            runningSum += B(a) * B(b)
        correctionB = B(k/2)
        correctionTerm = int((correctionB**2 - correctionB)/2)
        return runningSum - correctionTerm
    else:
        runningSum = 0
        for split in splits(k):
            a,b = split
            runningSum += B(a) * B(b)
        return runningSum
