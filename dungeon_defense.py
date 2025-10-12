def is_valid_path(a, b, h, w):
    """Check if arrays a and b define a valid defense line."""
    if len(a) != h or len(b) != w:
        return False
    
    # Simulate the path using the definition:
    # At row i, we go up at column a[i]
    # At column j, we go right at row b[j]
    x, y = 0, 0
    
    for i in range(h):
        # Move right to column a[i]
        while x < a[i]:
            if x >= w or b[x] != y:
                return False
            x += 1
        # Go up from row i to row i+1
        y += 1
    
    # Complete remaining right moves
    while x < w:
        if b[x] != y:
            return False
        x += 1
    
    return True

def solve():
    MOD = 998244353
    
    # Read input
    h, w = map(int, input().split())
    d = list(map(int, input().split()))
    
    # Count frequency of each value
    from collections import Counter
    freq = Counter(d)
    values = sorted(freq.keys())
    
    # Use backtracking to enumerate all valid partitions
    result = [0]  # Use list to allow modification in nested function
    
    def backtrack(idx, a_array, b_array):
        if idx == len(values):
            if len(a_array) == h and len(b_array) == w:
                if is_valid_path(a_array, b_array, h, w):
                    result[0] += 1
            return
        
        val = values[idx]
        cnt = freq[val]
        
        # Try all possible splits of this value
        for ka in range(cnt + 1):
            kb = cnt - ka
            
            # Pruning: check if we can possibly reach h and w
            remaining_after = sum(freq[v] for v in values[idx+1:])
            if len(a_array) + ka + remaining_after < h:
                continue
            if len(b_array) + kb + remaining_after < w:
                continue
            if len(a_array) + ka > h or len(b_array) + kb > w:
                continue
            
            # Value constraints
            if ka > 0 and val > w:
                continue
            if kb > 0 and val > h:
                continue
            
            # Extend arrays and recurse
            a_ext = [val] * ka
            b_ext = [val] * kb
            backtrack(idx + 1, a_array + a_ext, b_array + b_ext)
    
    backtrack(0, [], [])
    print(result[0] % MOD)

if __name__ == "__main__":
    solve()
