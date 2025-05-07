import sys
import argparse
from typing import Dict, List, Optional, Union

# ===== HELPER FUNCTIONS FOR BINARY CONVERSION AND OPERATIONS =====

def abs(x):
    if x >= 0:
        return x
    else:
        return -x

def bits(n):
    a = 0
    while n > 0:
        n = n // 2
        a += 1
    return a

def digits(n):
    """
    Counts the number of decimal digits in a positive integer n.
    For example, digits(123) = 3.
    """
    a = 0
    while n > 0:
        n = n // 10
        a += 1
    return a

def bin(n):
    """
    Converts a positive integer to a binary string representation.
    Returns a string of 1s and 0s representing the binary number.
    """
    m = 0
    while n > 0:
        m += 10 ** (bits(n) - 1)
        n -= 2 ** (bits(n) - 1)
    return str(m)

def padder(n):
    """
    Converts a positive integer to a binary string and pads it with leading zeros.
    Ensures the output string has a consistent length of 5 characters.
    """
    m = 0
    while n > 0:
        m += 10 ** bits(n)
        n -= 2 ** bits(n)
    return '0' * (5 - len(str(m))) + str(m)

def bin2int(s):
    """
    Converts a binary string to an integer.
    Strips leading zeros and processes the string bit by bit.
    Returns the decimal value of the binary string.
    """
    s = s.lstrip('0')
    if not s:  # Handle case of all zeros
        return 0
    s1 = int(s)
    m = 0
    power = 0
    while s1 > 0:
        if s1 % 10 == 1:
            m += 2 ** power 
        s1 //= 10
        power += 1
    return m

def binstr(s):
    """
    Converts a binary string with '0b' prefix to a padded binary string.
    """
    a = int(s[1:])
    m = 0
    while a > 0:
        m += 10 ** bits(a)
        a -= 2 ** bits(a)
    return '0' * (5 - len(str(m))) + str(m)

def twoscomp(st):
    """
    Converts a binary string to its two's complement representation.
    """
    if st[0] == '1':
        a = ""
        for bit in st:
            if bit == '0':
                a += '1'
            else:
                a += '0'
        ans = bin2int(str(int(a) + 1))
        return -ans
    else:
        return bin2int(st)

def binformat(n, b):

    if n >= 0:
        binary = bin(abs(n))
        return "0" * (b - len(binary)) + binary
    else:
        val = n + 2 ** b
        l = bin(val)
        return "0" * (b - len(l)) + l

def add(s, id):
    """
    Simulates the RISC-V ADD instruction.
    """
    # Split the state string into individual binary values
    l1 = s.split(" ")

    # Define lambda functions for common operations
    extract_bin = lambda x: bin2int(x[2:])  # Extract integer from binary string
    format_bin = lambda x: f"0b{binformat(x, 32)}"  # Format integer as 32-bit binary string

    # Update PC by adding 4 (next instruction)
    l1[0] = format_bin(extract_bin(l1[0]) + 4)

    # Extract register indices from instruction fields
    index1, index2, index3 = (bin2int(id[i:j]) for i, j in [(15, 20), (20, 25), (7, 12)])

    # Perform addition: rd = rs1 + rs2
    l1[index3 + 1] = format_bin(extract_bin(l1[index1 + 1]) + extract_bin(l1[index2 + 1]))

    # Extract values for all registers and PC
    reg_vals = list(map(extract_bin, l1))

    return reg_vals, l1


def sub(s, id):
    """
    Simulates the RISC-V SUB instruction.
    """
    # Split the state string into individual binary values
    l1 = s.split(" ")

    # Define lambda functions for common operations
    extract_bin = lambda x: bin2int(x[2:])  # Extract integer from binary string
    format_bin = lambda x: f"0b{binformat(x, 32)}"  # Format integer as 32-bit binary string

    # Update PC by adding 4 (next instruction)
    l1[0] = format_bin(extract_bin(l1[0]) + 4)

    # Extract register indices from instruction fields
    index1, index2, index3 = (bin2int(id[i:j]) for i, j in [(15, 20), (20, 25), (7, 12)])

    # Perform subtraction: rd = rs1 - rs2
    l1[index3 + 1] = format_bin(extract_bin(l1[index1 + 1]) - extract_bin(l1[index2 + 1]))

    return " ".join(l1)


