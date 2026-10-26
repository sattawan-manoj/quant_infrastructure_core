import numpy as np
from statsmodels.stats.multitest import multipletests

def filter_false_discoveries(p_values_list, alpha_target=0.05):
    if len(p_values_list) == 0:
        return np.array([]), np.array([])
        
    reject_flags, corrected_p_values, _, _ = multipletests(
        p_values_list, 
        alpha=alpha_target, 
        method='fdr_bh'
    )
    
    return reject_flags, corrected_p_values

if __name__ == "__main__":
    sample_data = [0.001, 0.012, 0.041, 0.048, 0.650]
    
    flags, adjusted_scores = filter_false_discoveries(sample_data)
    
    print(f"Raw Input Scores: {sample_data}")
    print(f"FDR Reject Flags: {flags.tolist()}")
    print(f"Adjusted Scores : {[round(num, 3) for num in adjusted_scores]}")
