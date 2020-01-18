# Implemented from: https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
def knapsack(cap, item_weights, item_values):
    n = len(item_values)
    K = [[0 for x in range(cap + 1)] for x in range(n + 1)]

    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(cap + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif item_weights[i - 1] <= w:
                K[i][w] = max(item_values[i - 1] + K[i - 1][w - item_weights[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    return K[n][cap]
