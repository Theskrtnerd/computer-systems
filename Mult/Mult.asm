// This file is based on part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: Mult.asm

// Multiplies R1 and R2 and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// PSEUDO code
// x = R1
// y = R2
// R0 = 0
// b = 1
// if(x < 0) b = -1
// x = abs(x)
// while(x > 0) {
//     R0 += y
//     x--
// }
// if(b < 0) R0 = -R0

@R1
D=M
@x
M=D // x = R1

@R2
D=M
@y
M=D // y = R2

@0
D=A
@R0
M=D	// R0 = 0

@1
D=A
@b
M=D // b = 1

@R1
D=M
@x
M=D // x = R1

// x = abs(x) && b = -1 if x < 0
// start abs
@x
D=M
@EAB
D;JGE

@x
D=M
@x
M=-D

@b
D=M
@b
M=-D

(EAB)
// end abs

(WHILE)
	@x
	D=M	// load x for loop condition
	@ELOO
	D;JLE	// if x <= 0 goto ENDLOOP
	// end of loop condition

	// begin body of while
	@y
	D=M	// D = y
	@R0
	M=D+M	// sum = sum + y
    
	@1
	D=A	// D = 1
	@x
	M=M-D	// x = x - 1	
	// end body of while

	@WHILE
	0;JMP	// jump to loop start

(ELOO)
    @b
	D=M	// load x for loop condition
	@END
	D;JGE	// if b >= 0 goto END

    @R0
    D=M
    @R0
    M=-D

(END)
    @END
    0;JMP

