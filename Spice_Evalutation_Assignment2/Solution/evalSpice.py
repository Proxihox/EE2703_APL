import numpy.linalg as linalg
# Begin Section - Gauss Elimination

# Code for solving A set of Linear equations
def merge(A,B): # Vertically merges 2 lists A and B
    for i in range(len(A)):
        A[i] = A[i] + [B[i]]
    return A

def split(C): #Does the opposite of merge
    A = []
    B = []
    for i in range(len(C)):
        A.append(C[i][:-1])
        B.append(C[i][-1])
    return (A,B)

def find_pivot(A,n): # Function which is used to find the 'n'th pivot of a matrix A 
    maxn = n
    maxval = abs(A[n][n])
    for i in range(n,len(A)):
        if(abs(A[i][n]) > maxval):
            maxval = abs(A[i][n])
            maxn = i
    return (maxval,maxn)

def switch_rows(A,a,b):# Function which switches the 'a'th and 'b'th of matrix A
    A[a],A[b] = A[b],A[a]
    return A

def decompose(A,n):# Decomposes a submatrix of A , the submatrix is the lower right part of A.
    #decompose operation is basically eliminating one variable from the equations
    x = A[n][n]
    for i in range(n+1,len(A)):
        y = A[i][n]/x
        for j in range(n,len(A[i])):
            A[i][j] -= A[n][j] * y
    return A

def RREF(A):# Converts matrix A into RREF form
    for i in range(len(A)-1):
        (m,n) = find_pivot(A,i)
        A = switch_rows(A,n,i)
        A = decompose(A,i)
        #print(A)
    return A

def back_sub(A,B):# Backsubstitutes the coefficients in LHS matrix A with the constant values on RHS matrix B , to solve for all variables
    #Assumes A and B to be obtained after RREF calculation
    n = len(A)
    solution = [0]*n
    for i in range(n):
        sum = 0
        for j in range(i):
            sum += A[n-i-1][n-j-1]*solution[n-j-1]
        solution[n-i-1]= (B[n-i-1] - sum)/A[n-i-1][n-i-1]
    return solution

def solve_matrix(A,B): # Solves matrix A consisting of coefficients of variables of linear eqautions and B containing the constant values 
    C = merge(A,B)
    C = RREF(C)
    (A,B) = split(C)
    sol = back_sub(A,B)
    return sol

# End Section - Gauss Elimination

# Begin Section - Error handling

def not_unique(L): # Function to check if all entries in a list are not the same
    if(L == []):
        return False
    elif([L[0]]*len(L) == L):
        return False
    else:
        return True

def check_loops(conns): #performs checks for voltage and current source consistency
    for i in conns:
        for j in conns[i]:
            D = {'V':[],'I':[]}
            for k in conns[i][j]:
                if(k[0] in 'VI'):
                    D[k[0]].append(k[1])
            if(not_unique(D['V']) or not_unique(D['I'])):
                raise ValueError('Circuit error: no solution')


def map_nodes(file_name): # Main function which maps elements to the nodes as a dictionary of dictionaries
    global Nodes,items
    Nodes = ['GND'] # defining GND as a node because we know it will definitely be part of circuit
    items = []
    f = open(file_name,'r')
    S = f.readlines()
    i = 0
    try:
        while(S[i] != ".circuit\n"):
            i += 1
        i += 1
    except:
        raise ValueError('Malformed circuit file') # malformed circuit if it doesnt contain .circuit
    # items is a simple list containing all the data from the .ckt file with no analysis done on it 
    while(S[i] != ".end\n"):
        j = S[i].split()
        type = j[0][0]
        name = j[0]
        if(type not in 'VIR'):
            raise ValueError('Only V, I, R elements are permitted')# Ensuring element is Voltage or current source or Resistor
        if(j[0][0] in ['V','I']):
            value = float(j[4])
            if(j[3] != 'dc'):
                raise ValueError('We dont handle non-dc curcuits')# Ensuring Voltage and current sources are DC
        else:
            value = float(j[3])
        if(j[1] not in Nodes):
            Nodes.append(j[1])
        if(j[2] not in Nodes):
            Nodes.append(j[2])
        
        items.append((type,j[1],j[2],value,name))
        i += 1
        if(S[i] == S[-1] and S[i] != ".end\n"):
            raise  ValueError('Malformed circuit file')# malformed circuit if it doesnt contain .end
    conns = format(Nodes)
    #print('yo')
    #print('Nodes',Nodes)
    if(debug_mode == True):
        for i in conns:
            print(conns[i])
    return conns


