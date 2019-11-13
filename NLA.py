import copy
import math
import numpy
def innerproduct(a,b):
	if len(a)!=len(b):
		raise ValueError
	sum=0
	for i in range(0,len(a)):
		sum+=(a[i]*b[i])
	return sum

def transpose(M):
    i=len(M)
    j=len(M[0])
    M_=[]
    for i_ in range(0,j):
        row=[]
        for j_ in range(0,i):
            row.append(M[j_][i_])
        M_.append(row)
    return M_
    
def product(A,B):
    if len(A[0])!=len(B):
        raise ValueError
    l1=len(A);l2=len(B);l3=len(B[0])
    C=[]
    for l1_ in range(0,l1):
        row=[]
        for l3_ in range(0,l3):
            sum=0
            for l2_ in range(0,l2):
                sum+=A[l1_][l2_]*B[l2_][l3_]
            row.append(sum)
        C.append(row)
    return C

def thomasalgorithm(a,b,c,r):
    for i in range(0,len(r)):
        if i>0:
            b[i]-=c[i-1]*a[i]
            r[i]-=r[i-1]*a[i]
            a[i-1]=0
        if i<len(c):c[i]/=b[i]
        r[i]/=b[i]
        b[i]=1
    x=[0]*len(r)
    x[len(r)-1]=r[len(r-1)]
    for i in range(len(r)-2,-1,-1):
        x[i]=r[i]-c[i]*x[i+1]
    return x


def cholesky(A):
    r=[[0 for i in range(len(A))] for j in range(len(A))]
    for i in range(0,len(A)):
        for j in range(i,len(A)):
            if i==j:
                s=0
                for k in range(0,i):
                    s+=r[i][k]*r[i][k]
                r[i][i]=math.sqrt(A[i][i]-s)
            else:
                s=0
                for k in range(0,i):
                    s+=r[i][k]*r[j][k]
                r[j][i]=(A[i][j]-s)/r[i][i]
    return r

def gaussianelimination(A_,b_,scaledpartialpivot):
    A=copy.deepcopy(A_)
    b=copy.deepcopy(b_)
    if len(A)!=len(A[0]):
        raise ValueError
    if len(A[0])!=len(b):
        raise ValueError
    n=len(A)
    for j in range(0,n-1):
        if scaledpartialpivot:
            Max=0
            Maxi=-1
            for i in range(j,n):
                max=0
                for j_ in range(j,n):
                    if abs(A[i][j_])>max:
                        max=abs(A[i][j_])
                if max==0:
                    raise ValueError
                for j_ in range(j,n):
                    A[i][j_]/=max
                b[i]/=max
                if abs(A[i][j])>Max:
                    Max=abs(A[i][j])
                    Maxi=i
            if Maxi==-1:
                raise ValueError
            for j_ in range(j,n):
                A[j][j_],A[Maxi][j_]=A[Maxi][j_],A[j][j_]
            b[j],b[Maxi]=b[Maxi],b[j]
        if A[j][j]==0:
            for i in range(j+1,n):
                if A[i][j]!=0:
                    for j_ in range(j,n):
                        A[j][j_],A[i][j_]=A[i][j_],A[j][j_]
                    b[j],b[i]=b[i],b[j]
            if A[j][j]==0:
                raise ValueError
        for i in range(j+1,n):
            m=A[i][j]/A[j][j]
            for j_ in range(0,n):
                A[i][j_]-=m*A[j][j_]
            b[i]-=m*b[j]
    if A[n][n]==0:
        raise ValueError
    x=[0]*n
    for i in range(n-1,-1,-1):
        s=0
        for j in range(i+1,n):
            s+=x[j]*A[i][j]
        x[i]=(b[i]-s)/A[i][i]
    return x

if __name__ == "__main__":
    A=[[2,0],[3,4]]
    print("A=",A)
    print("\ncholesky of A*A'  ",cholesky(product(A,transpose(A))))
    
    B=[5,8]
    print("\nB=",B)
    x=gaussianelimination(A,B,True)
    print("\ngaussian elimination(spp) of Ax=B  x=",x)
    print("Ax=",product(A,transpose([x])))
