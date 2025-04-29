import itertools
import pandas as pd

def calculate_noisy_or_probability(active_nodes, weights, leak):
    """
    active_nodes: list of booleans indicating which causes are active (True = active)
    weights: list of activation probabilities w_i for each cause
    leak: leak probability
    """
    product = 1.0
    for is_active, w in zip(active_nodes, weights):
        if is_active:
            product *= (1 - w) 
    total_failure = (1 - leak) * product
    return 1 - total_failure  

def generate_noisy_or_table(weights, labels, leak):
    n = len(weights)
    combinations = list(itertools.product([False, True], repeat=n))
    
    table = []
    for combo in combinations:
        prob_true = calculate_noisy_or_probability(combo, weights, leak)
        prob_false = 1 - prob_true
        row = {
            **{f'{label} ({weight})': int(state) for (label, weight), state in zip(zip(labels, weights), combo)},
            'P(C=true)': round(prob_true, 6),
            'P(C=false)': round(prob_false, 6)
        }
        table.append(row)
    
    return pd.DataFrame(table)

if __name__ == "__main__":
    # Your given data
    weights = [0.2, 0.6, 0.15, 0.6, 0.2, 0.1, 0.45]
    labels = [
        "DS0015", "DS0010", "DS0017", "DS0022", "DS0029.001", "DS0029.002", "DS0029.003"
    ]
    leak = 0.02

    noisy_or_table = generate_noisy_or_table(weights, labels, leak)
    name = "Klaus"
    # Before printing:
    pd.set_option('display.max_rows', None)     
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.width', None)        
    pd.set_option('display.max_colwidth', None) 
    noisy_or_table.to_excel(f'knotenwahrscheinlichkeitstabelle_{name}.xlsx', index=False)