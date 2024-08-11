import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def get_data(file_name): # Gets the data from CSV file in both row-wise and Column-wise format
    A = []
    B = []
    with open(file_name) as f:
        print(f.readline())
        for i in f.readlines():
            z = i.split(',')
            A.append([float(x) for x in z])
            if(B == []):
                for j in z:
                    B.append([float(j)])
            else:
                for j in range(len(z)):
                    B[j].append(float(z[j]))
    return A,B

def msq(A,B): # Returns mean square error between 2 sets of values
    error = 0
    for i in range(len(A)):
        error += (A[i]-B[i])**2
    return error/len(A)

def linear(t,m,c): # linear function for curve fit
    return t*m + c
def quadratic(t,a,b,c): # Quadratic function for curve fit
    return a*(t**2) + b*t + c

R,C = get_data('Admission_Predict_Ver1.1.csv')
def find_best_fit(x,y): # Calculating mean square error between each factor and Chance of Admit for linear and quadratic approximations
    (m,k),_ = curve_fit(linear,x,y)
    Z1 = []
    for i in range(len(x)):
        Z1.append(linear(x[i],m,k))
    e1 =msq(Z1,y)

    Z2= []
    (a,b,c),_ = curve_fit(quadratic,x,y)
    for i in range(len(x)):
        Z2.append(quadratic(x[i],a,b,c))
    e2 = msq(Z2,y)
    if(e1 > e2):
        print(e1,e2,'quadratric')
        return (a,b,c)
    else:
        print(e1,e2,'linear')
        return (m,k)

def get_linear_fit(x,y): # gets the resulting predicted values from performing a linear fit
    (m,k),_ = curve_fit(linear,x,y)
    Z1 = []
    for i in range(len(x)):
        Z1.append(linear(x[i],m,k))
    e1 =msq(Z1,y)
    return Z1,m,k,e1
for i in C[1:-1]:
    find_best_fit(i,C[-1])

coeff = []
inter = []
for j in C[1:-1]:
    Z,m,k,e = get_linear_fit(j,C[-1])
    coeff.append((m,k))
    inter.append(Z)

def linear_big(t1,t2,t3,t4,t5,t6,t7,a,b,c,d,e,f,g,h): #model for the data 
    return a*t1 + b*t2 + c*t3 + d*t4 + e*t5 + f*t6 + g*t7 + h

def linear_fit(inter): # function for performing the linear fit
    M = []
    for i in range(len(inter[0])):
        l = []
        for j in range(len(inter)):
            l.append(inter[j][i])
        l.append(1)
        M.append(l)
    A, _, _, _ = np.linalg.lstsq(M, C[-1], rcond=None)
    return A
A = linear_fit(C[1:-1])
print(A) # All the coefficients of the linear model 'linear_big'
Z = []
# generating predicted values from the model
for i in range(len(C[-1])):
    Z.append(linear_big(C[1][i],C[2][i],C[3][i],C[4][i],C[5][i],C[6][i],C[7][i],A[0],A[1],A[2],A[3],A[4],A[5],A[6],A[7]))
print('error',msq(Z,C[-1]))
# Plotting original datapoints and predicted datapoints on top of it
plt.cla()
plt.scatter(C[0],Z)
plt.scatter(C[0],C[-1])
plt.savefig('final')

#normalising the parameters.
print('Max values for each parameter:')
for i in C:
    print(max(i[1:]),end =' ')
print()
print('Normalised coefficients:')
c = 0
for i in C[1:-1]:
    print(max(i[1:])*A[c],end =' ')
    c += 1