def slt(s, id):
    """
    Simulates the RISC-V SLT (Set Less Than) instruction.
    """
    # Split the state string into individual binary values
    l1 = s.split(" ")

    # Define lambda functions for common operations
    extract_bin = lambda x: bin2int(x[2:])  # Extract integer from binary string
    format_bin = lambda x: f"0b{binformat(x, 32)}"  # Format integer as 32-bit binary string

    # Update PC by adding 4 (next instruction)
    l1[0] = format_bin(extract_bin(l1[0]) + 4)

    # Extract register indices from instruction fields
    index1, index2, index3 = (bin2int(id[i:j]) for i, j in [(15, 20), (20, 25), (7, 12)])

    # Perform comparison: rd = (rs1 < rs2) ? 1 : 0
    l1[index3 + 1] = format_bin(1 if extract_bin(l1[index1 + 1]) < extract_bin(l1[index2 + 1]) else 0)

    return " ".join(l1)


class Simulator:
    """
    A simulator for the RISC-V instruction set architecture.
    This simulator emulates the execution of RISC-V instructions in software.
    """
    def __init__(self):
        """
        Initialize the simulator with default state.
        """
        # Register file (x0-x31) - RISC-V has 32 general-purpose 32-bit registers
        # Initialize all registers to 0
        self.regs = {f'x{i}': 0 for i in range(32)}
        self.regs['x0'] = 0  # x0 is hardwired to zero in RISC-V and cannot be modified
        
        # Memory ranges - segmenting memory into different regions to simulate
        # real hardware memory organization
        self.CODE_START = 0x00000000  # Where code is stored (at address 0)
        self.CODE_END = 0x000000FF    # 256 bytes of program memory
        self.STACK_START = 0x00000100    # Stack memory follows program memory
        self.STACK_END = 0x0000017F      # 128 bytes of stack memory
        self.DATA_START = 0x00010000     # Data memory at a separate location
        self.DATA_END = 0x0001007F       # 128 bytes of data memory
        
        # Initialize memory as a continuous block of bytes
        self.mem = bytearray(0x00010080)  
        
        # Start at the beginning of program memory
        self.pc = self.CODE_START
        
        # Statistics counters to track execution metrics
        self.count = 0      
        self.cycles = 0     
        
        # Output buffer - stores formatted output for later writing to file
        self.output = []

    def read(self, addr: int, size: int = 4) -> int:
        """
        Read from memory with bounds checking.
        """
        # Check if address is within the bounds of allocated memory
        if addr < 0 or addr + size > len(self.mem):
            return 0
        
        # Check if address is in valid memory range
        if not (self.CODE_START <= addr <= self.CODE_END or
                self.STACK_START <= addr <= self.STACK_END or
                self.DATA_START <= addr <= self.DATA_END):
            return 0
        
        # Assemble multiple bytes into a single integer value
        val = sum(self.mem[addr + i] << (i * 8) for i in range(size))
        return val

    def write(self, addr: int, val: int, size: int = 4):
        """
        Write to memory with bounds checking.
        """
        # Check if address is within the bounds of allocated memory
        if addr < 0 or addr + size > len(self.mem):
            return
        
        # Check if address is in valid memory range (program, stack, or data)
        if not (self.CODE_START <= addr <= self.CODE_END or
                self.STACK_START <= addr <= self.STACK_END or
                self.DATA_START <= addr <= self.DATA_END):
            return
        
        # Split the integer value into individual bytes and write them to memory
        for i in range(size):
            self.mem[addr + i] = (val >> (i * 8)) & 0xFF

    def get(self, reg: str) -> int:
        """
        Get register value with special handling for x0.
        """
        # x0 is hardwired to 0 in RISC-V architecture
        if reg == 'x0':
            return 0
        return self.regs[reg]

    def set(self, reg: str, val: int):
        """
        Set register value with special handling for x0.
        """
        # x0 cannot be modified in RISC-V architecture
        if reg != 'x0':
            self.regs[reg] = val

    def load(self, prog: List[str], fmt: str = 'binary'):
        """
        Load program into memory.
        """
        addr = 0  
        for line in prog:
            line = line.strip()
            if not line:  
                continue
                
            if fmt == 'hex':
                # Remove 0x prefix if present
                if line.startswith('0x'):
                    line = line[2:]
                val = int(line, 16)  
            else:  
                val = int(line, 2)   
                
            self.write(addr, val)
            addr += 4  

    def exec(self, instr: int) -> bool:
        """
        Execute a single RISC-V instruction.
        """
        # Extract opcode (bits 0-6)
        op = instr & 0x7F
        
        # Extract register fields
        rd = (instr >> 7) & 0x1F
        funct3 = (instr >> 12) & 0x7
        rs1 = (instr >> 15) & 0x1F
        rs2 = (instr >> 20) & 0x1F
        funct7 = (instr >> 25) & 0x7F
        
        # Extract immediate fields
        imm_i = ((instr >> 20) & 0xFFF)
        imm_s = ((instr >> 25) & 0x7F) << 5 | ((instr >> 7) & 0x1F)
        imm_b = ((instr >> 31) & 0x1) << 12 | ((instr >> 7) & 0x1) << 11 | \
                ((instr >> 25) & 0x3F) << 5 | ((instr >> 8) & 0xF) << 1
        imm_u = instr & 0xFFFFF000
        imm_j = ((instr >> 31) & 0x1) << 20 | ((instr >> 12) & 0xFF) << 12 | \
                ((instr >> 20) & 0x1) << 11 | ((instr >> 21) & 0x3FF) << 1
        
        # Sign extend immediates
        if imm_i & 0x800:  
            imm_i |= 0xFFFFF000
        if imm_s & 0x800:  
            imm_s |= 0xFFFFF000
        if imm_b & 0x1000:  
            imm_b |= 0xFFFFE000
        if imm_j & 0x100000:  
            imm_j |= 0xFFE00000
        
        # Convert register numbers to names
        rd_reg = f'x{rd}'
        rs1_reg = f'x{rs1}'
        rs2_reg = f'x{rs2}'
        
        # Execute instruction based on opcode
        if op == 0x33:  # R-type instructions
            if funct3 == 0x0:  # ADD/SUB
                if funct7 == 0x00:  # ADD
                    self.set(rd_reg, self.get(rs1_reg) + self.get(rs2_reg))
                elif funct7 == 0x20:  # SUB
                    self.set(rd_reg, self.get(rs1_reg) - self.get(rs2_reg))
            elif funct3 == 0x2:  # SLT
                self.set(rd_reg, 1 if self.get(rs1_reg) < self.get(rs2_reg) else 0)
            elif funct3 == 0x5:  # SRL/SRA
                shamt = (instr >> 20) & 0x1F
                if funct7 == 0x00:  # SRL
                    self.set(rd_reg, (self.get(rs1_reg) & 0xFFFFFFFF) >> shamt)
            elif funct3 == 0x6:  # OR
                self.set(rd_reg, self.get(rs1_reg) | self.get(rs2_reg))
            elif funct3 == 0x7:  # AND
                self.set(rd_reg, self.get(rs1_reg) & self.get(rs2_reg))
            else:
                return False
        elif op == 0x13:  # I-type ALU instructions
            if funct3 == 0x0:  # ADDI
                self.set(rd_reg, self.get(rs1_reg) + imm_i)
            else:
                return False
        elif op == 0x03:  # Load instructions
            addr = self.get(rs1_reg) + imm_i
            if funct3 == 0x2:  # LW
                self.set(rd_reg, self.read(addr))
            else:
                return False
        elif op == 0x23:  # Store instructions
            addr = self.get(rs1_reg) + imm_s
            if funct3 == 0x2:  # SW
                self.write(addr, self.get(rs2_reg))
            else:
                return False
        elif op == 0x63:  # Branch instructions
            if funct3 == 0x0:  # BEQ
                if self.get(rs1_reg) == self.get(rs2_reg):
                    self.pc += imm_b - 4  
            elif funct3 == 0x1:  # BNE
                if self.get(rs1_reg) != self.get(rs2_reg):
                    self.pc += imm_b - 4
            elif funct3 == 0x4:  # BLT
                if self.get(rs1_reg) < self.get(rs2_reg):
                    self.pc += imm_b - 4
            else:
                return False
        elif op == 0x67:  # JALR
            target = (self.get(rs1_reg) + imm_i) & ~1  # Clear least significant bit
            self.set(rd_reg, self.pc)
            # Set PC to target address
            self.pc = target - 4

        else:
            # Unrecognized opcode
            return False

        return True

    def state(self):
        """
        Print current state of the simulator.
        This includes PC and register values in binary format.
        Results are stored in output buffer for later writing to file.
        """
        # Format PC as 32-bit binary string
        pc_bin = format(self.pc, '032b')
        
        # Format all 32 registers as binary strings and join with spaces
        regs_bin = ' '.join(format(self.get(f'x{i}'), '032b') for i in range(32))
        
        # Add PC and registers to output buffer
        self.output.append(f"{pc_bin} {regs_bin}")

    def dump(self):
        """
        Print memory contents in binary format.
        This outputs all used memory regions to the output buffer.
        """
        # Print program memory (word by word)
        for addr in range(self.CODE_START, self.CODE_END + 1, 4):
            val = self.read(addr)
            self.output.append(format(val, '032b'))
        
        # Print stack memory (word by word)
        for addr in range(self.STACK_START, self.STACK_END + 1, 4):
            val = self.read(addr)
            self.output.append(format(val, '032b'))
        
        # Print data memory (word by word)
        for addr in range(self.DATA_START, self.DATA_END + 1, 4):
            val = self.read(addr)
            self.output.append(format(val, '032b'))

    def run(self, max: int = 1000):
        """
        Run the simulator until completion or max_instructions limit.
        """
        while self.count < max:
            if not (self.CODE_START <= self.pc <= self.CODE_END):
                break
                
            instr = self.read(self.pc)
            
            # Execute instruction and check for success
            success = self.exec(instr)
            if not success:
                break  # Stop if instruction execution failed
                
            # Update PC and execution counters
            self.pc += 4  
            self.count += 1
            self.cycles += 1  
            
            # Print state after each instruction
            self.state()
            
            # Check for virtual halt
            # The instruction 0x00000063 is "beq x0,x0,0" which creates an infinite loop
            # This is a common way to implement a program end in RISC-V
            if instr == 0x00000063:  # beq zero,zero,0 noice ;)
                break

        # After execution is complete, print final memory state
        self.dump()

