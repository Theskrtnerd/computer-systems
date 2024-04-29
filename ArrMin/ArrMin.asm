// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// PSEUDO code
// x = R1
// y = R2
// z = R0
// y = y-1
// while(y > 0) {
//     x = x+1
//     if M(x)-R0 < 0 then R0 = M(x)
//     y--
// }
// R0 = z

@R1
D=M
@x
M=D // x = R1

@R2
D=M
@y
M=D // y = R2

@x
D=M
@z
A=D
D=M
@R0
M=D // R0 = M(x)

@1
D=A
@y
M=M-D // y = y-1

(WHILE)
    @y
	D=M

	@END
	D;JLE	// if y <= 0 goto END

    @1
    D=A
    @x
    M=M+D // x = x+1

    @x
    D=M
    @z
    A=D
    D=M

    // @R0
    // D=D-M

    // @ENDIF
    // D;JLE

    @R0
    D=D-M
    @t
    M=D

    @t
    D=M
    @ENDIF
    D;JLE

    @1
    D=A
    @y
    M=M-D

    @WHILE
    0;JMP

(ENDIF)
    @x
    D=M
    @z
    A=D
    D=M
    @R0
    M=D

    @1
    D=A
    @y
    M=M-D

    @WHILE
    0;JMP

(END)
    @END
    0;JMP