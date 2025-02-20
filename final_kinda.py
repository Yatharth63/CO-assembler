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
    
# Function to assemble R-type instructions 
def r_type(parts):
    if len(parts) != 4:
        return "ERROR"
    rd, rs1, rs2 = regis_to_bi(parts[1]), regis_to_bi(parts[2]), regis_to_bi(parts[3])
    funct3 = "000"
    if parts[0] != "sub":
        funct7 = "0000000"
    else:
        funct7 = "0100000"
    return funct7 + rs2 + rs1 + funct3 + rd + opcodes[parts[0]]

# Function to assemble I-type instructions 
def i_type(parts):
    if len(parts) != 4:
        return "ERROR"
    rd, rs1, imm = regis_to_bi(parts[1]), regis_to_bi(parts[2]), format(int(parts[3]), "012b")
    funct3 = "000"
    return imm + rs1 + funct3 + rd + opcodes[parts[0]]

# Function to assemble S-type instructions 
def s_type(parts):
    if len(parts) != 4:
        return "ERROR"
    rs1, rs2, imm = regis_to_bi(parts[3]), regis_to_bi(parts[1]), format(int(parts[2]), "012b")
    funct3 = "010"
    return imm[:7] + rs2 + rs1 + funct3 + imm[7:] + opcodes[parts[0]]

# Function to assemble B-type instructions 
def b_type(parts):
    if len(parts) != 4:
        return "ERROR"
    rs1, rs2, imm = regis_to_bi(parts[1]), regis_to_bi(parts[2]), format(int(parts[3]), "012b")
    funct3 = "000"
    return imm[:7] + rs2 + rs1 + funct3 + imm[7:] + opcodes[parts[0]]

# Function to assemble U-type instructions 
def u_type(parts):
    if len(parts) != 3:
        return "ERROR"
    rd, imm = regis_to_bi(parts[1]), format(int(parts[2]), "020b")
    return imm + rd + opcodes[parts[0]]

# Function to assemble an instruction from assembly to binary
def assemble(liners):
    parts = liners.replace(",", "").split()
    if not parts:
        return "ERROR: Empty instruction"
    if parts[0] not in opcodes:
        return "ERROR: Invalid instruction"
    opcode = opcodes[parts[0]]
    
    if opcode == "0110011":
        return r_type(parts)
    elif opcode in ["0000011", "0010011", "1100111"]:
        return i_type(parts)
    elif opcode == "0100011":
        return s_type(parts)
    elif opcode == "1100011":
        return b_type(parts)
    elif opcode == "0110111":
        return u_type(parts)
    return "ERROR: Unsupported instruction format"

# Function to assemble an entire file
def assemble_file(input, output):
    try:
        with open(input, 'r') as f:
            lines = f.readlines()
        binary_lines = [assemble(line.strip()) for line in lines if line.strip()]
        with open(output, 'w') as f:
            f.write("\n".join(binary_lines))
    except FileNotFoundError:
        print(f"Error: File '{input}' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


input = "file1.txt"    #input("Enter input file name: ")
output = "output.txt"  #input("Enter output file name: ")


assemble_file(input, output)

print("Done")