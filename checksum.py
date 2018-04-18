# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 22:11:33 2018

@author: Humberto
"""

def calc_checksum(string):
    sum = 0

    for i in range(len(string)):
        sum = sum + ord(string[i])

    temp = sum % 64  # mod64 - can change to other length
    print (temp)
    rem = -temp  # two's complement, easier way
    print(rem)
    
    return '%2X' % (rem & 0xFF)

test = calc_checksum('string')
print (test)