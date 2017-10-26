#!/usr/bin/python2.7
import os
import sys
import os.path

put_templ = """
sub {r1} {r1}
sub {r2} {r2}
sub {r3} {r3}
mov {r2} 0x{v0}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}
mov {r2} 4
shl {r1} {r2}
mov {r2} 0x{v1}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}
mov {r2} 4
shl {r1} {r2}
mov {r2} 0x{v2}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}
mov {r2} 4
shl {r1} {r2}
mov {r2} 0x{v3}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}
mov {r2} 4
shl {r1} {r2}
mov {r2} 0x{v4}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}
mov {r2} 4
shl {r1} {r2}
mov {r2} 0x{v5}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}
mov {r2} 4
shl {r1} {r2}
mov {r2} 0x{v6}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}
mov {r2} 4
shl {r1} {r2}
mov {r2} 0x{v7}
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}

"""

add_templ = """
mov {r3} 0
sub {r3} {r2}
sub {r1} {r3}

"""

pull_templ = """
mov {r3} 0
sub {r3} {r2}
mov {r1} 0
sub {r1} {r3}

"""
def main():
    fname = sys.argv[1]
    with open(fname) as fin:
        buf = fin.readlines()
        text = translate(fname, buf)
        with open(os.path.splitext(fname)[0]+'.bin', 'w+') as fout:
            fout.write(text)


def translate(fname, buf):
    obuf = ""

    r = dict([ (dz, i) for i, dz in enumerate('r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 r16 r17 r18 r19 r20 r21 r22 r23 r24 r25 four mfour fr sp lr pc zero'.split(' '))])
    op = dict([ (dz, i) for i, dz in enumerate('sub mov br ld st shl rot nor csub cmov cbr cld cst cshl crot cnor'.split(' '))])
    op.update({'subn':0, 'csubn': 8})
#    print r
#    print op

    #with open(fname) as fin:
    #    with open(fname+'_pp', 'w+') as fout:
    for lnum, line in enumerate(buf): #fin.readlines()):
        tokens = line.split()
        #print tokens
        if len(tokens) > 0:
            if tokens[0] == 'put':
                if len(tokens) != 5:
                    print 'invalid operand count at {}, {}:'.format(lnum+1, fname)
                    print line.strip()
                    exit(1)
                val = [hex((int(tokens[2], 16) & (0xf << (4*p))) >> (4*p))[2:] for p in range(7,-1,-1)]
                print val
#                exit(9)
#                val = tokens[2][2:]
                r1=tokens[1]
                r2=tokens[3]
                r3=tokens[4]
                if (r1 in [r2, r3]) or (r2 in [r1,r3]) or (r2 in [r1,r3]):
                    print 'invalid (overlaping) combination of registers at line {}, {}'.format(lnum, fname)
                    exit(1)
                s = put_templ.format(r1=r1, r2=r2, r3=r3,
                   v0=val[0], v1=val[1], v2=val[2], v3=val[3], v4=val[4], v5=val[5], v6=val[6], v7=val[7])
                #fout.write(s)
                obuf += s
            elif tokens[0] == 'add':
                if len(tokens) != 4:
                    print 'invalid operand count at {}, {}:'.format(lnum+1, fname)
                    print line.strip()
                    exit(1)

                r1=tokens[1]
                r2=tokens[2]
                r3=tokens[3]
                s = add_templ.format(r1=r1, r2=r2, r3=r3)
                #fout.write(s)
                obuf += s
            elif tokens[0] == 'pull':
                if len(tokens) != 4:
                    print 'invalid operand count at {}, {}:'.format(lnum+1, fname)
                    print line.strip()
                    exit(1)
                r1=tokens[1]
                r2=tokens[2]
                r3=tokens[3]
                s = pull_templ.format(r1=r1, r2=r2, r3=r3)
                #fout.write(s)
                obuf += s
            else:
                #fout.write(line)
                obuf += line


    adr = 0
    obuf = obuf.split('\n')
    buf = obuf
    obuf = ''
#    with open(fname+'_pp') as fin:
#        with open(os.path.splitext(fname)[0]+'.bin', 'w+') as fout:
    for lnum, line in enumerate(buf): #fin.readlines()):
        tokens = line.split()
        print tokens, adr

        if len(tokens) > 0:
            if tokens[0] in op.keys():
                if tokens[0] == 'mov':
                    try:
                        imm = int(tokens[2])
                    except ValueError as e:
                        try:
                            imm = int(tokens[2], 16)
                        except ValueError as e:
                            if tokens[2][0]=="'" and tokens[2][2]=="'":
                                imm = ord(tokens[2][1])

                    obuf += ( chr(((r[tokens[1]] & 0b1) << 7) | (imm & 0b1111111) ) )
                    obuf += ( chr((op[tokens[0]] << 4) | ((r[tokens[1]] & 0b11110) >> 1)) )
                    #fout.write( chr(((r[tokens[1]] & 0b1) << 7) | (imm & 0b1111111) ) )
                    #fout.write( chr((op[tokens[0]] << 4) | ((r[tokens[1]] & 0b11110) >> 1)) )
                    adr += 2
                elif tokens[0] in ['subn', 'csubn']:
                    obuf += ( chr(((r[tokens[1]] & 0b1) << 7) | ((r[tokens[2]] & 0b11111) << 2) | 0b01) )
                    obuf += ( chr((op[tokens[0]] << 4) | ((r[tokens[1]] & 0b11110) >> 1)))
                    #fout.write( chr(((r[tokens[1]] & 0b1) << 7) | ((r[tokens[2]] & 0b11111) << 2) | 0b01) )
                    #fout.write( chr((op[tokens[0]] << 4) | ((r[tokens[1]] & 0b11110) >> 1)))
                    adr += 2
                else:
                    obuf += ( chr(((r[tokens[1]] & 0b1) << 7) | ((r[tokens[2]] & 0b11111) << 2)) )
                    obuf += ( chr((op[tokens[0]] << 4) | ((r[tokens[1]] & 0b11110) >> 1)) )
                    #fout.write( chr(((r[tokens[1]] & 0b1) << 7) | ((r[tokens[2]] & 0b11111) << 2)) )
                    #fout.write( chr((op[tokens[0]] << 4) | ((r[tokens[1]] & 0b11110) >> 1)) )
                    adr += 2
            elif tokens[0].startswith('#'):
                pass
            else:
                print 'unknown yolo at line {}, {}:'.format(lnum+1, fname+'_pp')
                print line.strip()
                exit(1)
    return obuf


if __name__ == "__main__":
    main()
