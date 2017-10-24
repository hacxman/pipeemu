put r2 0xeeee0000 r3 r4
mov r1 308
st r2 r1
put sp 0x000e0000 r3 r4
put r1 0xeeef0000 r3 r4
mov r2 1
st r1 r2
mov r1 302
br r1 r10
mov r17 10
mov r1 'H'
put r2 0xffffffef r3 r4
st r2 r1
mov r1 'E'
st r2 r1
mov r1 'l'
st r2 r1
mov r1 'L'
st r2 r1
mov r1 'L'
st r2 r1
mov r1 'o'
st r2 r1
mov r1 32
st r2 r1
put r11 0xfffffff3 r12 r13
st r11 r12
mov r1 'w'
st r2 r1
mov r1 'o'
st r2 r1
mov r1 'l'
st r2 r1
mov r1 'e'
st r2 r1
mov r1 '!'
st r2 r1
mov r1 13
st r2 r1
mov r1 10
st r2 r1



put r11 0xf00d0000 r12 r13
mov r12 0
st r11 r12

mov r18 1
sub r17 r18
mov r19 2
cbr r19 r20


mov r0 0
mov r1 0
put r1 0x68404c37 r20 r21
put r2 0xfffffff7 r22 r23
st r2 r1