def main():
    """
    Main function to parse command line arguments and run the simulator.
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='RISC- Simulator')
    parser.add_argument('input', help='Input file (use - for stdin)')
    parser.add_argument('output', help='Output file (use - for stdout)')
    parser.add_argument('--format', choices=['binary', 'hex'], default='binary',
                      help='Input format (default: binary)')
    parser.add_argument('--max-instr', type=int, default=1000,
                      help='Maximum number of instructions to execute')
    args = parser.parse_args()

    # Read input from stdin or file
    if args.input == '-':
        prog = sys.stdin.readlines()
    else:
        try: # helps to skip statements that are not valid
            with open(args.input, 'r') as f:
                prog = f.readlines()
        except FileNotFoundError:
            print(f"Error: Could not open input file '{args.input}'")
            sys.exit(1)

    # Create simulator instance
    sim = Simulator()
    
    # Load program into simulator memory
    sim.load(prog, fmt=args.format)
    
    # Run the simulation
    sim.run(max=args.max_instr)
    
    # Write output to stdout or file
    if args.output == '-':
        for line in sim.output:
            print(line)
    else:
        try:
            with open(args.output, 'w') as f:
                for line in sim.output:
                    f.write(line + '\n')
        except IOError:
            print(f"Error: Could not write to output file '{args.output}'")
            sys.exit(1)
