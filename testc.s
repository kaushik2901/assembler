ORG 111
LDA B
STA PTR
CLA
LOP,ADD A
ISZ PTR
BUN LOP
STA ANS
HLT
A,DEC 5
B,DEC -4
ANS,DEC 0
PTR,DEC 0
TMP,HEX -FFF
END