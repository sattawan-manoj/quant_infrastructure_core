import numpy as np
from pykalman import KalmanFilter


def compute_tukeys_beta_bounds(historical_betas_vector):
    q25, q75 = np.percentile(historical_betas_vector, [25, 75])
    iqr = q75 - q25

    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr

    return lower_bound, upper_bound


def run_calibrated_kalman_filter(y_prices, x_prices):
    obs_mat = np.vstack([x_prices, np.ones_like(x_prices)]).T[
        :, np.newaxis, :
    ]

    
    kf_em = KalmanFilter(
        n_dim_obs=1,
        n_dim_state=2,
        initial_state_mean=np.zeros(2),
        initial_state_covariance=np.ones((2, 2)),
    )
    kf_em = kf_em.em(y_prices, n_iter=5)

    kf = KalmanFilter(
        n_dim_obs=1,
        n_dim_state=2,
        initial_state_mean=np.zeros(2),
        initial_state_covariance=np.ones((2, 2)),
        transition_matrices=np.eye(2),
        observation_matrices=obs_mat,
        transition_covariance=kf_em.transition_covariance,
        observation_covariance=kf_em.observation_covariance,
    )

    state_means, _ = kf.filter(y_prices)

    raw_betas = state_means[:, 0]
    intercepts = state_means[:, 1]

    print("[INFO] Deploying Tukey's Fences Loop Freeze Architecture...")
    lower_b, upper_b = compute_tukeys_beta_bounds(raw_betas)

    shielded_betas = []
    last_known_valid_beta = raw_betas[0]

    for idx, beta in enumerate(raw_betas):
        if beta > upper_b or beta < lower_b:
            print(f"⚠️ Day {idx+1}: Limit Breached ({beta:.4f})! [LOOP FREEZE ACTIVE] Using Last Valid Beta: {last_known_valid_beta:.4f}")
            shielded_betas.append(last_known_valid_beta)
        else:
            shielded_betas.append(beta)
            last_known_valid_beta = beta

    print("[INFO] Initializing mathematical analysis of residuals vector...")
    calculated_betas = np.array(shielded_betas)
    innovations = y_prices - (calculated_betas * x_prices + intercepts)
    
    n = len(innovations)
    mean_inn = np.mean(innovations)
    centered = innovations - mean_inn
    denominator = np.sum(centered ** 2)

    if denominator == 0:
        print("[WARNING] Zero variance detected in innovation sequence.")
        return calculated_betas, intercepts, False

    max_lags = 10
    q_statistic = 0.0
    
    for k in range(1, max_lags + 1):
        numerator = np.sum(centered[k:] * centered[:-k])
        r_k = numerator / denominator
        q_statistic += (r_k ** 2) / (n - k)
        
    q_statistic *= n * (n + 2)
    
    chi_square_critical = 18.307
    
    if q_statistic < chi_square_critical:
        print(f"[PASSED] Ljung-Box Multi-Lag Audit. Q-Stat: {q_statistic:.4f} (Critical Threshold: {chi_square_critical})")
        white_noise_passed = True
    else:
        print(f"[FAILED] Ljung-Box Multi-Lag Audit. Q-Stat: {q_statistic:.4f} (Critical Threshold: {chi_square_critical})")
        white_noise_passed = False

    return calculated_betas, intercepts, white_noise_passed


if __name__ == "__main__":


    np.random.seed(42)
    asset_X = np.cumsum(np.random.normal(0, 1, 1250)) + 100
    
    shocks = np.random.normal(0, 0.5, 1250)
    shocks[500] = 45.0  
    asset_Y = 1.5 * asset_X + shocks

    safe_hedge_ratios, alphas, global_pass_status = run_calibrated_kalman_filter(asset_Y, asset_X)

    if global_pass_status:
        print("\n[FINAL STATUS] PHASE 2 COMPLETE: 100% GREEN PASS STATUS. Adaptive spreads logged seamlessly.")
        print(f"Final Cleaned Betas Array Size: {len(safe_hedge_ratios)}")
    else:
        print("\n[FINAL STATUS] SYSTEM FAILURE: Dynamic parameter updates failed mathematical white noise check.")
