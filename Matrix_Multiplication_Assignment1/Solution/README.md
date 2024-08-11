# Matrix Multiplier by Prithvi P Rao , EE22B024

## Algorithm:
After the input variables A,B  have passed the preliminary checks and are of dimensions x*y and y*z respectively , we run a for loop with another for loop nested inside it . this is to generate each entry of the resulatant matrix . Therefore , the loops will run 'x' and 'z' times respectively. Within each of these loops , we run another loop to get the value of each of these terms . This loop runs `y` times , each time it adds one of the product terms from the multiplication. 

## Data checking:
check_matrix is a function which ensures that the input 'A' is 2 dimensional matrix. This is done by ensuring that A[0][0] exists , which is possible only if it is matrix of order >= 2 and at the same time also checks that A[0][0]
[0] does not exist which means that it is a matrix of order <= 2 . If both checks pass , then it is confirmed that A is a matrix of order 2 .

check_dim ensures that the matrices are of the dimensions x*y , y*z so that matrix multiplication is possible.