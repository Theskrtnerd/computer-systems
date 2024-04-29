// Sorts the array of length R2 whose first element is at RAM[R1] in descending order in place. Sets R0 to True (-1) when complete.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@i
    M=0

(OUTTER)
    @j
    M=0

(INNER)
    // *(R1+j)
    @R1
    D=M
    @j
    A=M+D
    D=A
    @x
    M=D
    @y
    M=D+1

    @x
    A=M
    D=M
    @NEGX
    D;JLT
    @POSX
    D;JGT

(COMPARE)
    @x
    A=M
    D=M
    @y
    A=M
    D=D-M
    @SWAP
    D;JGT

(CHECK)
    // check if (j >= R2-i-1)
    @i
    D=M
    @R2
    D=D+1
    D=M-D
    @j
    M=M+1
    D=D-M
    @INNER
    D;JGT

    // check if (i >= R2-1)
    @i
    M=M+1
    D=M
    @R2
    D=M-D
    D=D-1
    @OUTTER
    D;JGT

(END)
    @R0
    M=-1
    @END
    0;JMP

(SWAP)
    @x
    A=M
    D=M
    @R4
    M=D

    @y
    A=M
    D=M
    @x
    A=M
    M=D

    @R4
    D=M
    @y
    A=M
    M=D

    @CHECK
    0;JMP

(NEGX)
    @y
    A=M
    D=M
    @CHECK
    D;JGT
    @COMPARE
    0;JMP

(POSX)
    @y
    A=M
    D=M
    @SWAP
    D;JLT
    @COMPARE
    0;JMP