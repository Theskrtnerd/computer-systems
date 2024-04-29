// Calculates R1 + R2 - R3 and stores the result in R0.
// (R0, R1, R2, R3 refer to RAM[0], RAM[1], RAM[2], and RAM[3], respectively.)

// Put your code here.

// PSEUDO code
// x = R1
// y = R2
// z = R3

// x = x + y - z
// R0 = x

@R1
D=M
@x
M=D // x = R1

@R2
D=M
@y
M=D // y = R2

@R3
D=M
@z
M=D // z = R3

@y
D=M // D = y
@x
M=D+M // x = x+y

@z
D=M // D = z
@x
M=M-D // x = x-z

@x
D=M
@R0
M=D