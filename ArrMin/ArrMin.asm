// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// PSEUDO code
// x = R1
// y = R2
// z = R1
// y = y-1
// while(y > 0) {
//     x = x+1
//     if M(x)-z < 0 then z = M(x)
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

(END)
    @END
    0;JMP