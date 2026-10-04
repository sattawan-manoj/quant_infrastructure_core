import numpy as np
from pykalman import KalmanFilter


def compute_tukeys_beta_bounds(historical_betas_vector):
    q25, q75 = np.percentile(historical_betas_vector, [25, 75])
    iqr = q75 - q25

    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr

    return lower_bound, upper_bound


def run_calibrated_kalman_filter(y_prices, x_prices):
    obs_mat = np.vstack([x_prices, np.ones(list(x_prices.shape))]).T[
        :, np.newaxis, :
    ]

    print("[INFO] Executing Expectation-Maximization to calibrate noise settings...")
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
    last_known_valid_beta = raw_betas[0]  # Initializing the memory anchor

    # DAY 50-54: Parametric Boundary Closure Loop
    for idx, beta in enumerate(raw_betas):
        if beta > upper_b or beta < lower_b:
            print(f"⚠️ Day {idx+1}: Limit Breached ({beta:.4f})! [LOOP FREEZE ACTIVE] Using Last Valid Beta: {last_known_valid_beta:.4f}")
            shielded_betas.append(last_known_valid_beta)
        else:
            shielded_betas.append(beta)
            last_known_valid_beta = beta

    return np.array(shielded_betas), intercepts


if __name__ == "__main__":
    print("--- IIT-Bombay Quant Apprenticeship: Day 46-54 Integrated Test ---")

    np.random.seed(42)
    asset_X = np.cumsum(np.random.normal(0, 1, 100)) + 100
    # Simulating a massive market anomaly/shock on Day 50 to test the freeze mechanism
    shocks = np.random.normal(0, 1, 100)
    shocks[50] = 50.0  # Extreme anomaly
    asset_Y = 1.5 * asset_X + shocks

    safe_hedge_ratios, alphas = run_calibrated_kalman_filter(asset_Y, asset_X)

    print("\n[SUCCESS] Integrated Engine successfully resolved loops!")
    print(f"Final Cleaned Betas Array Size: {len(safe_hedge_ratios)}")
