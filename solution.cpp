#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<string> grid(n);
    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }
    
    vector<tuple<int, int, int, int, int>> operations;
    
    // For each row, find segments of consecutive 1s and paint them
    for (int i = 0; i < n; i++) {
        int j = 0;
        while (j < m) {
            if (grid[i][j] == '1') {
                int start = j;
                // Find the end of this segment of 1s
                while (j < m && grid[i][j] == '1') {
                    j++;
                }
                int end = j - 1;
                // Paint row i+1 (1-indexed), columns start+1 to end+1 with white
                operations.push_back({i+1, i+1, start+1, end+1, 1});
            } else {
                j++;
            }
        }
    }
    
    // Output the operations
    cout << operations.size() << endl;
    for (const auto& op : operations) {
        cout << get<0>(op) << " " << get<1>(op) << " " 
             << get<2>(op) << " " << get<3>(op) << " " 
             << get<4>(op) << endl;
    }
    
    return 0;
}
