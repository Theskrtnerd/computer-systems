@3
M=1 // r3=1
(WHILEA)
@3
D=M
@2
D=D-M
@END
D;JGE // while r3<r2
@4
M=0 // r4 = 0
(WHILEB)
@4
D=M+1
@2
D=D-M
@ENDWHILEB
D;JGE // while r4 < r2-1
@2
D=M
@7
M=D-1 // r7 = r2-1
@3
D=M
@4
D=D+M
D=D-1
@5
M=D // r5 = r3+r4-1
@7
D=D-M
@CPMID
D;JLE
@7
D=M
@5
M=D
(CPMID) // r5 = min(r5, r7)
@3
D=M
@5
D=D+M
@6
M=D // r6 = r5+r3
@7
D=D-M
@CPRIGHT
D;JLE
@7
D=M
@6
M=D
(CPRIGHT) // r6 = min(r6, r7)
@MERGE
0;JMP
(ENDMERGE)
@3
D=M
D=D+M
@4
M=D+M // r4 += 2*r3
@WHILEB
0;JMP
(ENDWHILEB)
@3
D=M
M=D+M // r3 *= 2
@WHILEA
0;JMP
(MERGE) // def merge(arr, r4, r5, r6):
@4
D=M
@11
M=D // i = r4
@5
D=M+1
@12
M=D // j = r5+1
(WHILEC)
@11
D=M
@5
D=D-M
@ENDMERGE
D;JGT
@12
D=M
@6
D=D-M
@ENDMERGE
D;JGT // while i <= r5 and j <= r6
@1
D=M
@11
D=D+M
@13
M=D // r13 = address(arr[i])
@1
D=M
@12
D=D+M
@14
M=D // r14 = address(arr[j])
@13
A=M
D=M
@14
A=M
D=D-M
@FINALIF
D;JGT // if arr[i] <= arr[j]
@11
D=M
@11
M=D+1 // i += 1
@WHILEC
0;JMP
(FINALIF) // else
@14
A=M
D=M
@15
M=D // temp = arr[j]
@12
D=M
@8
M=D // k = j
(FOR)
@8
D=M
@11
D=D-M
@ENDFOR
D;JLE // if k <= i ENDFOR
@1
D=M-1
@8
D=D+M
@x
A=D
D=M
@x
M=D // x = arr[k-1]
@1
D=M
@8
D=D+M
@y
M=D
@x
D=M
@y
A=M
M=D // arr[k] = x
@8
D=M
@8
M=D-1 // k--
(ENDFOR)
@15
D=M
@13
A=M
M=D // arr[i] = temp
@11
D=M
@11
M=D+1 // i += 1
@12
D=M
@12
M=D+1 // j += 1
@5
D=M
@5
M=D+1 // r5 += 1
@WHILEC
0;JMP
(END)
@0
M=-1
@LOOP
0;JMP
(LOOP)
@LOOP
0;JMP