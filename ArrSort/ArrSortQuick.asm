@R3
M=0 // r3=0
@R2
D=M
@R4
M=D-1 // r4=r2-1
(QSORT)
@R3
D=M
@R4
D=D-M // d=r3-r4
@END
D;JGE // if d >= 0 (or r3 >= r4) END
@PART
0;JMP
(ENDPART)
@R5
D=M
@x
M=D-1 // x = r5-1
@R5
D=M
@y
M=D+1 // y = r5+1
@R4
D=M
@z
M=D // z = r4
@x
D=M
@R4
M=D // r4=x
@QSORT
0;JMP
@y
D=M
@R3
M=D // r3=y
@z
D=M
@R4
M=D // r4=z
QSORT
0;JMP
END
0;jmp
(PART)
@R1
D=M
@R4
D=D+M
@R6
A=D 
D=M
@R6
M=D // r6 = arr[r4]
@R3
D=M
@R7
M=D-1 // r7 = r3-1
@R3
D=M
@R8
M=D // r8 = r3
(LOOP)
@R8 
D=M
@R4
D=D-M // D=r8-r4
@ENDLOOP
D;JGE // if D>=0 or r8 >= r4 ENDLOOP
@R1
D=M
@R8
D=D+M
A=D
D=M
@R6
D=D-M // D = arr[r8]-r6
@ENDIF
D;JGE // if arr[r8] >= r6 ENDIF
@R7
D=M
@R7
M=D+1 // r7++
@R1
D=M
@R7
D=D+M
@R9
M=D // r9 = address(r7)
@R1
D=M
@R8
D=D+M
@R10
M=D // r10 = address(r8)
@SWAPX
0;JMP
(ENDIF)
@R8
D=M
@R8
M=D+1 // r8++
@LOOP
0;JMP // continue LOOP
(ENDLOOP)
@R1
D=M+1
@R7
D=D+M
@R9
M=D // R9 = address(r7+1)
@R1
D=M
@R4
D=D+M
@R10
M=D // R10 = address(r4)
@SWAPY
0;JMP
(ENDSWAPY)
@R7
D=M
@R5
M=D+1 // r5=r7+1
@ENDPART
0;JMP // return
(SWAPX)
@R9
A=M
D=M
@R14
M=D // r14 = arr[r9]
@R10
A=M
D=M
@R9
A=M
M=D // arr[r9] = arr[r10]
@R14
D=M
@R10
A=M
M=D // arr[r10] = r14
@ENDIF
0;JMP
(SWAPY)
@R9
A=M
D=M
@R14
M=D // r14 = arr[r9]
@R10
A=M
D=M
@R9
A=M
M=D // arr[r9] = arr[r10]
@R14
D=M
@R10
A=M
M=D // arr[r10] = r14
@ENDSWAPY
0;JMP
(END)
@END
0;JMP    