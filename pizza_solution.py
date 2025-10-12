#!/usr/bin/env python3
"""
Solution for "Happy with Pizza" problem

A day is happy if no pizza type appears exactly once.
We need to find the maximum number of continuous parts we can split
the sequence into, where each part is a happy day.

Strategy: Greedy approach - split as soon as we have a valid happy day.
"""

def solve():
    n = int(input())
    pizzas = list(map(int, input().split()))
    
    happy_days = 0
    freq = {}
    types_with_count_one = 0  # Number of pizza types with frequency exactly 1
    
    for i in range(n):
        pizza = pizzas[i]
        
        # Update frequency map
        if pizza in freq:
            if freq[pizza] == 1:
                # This pizza type had count 1, now it will have count 2
                types_with_count_one -= 1
            freq[pizza] += 1
        else:
            # New pizza type with count 1
            freq[pizza] = 1
            types_with_count_one += 1
        
        # Check if current segment is valid (no type with count exactly 1)
        if types_with_count_one == 0:
            # We found a happy day! Split here and start a new segment
            happy_days += 1
            freq = {}
            types_with_count_one = 0
    
    print(happy_days)

if __name__ == "__main__":
    solve()
