# -*- coding: utf-8 -*-
"""
Spyder Editor

Implements the guessing game. 
The player thinks of a number and the computer has to guess it
"""

mininterval = 1
maxinterval = 100
# The interval can be modified here.

minguess = mininterval - 1
maxguess = maxinterval + 1
# Since I use "//", "guess" will not reach the extreme of the interval.
# So the range should be 1 wider.

maxguesstimes = 0
temp = maxguess - minguess

while temp !=0:
    temp //= 2
    maxguesstimes += 1
# "maxguesstimes" is to define whether the player is lying.

count = 1       # To count the steps.
guess = (maxguess - minguess)//2   
# Defined the initial guess. It will change in the loops.

print("Think of a number between {} and {}!"\
      .format(mininterval,maxinterval))

while True:
    if count > maxguesstimes: 
        print("YOU ARE LYING!!!!!")
        break
    # The number of steps should be no more than "maxguesstimes". Otherwise the player is lying.
    
    print("Is your number greater (>), equal (=), or less (<) than {}"\
          .format(guess),end="?")
        
    tips = str(input("Please answer <,=, or > !  "))
    # The input should be save as str which will not be interpreted.
    
    
    if tips == "=":
        print("I have guessed it!")
        print("I needed {} steps!".format(count))
        break
    
    elif tips == "<":
        maxguess = guess   # The max edge of the interval should be modified as last guess.
        guess -= (maxguess - minguess) // 2   # A new guess which is the middle of the new interval.
        count += 1
    elif tips == ">":
        minguess = guess   # The min edge of the interval should be modified as last guess.
        guess += (maxguess - minguess) // 2   # A new guess which is the middle of the new interval.
        count += 1
        # Bisection method can help minimize the number of steps.
        
    else:
        print("PLEASE ANSWER <,=, OR > !!!!!!!!!!!!  ")
        # To handle the wrong inputs.