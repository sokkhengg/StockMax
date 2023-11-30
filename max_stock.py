from itertools import combinations

def total_value(combination):
    return sum(item[1] for item in combination)

def total_stocks(combination):
    return sum(item[0] for item in combination)

def exhaustive_search(M, items): 
    # M = amount, items = list of tuples (stock_count, stock_value)
    best = None 
    for r in range(len(items) + 1): # r = number of stocks to buy
        for candidate in combinations(items, r): # candidate = list of tuples (stock_count, stock_value)
            if total_value(candidate) <= M:
                if best is None or total_stocks(candidate) > total_stocks(best):
                    best = candidate
    return best

def dynamic_programming(M, items):
    # M = amount, items = list of tuples (stock_count, stock_value)
    dp = [[0 for _ in range(M + 1)] for _ in range(len(items) + 1)]

    for i in range(1, len(items) + 1): # i = number of stocks to buy
        for j in range(1, M + 1): # j = amount
            stock_count, stock_value = items[i - 1] 
            if stock_value <= j: # if stock_value > j, then we can't buy it
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - stock_value] + stock_count) 
            else:
                dp[i][j] = dp[i - 1][j] # we can't buy it, so we just use the previous value
    
    return dp[len(items)][M]

def read_test_cases(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    test_cases = []
    i = 0
    while i < len(lines):
        if lines[i].strip():
            N = int(lines[i].strip()) 
            stocks_and_values = [list(map(int, lines[j].strip().split())) for j in range(i + 1, i + N + 1)]
            amount = int(lines[i + N + 1].strip())
            test_cases.append((N, stocks_and_values, amount))
            i += N + 2
        else:
            i += 1
    return test_cases

def write_results_to_file(file_path, results):
    with open(file_path, 'w') as file:
        for result in results:
            file.write(f"Exhaustive Search - Max Stocks: {result['exhaustive']}, Combination: {result['combination']}\n")
            file.write(f"Dynamic Programming - Max Stocks: {result['dynamic']}\n\n")

# Main execution
if __name__ == "__main__":
    input_file_path = 'input.txt'
    output_file_path = 'output.txt'

    test_cases = read_test_cases(input_file_path)
    results = []

    for N, stocks_and_values, amount in test_cases:
        best_combination = exhaustive_search(amount, stocks_and_values)
        max_stocks_exhaustive = total_stocks(best_combination) if best_combination else 0
        max_stocks_dynamic = dynamic_programming(amount, stocks_and_values)
        
        results.append({
            'exhaustive': max_stocks_exhaustive,
            'dynamic': max_stocks_dynamic,
            'combination': best_combination
        })

    write_results_to_file(output_file_path, results)
