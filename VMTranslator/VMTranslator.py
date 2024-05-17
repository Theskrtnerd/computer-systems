class VMTranslator:

    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        common_string = f'\nD=M\n@{offset}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        asm_string = ""
        if segment == "local":
            asm_string = "@LCL" + common_string
        elif segment == "argument":
            asm_string = "@ARG" + common_string
        elif segment == "this":
            asm_string = "@THIS" + common_string
        elif segment == "that":
            asm_string = "@THAT" + common_string
        elif segment == "temp":
            asm_string = f'@R5\nD=A\n@{offset}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == "static":
            asm_string = f'@{(sys.argv[1].split("."))[0]}.{offset}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == "pointer":
            asm_string = f'@R3\nD=A\n@{offset}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == "constant":
            asm_string = f'@{offset}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        else:
            raise Exception("Invalid Push Instruction: ", segment, offset)

        return asm_string

    def vm_pop(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        common_string = f"\n@13\nM=D\n@{offset}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
        asm_string = ""
        if segment == "local":
            asm_string = "@LCL\nD=M" + common_string
        elif segment == "argument":
            asm_string = "@ARG\nD=M" + common_string
        elif segment == "this":
            asm_string = "@THIS\nD=M" + common_string
        elif segment == "that":
            asm_string = "@THAT\nD=M" + common_string
        elif segment == "temp":
            if int(offset) >= 0 and int(offset) <= 7:
                asm_string = "@5\nD=A" + common_string
            else:
                raise Exception("Invalid Pop Temp (out of range [5-12]) ", segment, offset)
        elif segment == "static":
            if int(offset)>=0 and int(offset)<=238: # 16-255
                asm_string = f"@static.{offset}\nD=A\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
            else:
                raise Exception("Pop static is out of Range [16-255]) : ", segment, offset)
        elif segment == "pointer":
            if str(offset) in ["0","1"]:
                if str(offset)=="0":
                    asm_string = f"@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"
                else:
                    asm_string = f"@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"
            else:
                raise Exception("0 and 1 are the only allowed values for pointer instruction: ", segment, offset)
        else:
            raise Exception("Invalid Pop Instruction: ", segment, offset)

        return asm_string

    def vm_add():
        '''Generate Hack Assembly code for a VM add operation'''
        return '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M'

    def vm_sub():
        '''Generate Hack Assembly code for a VM sub operation'''
        return '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D-M'

    def vm_neg():
        '''Generate Hack Assembly code for a VM neg operation'''
        return '@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1'

    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        return ""

    def vm_gt():
        '''Generate Hack Assembly code for a VM gt operation'''
        return ""

    def vm_lt():
        '''Generate Hack Assembly code for a VM lt operation'''
        return ""

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
        return ""

    def vm_if(label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        return ""

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

        