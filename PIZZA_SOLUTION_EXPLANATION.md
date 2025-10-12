# Pizza Problem Solution

## Problem Summary (Ukrainian: "Щасливі з піцою")

The turtles want to split their pizza eating sequence into the maximum number of "happy days". A day is happy if no pizza type appears exactly once (i.e., every type must appear 0 times or at least 2 times).

## Algorithm

**Greedy Approach**: Split the sequence as early as possible whenever we have a valid happy day.

### Key Insights:
1. We want to maximize the number of splits
2. Splitting early gives us more opportunities for future splits
3. We need to track how many pizza types have a frequency of exactly 1

### Implementation:
- Use a frequency map to count occurrences of each pizza type in the current segment
- Track the count of pizza types with frequency exactly 1
- When this count becomes 0, we have a valid happy day → split there and start a new segment
- Continue until we process all pizzas

### Time Complexity: O(n)
### Space Complexity: O(k) where k is the number of distinct pizza types

## Test Results:
- Example 1: [4 7 7 4 7 7 7] → 2 happy days ✓
- Example 2: [1 1 1 1 1 1 1 1 1] → 4 happy days ✓
- Example 3: [3 2 2 2 3 2] → 1 happy day ✓

## Usage:
```bash
python3 pizza_solution.py < input.txt
```
