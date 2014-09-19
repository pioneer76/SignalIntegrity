from numpy import matrix
from numpy import array

from Z0KHelper import Z0KHelper

def ABCD2S(ABCD,Z0=None,K=None):
    (Z0,K)=Z0KHelper((Z0,K),len(ABCD))
    Z01=Z0.item(0,0)
    Z02=Z0.item(1,1)
    K1=K.item(0,0)
    K2=K.item(1,1)
    C11=matrix([[0,0],[1.0/(2.0*K2),Z02/(2.0*K2)]])
    C12=matrix([[1.0/(2.0*K1),-Z01/(2.0*K1)],[0,0]])
    C21=matrix([[0,0],[1.0/(2.0*K2),-Z02/(2.0*K2)]])
    C22=matrix([[1.0/(2.0*K1),Z01/(2.0*K1)],[0,0]])
    return array((C21+C22*ABCD)*((C11+C12*ABCD).getI())).tolist()
