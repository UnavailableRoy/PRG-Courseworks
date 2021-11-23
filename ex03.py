#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 21:28:41 2021

@author: roy

The 8 Queens Puzzle
"""

bs = 4    # bs means board size. It can be modified to get solutions for any board sizes.

board = []
for i in range(0,bs) :
    board += [[0]*bs]
# The loop makes the variable board a list of lists which is bs*bs size.

##############################

# A function for check whether the Queen can be placed in slot
def possible(y,x) :
    for i in range(0,bs) :
        if board[i][x] == 1 :
            return False
    # check whether there are other Queens in the same x row.
    
    hy1 = y + 1
    hx1 = x + 1
    while 0 <= hy1 < bs and 0 <= hx1 < bs :
        if board[hy1][hx1] == 1 :
            return False
        else:
            hy1 += 1
            hx1 += 1
    # check from the lower right diagonal direction
    
    hy2 = y + 1
    hx2 = x - 1
    while 0 <= hy2 < bs and 0 <= hx2 < bs :
        if board[hy2][hx2] == 1 :
            return False
        else:
            hy2 += 1
            hx2 -= 1
    # check from the lower left diagonal direction
    
    hy3 = y - 1
    hx3 = x + 1
    while 0 <= hy3 < bs and 0 <= hx3 < bs :
        if board[hy3][hx3] == 1 :
            return False
        else:
            hy3 -= 1
            hx3 += 1
    # check from the upper right diagonal direction
    
    hy4 = y - 1
    hx4 = x - 1
    while 0 <= hy4 < bs and 0 <= hx4 < bs :
        if board[hy4][hx4] == 1 :
            return False
        else:
            hy4 -= 1
            hx4 -= 1
    return True
    # check from the upper left diagonal direction
##############################


# A function for printing the board, 0 and 1 represent empty cell and Queen respectively
def print_board() :
    for y in board :
        for x in y :
            if x == 0 :
                print(".",end=" ")
            else:
                print("Q",end=" ")
        print()
    
##############################

count = 0   # Represents the number of queens that have been placed.

# This is a recursive function
def solve() : 
    global bs,board,count
    if count < bs:      # Meeting the condition mean that there are still queens need to be placed.
        for x in range(0,bs):
            if possible(count,x):   # Use count to locate the column where the next queen will be placed.
                board[count][x] = 1   # The queen is placed in the cell of which the possibility is checked
                count += 1            # count the queens that have been placed
                solve()               # Calls itself to place the next queen.
                count -= 1            # Once it meets a dead end or find a solution, it backtracks to seek other solutions.
                board[count][x] = 0   # The two lines after solve() is to remove the last queen that was placed.
        return      # When the for loop finish, there is no solution in this route, it should backtrack to seek other solutions.
    print_board() # If count == bs, all the queens are placed, it will print the board without running the if statement.
    input("More?")
##############################            


