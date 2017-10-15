#!/bin/bash -x
python ../asm.py valid_simple
echo
python ../asm.py valid_complex
echo
python ../asm.py invalid_simple
echo
python ../asm.py invalid_complex
