#!/usr/bin/python
import sys
import os
from time import sleep
from collections import namedtuple

MEMSIZE = 1024 * 1024 * 1

#def namedkokot(pica, rit):
#    rit = rit.split(' ')
#    wololo = dict([ (dz, 0) for dz in rit])
#    print wololo

class Regfile(object):
    def __init__(self, *k):
        self.r = dict([ (dz, 0) for dz in 'r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 r16 r17 r18 r19 r20 r21 r22 r23 r24 r25 r26 r27 sp lr pc zero'.split(' ')])

    def __getitem__(self, i):
        if type(i) is int:
            return self.r[self.r.keys()[i]]
        else:
            return self.r[i]
    def __setitem__(self, i, v):
        if type(i) is int:
            self.r[self.r.keys()[i]] = v
        else:
            self.r[i] = v

    def __repr__(self):
        return repr(self.r)

class CPU(object):
    def __init__(self, mmu):
        self.mmu = mmu
        mmu.add_cpu(self)
        self.regs = Regfile()

        self.ops = {0b000: self.sub_i
                    0b001: self.mov_i}

    def fetch_instruction(self, addr):
        return self.mmu.read(addr, 2)

    def sub_i(self, r1, r2, imm):
        print 'sub', r1, r2
        self.regs['pc'] += 2
        self.regs[r1] += self.regs[r2]

    def mov_i(self, r1, r2, imm):
        # TODO: make register name <-> id lookup function
        self.regs['pc'] += 2
        self.regs[r1] = imm

    #def br_i


    #def ld_i

    #def st_i

    #def shl_i

    #def rot_i

    #def nor_i

    def execute_instruction(self, i):
        opcode = (i[0] & 0b01110000) >> 4;

        r1 = ((i[0] & 0b1111) << 1) | ((i[1] & 0b10000000) >> 7)
        r2 = ((i[1] & 0b01111100) >> 2)

        imm = i[1] & 0b1111111

        if self.ops.has_key(opcode):
            self.ops[opcode](r1, r2, imm)

    def make_step(self):
        i = self.fetch_instruction(self.regs['pc'])
        print i
        self.execute_instruction(i)

    def show(self):
        print self.regs


class MMU(object):
    def __init__(self, mem):
        self.cpus = []
        self.mem = mem

    def add_cpu(self, cpu):
        self.cpus.append(cpu)

    def read(self, addr, size):
        print "len mem =", len(self.mem)
        return [self.mem[addr+i] for i in xrange(size)]

class Memory(object):
    def __init__(self, size=MEMSIZE):
        self.mem = [0]*size
        self.ln = size

    def __getitem__(self, i):
        return self.mem[i % self.ln]

    def __setitem__(self, i, v):
        self.mem[i % self.ln] = v

    def load_file(self, filename):
        with open(filename, 'rb') as fin:
            self.mem = map(ord, fin.read())
            print "mem size=", len(self.mem)
            self.ln = len(self.mem)
            sleep(1)

    def __len__(self):
        return self.ln #len(self.mem)

class Machine(object):
    def __init__(self):
        self.mem = Memory()
        self.mmu = MMU(self.mem)
        self.cpu = CPU(self.mmu)

    def load(self, filename):
        self.mem.load_file(filename)

    def run(self):
        while(True):
            self.cpu.make_step()
            self.cpu.show()

if __name__ == '__main__':
    m = Machine()
    m.load('kkt.bin')
    m.run()
