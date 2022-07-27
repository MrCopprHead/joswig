#manual process of interpolation.

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate,optimize
import t_joswig as tj

griddata = interpolate.griddata

#open and read the file after the appending:
fil = open("gatewayDistances.csv", "r")
x = []
a = fil.readline()
while(a != ""):
    x.append(a)
    a = fil.readline()

times = []
params = [[],[],[],[],[],[],[]]
#print(x[1].split('\n')[0])
for line in x[1:]:
    vals = line.split('\n')[0]
    other = vals.split(',')
    times.append(int(other[0]))
    params[0].append(float(other[3]))
    params[1].append(float(other[5]))
    params[2].append(float(other[1]))
    params[3].append(float(other[4]))
    params[4].append(float(other[7]))
    params[5].append(float(other[2]))
    params[6].append(float(other[6]))
    #times.append(int(vals[0]))
    #print(vals)
#print(times)
#print(params)
#print(len(times))
#print(len(params[0]))

beg = 0
end = 2880
f1 = interpolate.interp1d(times,params[0],'cubic')
f2 = interpolate.interp1d(times,params[1],'cubic')
f3 = interpolate.interp1d(times,params[2],'cubic')
f4 = interpolate.interp1d(times,params[3],'cubic')
f5 = interpolate.interp1d(times,params[4],'cubic')
f6 = interpolate.interp1d(times,params[5],'cubic')
f7 = interpolate.interp1d(times,params[6],'cubic')
xnew = np.arange(30*beg,30*end,15)

'''
y1new = f1(xnew)
y2new = f2(xnew)
y3new = f3(xnew)
y4new = f4(xnew)
y5new = f5(xnew)
y6new = f6(xnew)
y7new = f7(xnew)
#plt.plot(times[beg:end], params[0][beg:end], 'o', xnew, y1new, '-')
#plt.plot(times[beg:end], params[1][beg:end], 'r', xnew, y2new, '-')
plt.plot(y1new,y2new, '-')
plt.plot(y1new,y3new, '-')
plt.plot(y1new,y4new, '-')
plt.plot(y1new,y5new, '-')
plt.plot(y1new,y6new, '-')
plt.plot(y1new,y7new, '-')
#plt.show()
'''

def test(x):
    return x**2-1

def g12list(xnew):
    return f7(xnew)-f6(xnew)-38344

#print(("test",g12list.__call__(42400)))

ynew = g12list(xnew)
plt.plot(xnew,ynew, '-')
#plt.show()

#print('roots')

def g(x):
#    a = f1.__call__(x)
#    b = f2.__call__(x)
    return f7.__call__(x)-f6.__call__(x)-38344

part = [6753,34171,16747,84927,5146,45754,17567,73152,8257,4131,28480,14537,78327,50536,
        78208,3434,47450,47379,71805,10449,59609,41646,49744,41410,62479,26412,64603,34257,59495,14794,54730,40150,44290]
#for t in part:
#    print(t)
part.sort()
#for t in part:
    #print(int(t/60.))


sep = []
for i in range(0,len(part)-1):
    sep.append(part[i+1]-part[i])
print(max(sep))
print(min(sep))

#MAX SEPARATION IS 8845

#the first index is the LHS param (source)
#and the second index is the RHS alt. param.
#the actual value is the added dist.
altD = [[0,62654,52279,77513,50401,67977,39523],
        [62654,0,40544,27631,43317,82376,53300],
        [52279,40544,0,38116,2773,42791,12756],
        [77513,27631,38116,0,39719,79737,50597],
        [50401,43317,2773,39719,0,40018,10878],
        [67977,82376,43591,79737,40018,0,38344],
        [39523,53300,12756,50597,10878,38344,0]]

def ineq(a,b,c):
    result = False
    if(a>= b+c):
        result = True
    return result

for z in range(0,len(part)-1):
    t = int((part[z]+part[z+1])/2)
#t = 500
    tree = 0x0
    pos = 0
    samp = [float(f1(t)),float(f2(t)),float(f3(t)),float(f4(t)),float(f5(t)),float(f6(t)),float(f7(t))]
    print('sample',samp)
    for val in samp:
        i = samp.index(val)
        for j in range(0,len(altD[0])):
            if(i != j):
                #print(i,j)
                bound = altD[i][j]
                if ineq(val, samp[j], bound):
                    #print((val,samp[j],bound))
                    tree = tree | (1<<pos)
                    #print(hex(tree))
                pos += 1
    #print(pos)
    print('final result',t,hex(tree))


#mid = 42400
#sol = optimize.root_scalar(g,bracket=[0,mid],method='bisect')
#print(sol.root)

#sol = optimize.root_scalar(g,bracket=[mid,86400],method='bisect')
#print(sol.root)


'''
print(y)
y = y.split('\n')
print(y[0])
print('hello')
'''
'''
for i in range(0,20):
    a = fil.readline()
    print(a)
    print(a == "")
'''

'''
x.append(fil.readline())
print(x)
x.append(fil.readline())
print(x)
print(x[0].split(','))
#print(fil.readline())
'''

fil.close()

'''
f1 = interpolate.interp1d(x, y1,'cubic')
f2 = interpolate.interp1d(x, y2,'cubic')
xnew = np.arange(0, 9, 0.1)
y1new = f1(xnew)   # use interpolation function returned by `interp1d`
y2new = f2(xnew)
plt.plot(x, y1, 'o', xnew, y1new, '-')
plt.plot(x, y2, 'o', xnew, y2new, '-')
plt.plot(y1new,y2new, '-')
plt.show()


def func(t):
    return (f1(t),f2(t))

T = np.arange(0, 2*np.pi,0.1)

newX,newY = func(T)

plt.plot(newX,newY, '-')
plt.show()
'''
