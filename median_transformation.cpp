#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int median(int a, int b, int c) {
    vector<int> v = {a, b, c};
    sort(v.begin(), v.end());
    return v[1];
}

vector<int> transform(const vector<int>& a) {
    int n = a.size();
    vector<int> b(n);
    for (int i = 0; i < n; i++) {
        int prev = (i - 1 + n) % n;
        int next = (i + 1) % n;
        b[i] = median(a[prev], a[i], a[next]);
    }
    return b;
}

int main() {
    int n, k;
    cin >> n >> k;
    
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    // Apply transformation k times or until array stabilizes
    for (int i = 0; i < k; i++) {
        vector<int> b = transform(a);
        if (b == a) {
            // Array is stable, no more changes
            break;
        }
        a = b;
    }
    
    // Output the result
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << " ";
        cout << a[i];
    }
    cout << endl;
    
    return 0;
}
