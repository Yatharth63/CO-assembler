# CO-assembler

A RISC-V assembler and simulator implementation that converts RISC-V assembly code to binary and simulates its execution.

## Project Structure

- `assembler_project.py`: The RISC-V assembler implementation that converts assembly instructions to binary format
- `simulator.py`: A RISC-V instruction set simulator that executes binary instructions

## Features

### Assembler
- Supports RISC-V RV32I base integer instruction set
- Converts assembly instructions to 32-bit binary format
- Handles various instruction formats (R-type, I-type, S-type, B-type, U-type)
- Supports register mapping for all 32 RISC-V registers

### Simulator
- Emulates RISC-V instruction execution
- Maintains register file (32 general-purpose registers)
- Implements memory management with code and stack segments
- Supports instruction execution with proper state tracking
- Provides debugging capabilities through state dumps

## Supported Instructions

The assembler and simulator support the following RISC-V instructions:

- Arithmetic: `add`, `sub`, `slt`, `sltu`
- Logical: `and`, `or`, `xor`
- Memory: `lw`, `sw`
- Control Flow: `beq`, `bne`, `blt`, `jal`, `jalr`
- Immediate: `addi`

## Usage

1. Write your RISC-V assembly code
2. Use the assembler to convert it to binary
3. Run the simulator to execute the binary instructions

## Requirements

- Python 3.x

## License

This project is open source and available for educational purposes.

