#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    if (n <= 1) {
        cout << 0 << '\n';
        return 0;
    }

    vector<int> price_counts(201, 0);
    long long count_variants = 0;

    for (int i = 0; i < n; ++i) {
        int now_price;
        cin >> now_price;

        long long count_of_money_talks_days = 0;
        for (int low_price = 1; low_price < now_price; ++low_price) {
            count_of_money_talks_days += price_counts[low_price];
        }

        count_variants += count_of_money_talks_days;
        price_counts[now_price]++;
    }

    cout << count_variants << '\n';

    return 0;
}