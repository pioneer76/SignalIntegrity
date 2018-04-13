'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
# port 1 and 2 are a thru
# port 3 picks off the wave going from port 1 to 2
# port 4 (optional) picks off the wave going from port 2 to port 1
def DirectionalCoupler(ports):
    if ports==3:
        return [[0,1,0],
                [1,0,0],
                [1,0,0]]
    elif ports==4:
        return [[0,1,0,0],
                [1,0,0,0],
                [1,0,0,0],
                [0,1,0,0]]
