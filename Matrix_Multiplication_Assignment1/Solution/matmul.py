# Function which checks whether the given variable is in fact a matrix and not a vector or N-D tensor (N >= 3)
def check_matrix(y): 
    check1 = True
    check2 = False
    try:
        y[0][0]
    except:
        check1 = False
    try:
        y[0][0][0]
    except:
        check2 = True
    return check1 and check2

# Function which checks that the dimensions of the given matrices are of the form of x*y , y*z 
# it also calls the check_matrix function and handles the error for the same 
def check_dim(A,B):
    if(check_matrix(A) and check_matrix(B)):
        if(len(A[0]) != len(B)):
            raise ValueError
    else:
        raise TypeError

# main multiplier function , explanation in README.md
def matmul(A, B):
    check_dim(A,B)
    result = []
    for i in range(len(A)):
        temp = []
        for j in range(len(B[0])):
            s = 0
            for k in range(len(B)):
                # try except case to handle the cases where matrices have non-numeric entries or entry doesnt exist
                try:
                    # converting every entry to complex in case the matrix contains a number stored in string form
                    s += complex(A[i][k])*complex(B[k][j]) 
                except:
                    try: #tries to check if the entry exists , if it does exist , TypeError
                        A[i][k]
                        B[k][j]
                        raise TypeError
                    except: # if entry doesnt exist , IndexError
                        raise IndexError   
            temp.append(s)
        result.append(temp)
    return result
