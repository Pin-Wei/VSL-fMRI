from VSL_exp_constants import *
import VSL_exp_functions as myFunc

# Create the lists of un-shuffled ISI
sc_ISI_list = myFunc.determine_ISIs(3*4*REPT_SC-1, ISIs, ISI_Ws)
with open('sc_ISI_unshuffled.csv', 'w') as fn:
    fn.write('\n'.join(str(x) for x in sc_ISI_list))

exp_ISI_list = myFunc.determine_ISIs(3*4*REPT_EXP-1, ISIs, ISI_Ws)
with open('exp_ISI_unshuffled.csv', 'w') as fn:
    fn.write('\n'.join(str(x) for x in exp_ISI_list))
