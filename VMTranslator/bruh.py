"""
Building a Hack VM Translator in Python

Github : https://github.com/VishalTheHuman
LinkedIn : https://www.linkedin.com/in/vishalthehuman/

Caution : This Code will not work for any recursive function call 
"""

# Label Dictionary to Store all the Label it encounters 
label = {
    
}
# For Tracking the Jump
global JumpTrack
JumpTrack = 0
# To use store the file name 
global filename
filename = ""
global returnAddressCounter
returnAddressCounter = 0

# Remove the comments in the file
def RemoveComments(string):
    count=0
    flag=False
    for x in range(len(string)):
        if string[x]=="/":
            count+=1
            if(count==2):
                return string[:x-1]
        elif count == 1:
            flag=True
            # Raise error if only one '/' is present
            if count == 1 or (count ==1 and flag==True):
                raise Exception("Error in the Code : Only one '/' is present.")
    if count == 1:
                raise Exception("Error in the Code : Only one '/' is present.")
    return string


# To handle Arithmetic and Logical Operations 
def Arithmetic_Logical(string):
    global JumpTrack
    if string == "add": 
        string= "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n"
    elif string =="sub": 
        string= "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1\n"
    elif string =="neg": 
        string= "@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n"
    elif string =="and": 
        string = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1\n"
    elif string =="or": 
        string = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n"
    elif string =="not": 
        string = "@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n"
    elif string =="eq": 
        string ="@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMP_START_"+str(JumpTrack)+"\nD;JEQ\n@SP\nA=M-1\nM=0\n@JUMP_END_"+str(JumpTrack)+"\n0;JMP\n(JUMP_START_"+str(JumpTrack)+")\n@SP\nA=M-1\nM=-1\n(JUMP_END_"+str(JumpTrack)+")\n"
        JumpTrack+=1
    elif string =="gt": 
        string="@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMP_START_"+str(JumpTrack)+"\nD;JGT\n@SP\nA=M-1\nM=0\n@JUMP_END_"+str(JumpTrack)+"\n0;JMP\n(JUMP_START_"+str(JumpTrack)+")\n@SP\nA=M-1\nM=-1\n(JUMP_END_"+str(JumpTrack)+")\n"
        JumpTrack+=1
    elif string =="lt": 
        string="@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMP_START_"+str(JumpTrack)+"\nD;JLT\n@SP\nA=M-1\nM=0\n@JUMP_END_"+str(JumpTrack)+"\n0;JMP\n(JUMP_START_"+str(JumpTrack)+")\n@SP\nA=M-1\nM=-1\n(JUMP_END_"+str(JumpTrack)+")\n"
        JumpTrack+=1
    else:
        # To raise exceptions for Invalid Conditions 
        raise Exception("Invalid Arithmetic / Logical Expression :" + str(string))
    return string


# To handle Push and Pop operations in the VM Code
def handlePushPop(string):
    # To handle Pop
    if string[0]=="pop":
        if string[1]=="local":
            string = f"@LCL\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
        elif string[1]=="argument":
            string = f"@ARG\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
        elif string[1]=="this":
            string = f"@THIS\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
        elif string[1]=="that":
            string = f"@THAT\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
        elif string[1]=="temp":
            if int(string[2])>=0 and int(string[2])<=7:
                string = f"@5\nD=A\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
            else:
                raise Exception("Pop temp is out of Range [5-12]) : " + str(string))
        elif string[1]=="static":
            # Check if Static Variable lies within the range 
            if int(string[2])>=0 and int(string[2])<=238: # 16-255
                string = f"@{filename}.{string[2]}\nD=A\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
            else:
                raise Exception("Push static is out of Range [16-255]) : "+str(string) )
        elif string[1]=="pointer":
            if string[2] in ["0","1"]:
                if string[2]=="0":
                    string = f"""@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"""
                else :
                    string = f"@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"
            else:
                raise Exception("0 and 1 are the only allowed values for pointer instruction: "+str(string))
        else:
            raise Exception("Invalid Pop Instruction : "+str(string))
    # To handle Push
    elif string[0]=="push":
        if string[1]=="local":
            string = f"@LCL\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif string[1]=="argument":
            string = f"@ARG\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif string[1]=="this":
            string = f"@THIS\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif string[1]=="that":
            string = f"@THAT\nD=M\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif string[1]=="temp":
            if int(string[2])>=0 and int(string[2])<=7:
                string = f"@5\nD=A\n@13\nM=D\n@{string[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            else:
                raise Exception("Push temp is out of Range [5-12]) : "+ str(string))
        elif string[1]=="static":
            # Check if Static Variable lies within the range 
            if int(string[2])>=0 and int(string[2])<=238: # 16-255
                string = f"@{filename}.{string[2]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            else:
                raise Exception("Push static is out of Range [16-255]) : "+str(string))
        elif string[1]=="pointer":
            if string[2] in ["0","1"]:
                if string[2]=="0":
                    string = f"@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                else :
                    string = f"@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif string[1]=="constant":
            string = f"@{string[2]}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        else:
            raise Exception("Invalid Push Instruction : "+str(string))
    return string