def format(Nodes): # Combines information from items and Nodes to create the dictionary of all the connections
    global items
    D = items 
    connections = {}
    n = len(Nodes)
    for i in Nodes:
        connections[i] = {}
    for i in D:
        try:
            connections[i[1]][i[2]].append((i[0],i[3],i[-1]))
            if(i[0] not in ['V','I']):
                connections[i[2]][i[1]].append((i[0],i[3],i[-1]))
            else:
                connections[i[2]][i[1]].append((i[0],-i[3],i[-1]))
        except:
            connections[i[1]][i[2]]  = [(i[0],i[3],i[-1])]
            if(i[0] not in ['V','I']):
                connections[i[2]][i[1]] = [(i[0],i[3],i[-1])]
            else:
                connections[i[2]][i[1]] = [(i[0],-i[3],i[-1])]
    return connections



def read_file(file_name):
    try:
        f = open(file_name,'r')
    except:
        raise FileNotFoundError('Please give the name of a valid SPICE file as input') # if it fails to open the file , it doesnt exist
    if(file_name.split('.')[-1] != 'ckt'):
            raise TypeError('Invalid File Type')# Ensuring file is .ckt type
    conns = map_nodes(file_name)
    check_loops(conns)
    return conns



def equation_nodal(i,conns,Sources,b): # Given i , this function generates the nodal analysis equation for the ith line in the matrix
    global  Nodes , items
    s = []
    b_val = 0
    for j in Nodes[1:]:
        try:
            conns[j][i]
        except:
            if(j == i):
                c = 0
                for k in conns[i]:
                    t = conns[i][k]
                    for l in t:
                        if(l[0] == 'R'):
                            c += 1/l[1]
                s.append(c)
            else:
                s.append(0)
            continue
        t = conns[i][j]
        for l in t:
            if(l[0] == 'R'):
                s.append(-1/l[1])
            elif(l[0] == 'I'):
                if(j == t[0]):
                    b_val += l[1]
                else:
                    b_val -= l[1]
    for l in conns[i]['GND']:
        if(l[0] == 'I'):
            b_val -= l[1]
    for j in Sources:
        if(j[1] == i):
            s.append(1)
        elif(j[2] == i):
            s.append(-1)
        else:
            s.append(0)
    #print(i,s)
    b.append(b_val)
    return s,b
        
def equation_current(j,conns,Sources,b): # Given j , this function generates the Current analysis equation for the jth line in the matrix
    global Nodes
    s = [0]*(len(Nodes)-1 + len(Sources))
    if(j[1] == 'GND'):
        pass
    else:
        s[Nodes.index(j[1])-1] = 1
    
    if(j[2] == 'GND'):
        pass
    else:
        s[Nodes.index(j[2])-1] = -1
    b.append(j[3])
    return s,b

    
def build(conns): # function which builds the matrix from the connections data
    global Nodes , items
    n = len(Nodes)-1
    v = 0
    Sources = []
    for i in items:
        if(i[0] == 'V'):
            v += 1
            Sources.append(i)
    b = []
    M = []
    c1 = 0
    for i in Nodes[1:]:
        s,b = equation_nodal(i,conns,Sources,b)
        M.append(s)
    for j in Sources:
        s,b = equation_current(j,conns,Sources,b)
        M.append(s)
    return M,b


debug_mode = False
if(debug_mode):
    print('items',items)
    print('Nodes',Nodes)
    print()


def format_ans(L): # Formats the output matrix to the pair of dictionaries as is expected as the ouptut
    global Nodes , items
    Voltages = {'GND':0}
    Currents = {}
    c = 0
    for i in range(1,len(Nodes)):
        Voltages[Nodes[i]] = L[c]
        c += 1
    for j in items:
        if(j[0] == 'V'):
            Currents[j[4]] = L[c]
            c += 1
    return Voltages,Currents



def get_currents(Voltages,Currents,conns): # function for calculating current through each connection
    global Nodes,items
    I = {}
    for i in Nodes:
        temp = {}
        for j in Nodes:
            if(i == j):
                temp[i] = 0
                continue
            try:
                vals = conns[i][j]
                temp[j] = 0
                for k in vals:
                    if(k[0] == 'R'):
                        temp[j] += (Voltages[i] - Voltages[j])/k[1]
                    elif(k[0] == 'I'):
                        try:
                            I[j][i]
                            temp[j] += k[-1]
                        except:
                            temp[j] -= k[1]
                    else:
                        try:
                            I[j][i]
                            temp[j] += Currents[k[-1]]
                        except:
                            temp[j] -= Currents[k[-1]]
            except:
                temp[j] = 0
        I[i] = temp
    return I

def validate(I): # function to verify KCL at every node
    for i in I:
        s = 0
        for j in I[i]:
            s += I[i][j]
        if(s != 0):
            return False  
    else:
        return True

def evalSpice(filename):

    conns = read_file(filename)
    A,B = build(conns)
    try:
        Solution = linalg.solve(A,B)
    except:
        Solution = solve_matrix(A,B)
    
    Voltages , Currents =  format_ans(Solution)
    I = get_currents(Voltages,Currents,conns)
    validate(I)
    return (Voltages,Currents)