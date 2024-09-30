#include <bits/stdc++.h>
using namespace std;

// Function to compute sum of (1 - P(D_i, R)) for first K objects
double compute_sum(const vector<double>& distances, int K, double R) {
    double sum = 0.0;
    for(int i = 0; i < K; ++i){
        double D = distances[i];
        if(R < 1e-9){
            if(D == 0.0){
                // P = 1
            }
            else{
                // P = 0, so (1 - P) = 1
                sum += 1.0;
            }
        }
        else{
            if(D <= R + 1e-12){
                // P = 1, so (1 - P) = 0
            }
            else{
                double exponent = 1.0 - (D * D) / (R * R);
                double P = exp(exponent);
                sum += (1.0 - P);
            }
        }
    }
    return sum;
}

// Function to truncate a double to 3 decimal places without rounding
double truncate_to_three(double x){
    double truncated = floor(x * 1000.0 + 1e-9) / 1000.0;
    return truncated;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int N;
    cin >> N;
    int K;
    int epsilon_milli;
    cin >> K >> epsilon_milli;
    double epsilon = epsilon_milli / 1000.0;
    int X0, Y0;
    cin >> X0 >> Y0;
    vector<pair<int, int>> objects(N);
    vector<double> distances;
    for(int i = 0; i < N; ++i){
        cin >> objects[i].first >> objects[i].second;
        double dx = (double)(objects[i].first - X0);
        double dy = (double)(objects[i].second - Y0);
        double dist = sqrt(dx * dx + dy * dy);
        distances.push_back(dist);
    }
    // Sort distances ascending
    sort(distances.begin(), distances.end());
    // Binary search for minimal R
    double left = 0.0;
    // Find max distance among first K to set high
    double max_dist = 0.0;
    for(int i = 0; i < K && i < N; ++i){
        max_dist = max(max_dist, distances[i]);
    }
    // To cover the case where sum might require larger R
    double initial_high = 2000.0 * sqrt(2.0);
    double right = initial_high;
    // Binary search with sufficient precision
    for(int iter = 0; iter < 100; ++iter){
        double mid = (left + right) / 2.0;
        double s = compute_sum(distances, K, mid);
        if(s <= epsilon){
            right = mid;
        }
        else{
            left = mid;
        }
    }
    // After binary search, right is the minimal R
    double R = right;
    // Truncate R to three decimal places
    double R_truncated = truncate_to_three(R);
    // To handle the case when truncation might not satisfy the condition, verify and adjust if necessary
    // Because truncation might make R slightly smaller, we need to ensure the condition is met
    // Increment up by 0.001 until condition is satisfied
    // This step ensures that truncation does not violate the condition
    while (true){
        // Compute sum with R_truncated
        double s = compute_sum(distances, K, R_truncated);
        if(s <= epsilon + 1e-9){
            break;
        }
        // Otherwise, increment R_truncated by 0.001
        R_truncated += 0.001;
        // To avoid floating point precision issues
        R_truncated = floor(R_truncated * 1000.0 + 1e-6) / 1000.0;
    }
    // Output with exactly three decimal places
    cout << fixed << setprecision(3) << R_truncated;
}