# To locate all the labels and put them in the Label Dictionary 
def locateLabels(filename):
    with open(filename,'r') as input_file:
        for string in input_file:
            string = string.strip()
            string = string.split(" ")
            if string[0]=="label":
                # Updating to the Label Dictionary
                label.update({string[1]:f"({string[1]})"})
    input_file.close()


# To handle Branching Instructions
def handleProgramFlow(string):
    # Label Declaration
    if string[0]=="label" and label.get(string[1])!=None:
        return label.get(string[1])
    # Goto : Unconditional Jump
    elif string[0]=="goto" and label.get(string[1])!=None:
        return f"@{string[1]}\n0;JMP\n"
    #If-goto : Conditional Jump
    elif string[0]=="if-goto" and label.get(string[1])!=None:
        return f"\n@SP\nM=M-1\nA=M\nD=M\n@{string[1]}\nD;JNE\n"
    else:
        raise Exception("Label Not Found",string)


# To identify what type of Instruction whether it's Arithmetic/Logical, Push/Pop, Branching and Function 
def handleString(string):
    string = string.strip()
    string = string.split(" ")
    if len(string) == 1:
        # Return
        if string[0] == "return":
            string = handleReturn()
        # Arithmetic / Logical 
        else:
            string = Arithmetic_Logical(string[0])
        return string
    elif len(string) == 2:
        # Branching Statements
        string = handleProgramFlow(string)
        return string
    elif len(string) == 3:
        # Function Declaration
        if string[0] == "function":
            string = handleFunctionCall(string)
        # Function Call
        elif string[0] == "call":
            string = executeFunction(string)
        # Push / Pop
        else:
            string = handlePushPop(string)
        return string
    else:
        # Invalid Command
        raise Exception("Invalid VM Command: " + str(string))


# To handle function Call
def handleFunctionCall(string):
    function_name = string[1]
    num_locals = int(string[2])
    # Making the function as a label in Hack Assembly
    function_code = f"({function_name})\n"
    for i in range(num_locals):
        # Making Space for Local Variables 
        function_code += "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
    return function_code


# To store the Frame when calling the function
def executeFunction(string):
    global returnAddressCounter
    function_name = string[1]
    num_args = int(string[2])
    return_address = f"RETURN_ADDRESS_{function_name}_{returnAddressCounter}"
    returnAddressCounter += 1
    # Saving the frame [Return Address; LCL; ARG; THIS; THAT]
    function_code = f"@{return_address}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    function_code += "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" 
    function_code += "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    function_code += "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    function_code += "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    function_code += f"@SP\nD=M\n@{num_args}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n"
    function_code += f"@SP\nD=M\n@LCL\nM=D\n"
    function_code += f"@{function_name}\n0;JMP\n"
    function_code += f"({return_address})\n"
    return function_code


# To handle Function Return
def handleReturn():
    # Returning Back to the Main Function 
    return_code = "@LCL\nD=M\n@13\nM=D\n"
    return_code += "@5\nA=D-A\nD=M\n@14\nM=D\n"
    return_code += "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"
    return_code += "@ARG\nD=M+1\n@SP\nM=D\n"
    return_code += "@13\nAM=M-1\nD=M\n@THAT\nM=D\n"
    return_code += "@13\nAM=M-1\nD=M\n@THIS\nM=D\n"
    return_code += "@13\nAM=M-1\nD=M\n@ARG\nM=D\n"
    return_code += "@13\nAM=M-1\nD=M\n@LCL\nM=D\n"
    return_code += "@14\nA=M\n0;JMP\n"
    return return_code


# To get the file name
def get_file_name(file):
    global filename
    index = 0
    for x in range(len(file) - 1, 0, -1):
        if file[x] == '/' or file[x] == "\\":
            index = x
            break
    filename = file[index+1:]
    filename = filename[:-3]
    return filename


# Main function which executes Input and Output Operations
def main(file):
    # To get the File name
    get_file_name(file)
    # To Locate all the Labels
    locateLabels(file)
    # Opening the Input File with the same name and Creating a file with same name but with ".asm" extension
    with open(file, 'r') as input_file, open(file[:-2]+"asm", 'w') as output_file:
        output_file.writelines("@256\nD=A\n@SP\nM+D\n")
        for line in input_file:
            stripped_line = line.strip()
            stripped_line=RemoveComments(str(stripped_line))
            if stripped_line:
                print(stripped_line)
                output_file.writelines("//"+stripped_line+"\n")
                stripped_line = handleString(str(stripped_line))
                output_file.writelines(str(stripped_line)+"\n")
        output_file.writelines("\n(END)\n@END\n0;JMP\n")
    input_file.close()
    output_file.close()



main("filename.vm")