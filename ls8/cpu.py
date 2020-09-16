"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #ram that holds 256 bytes of memory
        self.reg = [0] * 8 #8 general purpose registers
        self.pc = 0 #pc counter
        #set initial value of stack pointer --- possibly not now
        

    def ram_read(self, MAR):
        #MAR: Memory Address Register aka the address being read  
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        #MDR: Memory Data Register aka the value at the MAR
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""


        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        if len(sys.argv) != 2:
            print("Insufficient arguments, re-evaluate and try again")
            sys.exit(1)

        try:
            address = 0

            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    potential_num = comment_split[0].strip()

                    if potential_num == "":
                        continue

                    try:
                        potential_num = int(potential_num, 2)
                    except ValueError:
                        print(f"Invalid number '{potential_num}''")
                        sys.exit(1)

                    self.ram[address] = potential_num
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #This uses the set of instructions LDI, HLT, PRN...etc
        #probably need a running state to make instructions execute
        #add local IR variable hold result from PC
        #get operand_a and operand_b from ram using ram_read()
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        
        running = True

        while running:
            IR = self.ram_read(self.pc) #Instruction Register. stores the memory result that is stored in register PC
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            #if HLT
            if IR == HLT:
                running = False #end the run
                
            
            #if LDI
            elif IR == LDI: #set specified register to specified value
                self.reg[operand_a] = operand_b
                self.pc += 3 #increment to find next instruction

            #if PRN
            elif IR == PRN: #prints the specified value at a register
                print(self.reg[operand_a])
                self.pc += 2 #increment to find next instruction

            elif IR == MUL:
                #multiply the operands calling the operation from alu
                self.alu('MUL', operand_a, operand_b)
                self.pc +=3
        
