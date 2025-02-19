def mod(x):
    if x>=0:
        return x
    else:
        return -x
def t(n):
    a=0
    while(n>0):
        n=n//2
        if n==0:
            break
        else:
            a+=1
    return a
def bin(n):
    m=0
    while(n>0):
        m+=10**t(n)
        n=n-2**t(n)
    return str(m)
def dec(n):
    m=0
    while(n>0):
        m+=10**t(n)
        n=n-2**t(n)
    return '0'*(5-len(str(m)))+str(m)
def f(s):
    a=int(s[1:])
    m=0
    while(a>0):
        m+=10**t(a)
        a=a-2**t(a)
    return '0'*(5-len(str(m)))+str(m)
def j(n,b):
    if n>0:
        return "0"*(b-len(bin(mod(n))))+bin((n))
    else:
        t=n+1
        l="0"*(b-len(bin(mod(t))))+bin(mod(t))
        l1=[]
        for i in l:
            l1.append(i)
        l2=[]
        for i in l1:
            l2.append(str(mod(int(i)-1)))
        s1=("").join(l2)
        return s1
def sum(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    s1="0000000"+f(l2[3])+f(l2[2])+"000"+f(l2[1])+"0110011"
    return s1
def sub(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    s1="0100000"+f(l2[3])+f(l2[2])+"000"+f(l2[1])+"0110011"
    return s1
def slt(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    s1="0000000"+f(l2[3])+f(l2[2])+"010"+f(l2[1])+"0110011"
    return s1
def sltu(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    s1="0000000"+f(l2[3])+f(l2[2])+"011"+f(l2[1])+"0110011"
    return s1
def xor(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    s1="0000000"+f(l2[3])+f(l2[2])+"100"+f(l2[1])+"0110011"
    return s1
def or1(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    s1="0000000"+f(l2[3])+f(l2[2])+"110"+f(l2[1])+"0110011"
    return s1
def and1(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    s1="0000000"+f(l2[3])+f(l2[2])+"111"+f(l2[1])+"0110011"
    return s1   
def f1(s):
    i=s[0:3]
    j=s[0:4]
    k=s[0:2]
    if i=="add":
        return sum(s)
    elif i=="sub":
        return sub(s)
    elif i=="slt" and j!="sltu":
        return slt(s)
    elif j=="sltu":
        return sltu(s)
    elif i=="xor":
        return xor(s)
    elif k=="or":
        return or1(s)
    if i=="and":
        return and1(s)
    else:
        return("Invalid Instruction!")
f2=open("assembly.txt","a")
with open("input.txt", "r") as file:
    data = file.readlines()
    for line in data:
        f2.write(f1(line.strip()))
        f2.write("\n")

