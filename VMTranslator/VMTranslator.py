global jumpTrack
jumpTrack = 0

global labels
labels = {}
class VMTranslator:
    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        segment_list = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        asm_string = ""
        if segment in segment_list.keys():
            asm_string = f'@{segment_list[segment]}\nD=M\n@{offset}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == "temp":
            asm_string = f'@R5\nD=A\n@{offset}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == "static":
            asm_string = f'@{16+offset}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
            #raise Exception(asm_string,segment, 16+offset)
        elif segment == "pointer":
            asm_string = f'@R3\nD=A\n@{offset}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == "constant":
            asm_string = f'@{offset}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        else:
            raise Exception("Invalid Push Instruction: ", segment, offset)

        return asm_string

    def vm_pop(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        segment_list = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        asm_string = ""
        if segment in segment_list.keys():
            asm_string = f'@SP\nM=M-1\n@{segment_list[segment]}\nD=M\n@{offset}\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif segment == "temp":
            asm_string = f'@SP\nM=M-1\n@R5\nD=A\n@{offset}\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif segment == "static":
            asm_string = f'@SP\nM=M-1\nA=M\nD=M\n@{16+offset}\nM=D'
            #raise Exception(asm_string,segment, 16+offset)
        elif segment == "pointer":
            asm_string = f'@SP\nM=M-1\n@R3\nD=A\n@{offset}\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        else:
            raise Exception("Invalid Pop Instruction: ", segment, offset)

        return asm_string
    
    def vm_add():
        '''Generate Hack Assembly code for a VM add operation'''
        return '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M'

    def vm_sub():
        '''Generate Hack Assembly code for a VM sub operation'''
        return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1'

    def vm_neg():
        '''Generate Hack Assembly code for a VM neg operation'''
        return '@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1'

    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        global jumpTrack
        jumpTrack +=1
        return f"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMP_START_{jumpTrack}\nD;JEQ\n@SP\nA=M-1\nM=0\n@JUMP_END_{jumpTrack}\n0;JMP\n(JUMP_START_{jumpTrack})\n@SP\nA=M-1\nM=-1\n(JUMP_END_{jumpTrack})\n"

    def vm_gt():
        '''Generate Hack Assembly code for a VM gt operation'''
        global jumpTrack
        jumpTrack +=1
        return f"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMP_START_{jumpTrack}\nD;JGT\n@SP\nA=M-1\nM=0\n@JUMP_END_{jumpTrack}\n0;JMP\n(JUMP_START_{jumpTrack})\n@SP\nA=M-1\nM=-1\n(JUMP_END_{jumpTrack})\n"

    def vm_lt():
        '''Generate Hack Assembly code for a VM lt operation'''
        global jumpTrack
        jumpTrack +=1
        return f"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMP_START_{jumpTrack}\nD;JLT\n@SP\nA=M-1\nM=0\n@JUMP_END_{jumpTrack}\n0;JMP\n(JUMP_START_{jumpTrack})\n@SP\nA=M-1\nM=-1\n(JUMP_END_{jumpTrack})\n"

    def vm_and():
        '''Generate Hack Assembly code for a VM and operation'''
        return '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M'

    def vm_or():
        '''Generate Hack Assembly code for a VM or operation'''
        return '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M'

    def vm_not():
        '''Generate Hack Assembly code for a VM not operation'''
        return '@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1'

    def vm_label(label):
        '''Generate Hack Assembly code for a VM label operation'''
        
        return ""

    def vm_goto(label):
        '''Generate Hack Assembly code for a VM goto operation'''
        return f"@{label}\n0;JMP\n"

    def vm_if(label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        return f"\n@SP\nM=M-1\nA=M\nD=M\n@{label}\nD;JNE\n"

    def vm_function(function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        return ""

    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        return ""

    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        return ""

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        