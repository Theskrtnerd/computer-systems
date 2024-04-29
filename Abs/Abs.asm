// Calculates the absolute value of R1 and stores the result in R0.
// (R0, R1 refer to RAM[0], and RAM[1], respectively.)

// Put your code here. 

// PSEUDO code
// x = R1
// if (x < 0) x = -x
// R0 = x

@R1
D=M
@x
M=D // x = R1

@x
D=M
@END
D;JGE

@x
D=M
@x
M=-D

(END)
    @END
    @x
    D=M
    @R0
    M=D
    0;JMP