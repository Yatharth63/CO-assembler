# Assembler: Converts RISC-V assembly to binary

# Dictionary for register mapping 
# Each register has a 5-bit binary code used instruction 
registers = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
    }
# Dictionary for opcode mapping 
# Each instruction type (R, I, S, B, U) has a different opcode used 
opcodes = {
    "add": "0110011",
    "sub": "0110011",
    "slt": "0110011",
    "srl": "0110011",
    "or": "0110011",
    "and": "0110011",
    "lw": "0000011",
    "addi": "0010011",
    "jalr": "1100111",
    "sw": "0100011",
    "beq": "1100011",
    "bne": "1100011",
    "blt": "1100011",
    "jal": "1101111"
    }

# Function to convert register name to binary
# Returns a 5-bit binary representation of the register name
def regis_to_bi(name):
    if name in registers:
        return registers[name]
    else:
        return "00000"
def i_type(parts):
    if len(parts) != 4:
        return "ERROR"
    rd, rs1, imm = regis_to_bi(parts[1]), regis_to_bi(parts[2]), format(int(parts[3]), "012b")
    funct3 = "000"
    return imm + rs1 + funct3 + rd + opcodes[parts[0]]
def assemble(liners):
    parts = liners.replace(",", "").split()
    if not parts:
        return "ERROR: Empty instruction"
    if parts[0] not in opcodes:
        return "ERROR: Invalid instruction"
    opcode = opcodes[parts[0]]
    if opcode in ["0000011", "0010011", "1100111"]:
        return i_type(parts)
    else:
        return "ERROR: Unsupported instruction format"
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

# b type instruction

def set_register_binary(r):
    register_no=int(r[1:])       # input wouk dbe r1, r2 so taking integers from 1st pace till end
    #binary_of_reg=p.bin(register_no) 
    return j(register_no,5)  # gives reg in 5 bits
def beq(r1,r2,immediate):
    imm=j(immediate,12)
    register_1=set_register_binary(r1)
    register_2=set_register_binary(r2)
    register_1==register_2
    final_instruction=imm[0]+imm[2]+imm[3]+imm[4]+imm[5]+imm[6]+imm[7]+set_register_binary(r1)+set_register_binary(r2)+"000"+imm[8]+imm[9]+imm[10]+imm[11]+imm[1]+"1100011"
    return final_instruction

def bne(r1,r2,immediate):
    #immediate=p.bin(immediate)
    imm=j(immediate,12)
    register_1=set_register_binary(r1)
    register_2=set_register_binary(r2)

        # imm[0] is imm[12th bit] and imm[8:12]=imm[4:1 wala bit] and imm[]
    final_instruction=imm[0]+imm[2]+imm[3]+imm[4]+imm[5]+imm[6]+imm[7]+set_register_binary(r1)+set_register_binary(r2)+"001"+imm[8]+imm[9]+imm[10]+imm[11]+imm[1]+"1100011"
    return final_instruction
print(beq("r2","r2",7))

print(bne("r4","r2",7))
# j type instruction
def jal(rd,immediate):      # immediat value in jal instru tion is a 21 bit offset
    register=set_register_binary(rd)    #  rd to binary
    imm=j(immediate,21)
    final_instruction=imm[1]+imm[11:21]+imm[10]+imm[2:10]+register+"1101111"
    return final_instruction
def beq1(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    st1=beq(l2[1],l2[2],int(l2[3]))
    return st1
def bne1(s):
    l=[]
    for i in s:
        if i!=" ":
            l.append(i)
        elif i==" ":
            l.append(",")
    s2=("").join(l)
    l2=s2.split(",")
    st1=bne(l2[1],l2[2],int(l2[3]))
    return st1
def rev(s):
    l=[]
    for i in s:
        l.append(i)
    l.reverse()
    s2=("").join(l)
    return s2
def sw(s):
    a=s.index(",")
    b=s.index("(")
    c=s.index(")")
    l=[s[3:a],s[a+1:b],s[b+1:c]]
    s1=j(int(l[1]),12)[:7]+f(l[0])+f(l[2])+"010"+(rev(j(int(l[1]),12)))[0:5]+"0100011"
    return s1
def f1(s):
    i=s[0:3]
    j=s[0:4]
    k=s[0:2]
    if i=="add" and j!="addi":
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
    elif i=="and":
        return and1(s)
    elif k=="sw":
        return sw(s)
    elif i=="beq":
        return beq1(s)
    elif i=="bne":
        return bne1(s)
    else:
        return(assemble(s))
f2=open("assembly.txt","a")
with open("input.txt", "r") as file:
    data = file.readlines()
    for line in data:
        f2.write(f1(line.strip()))
        f2.write("\n")
