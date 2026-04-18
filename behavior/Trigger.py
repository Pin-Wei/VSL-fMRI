from psychopy import core
from pykeyboard import PyKeyboard
import sys

k = PyKeyboard()
Ver = int(sys.argv[1])
TR_number = [59, 115, 217]
core.wait(10)

for count in range(TR_number[Ver]):
    # k.tap_key('num_5')
    k.tap_key('5')
    core.wait(2)
