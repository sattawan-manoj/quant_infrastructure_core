import numpy as np
from pykalman import KalmanFilter


def compute_tukeys_beta_bounds(historical_betas_vector):
    q25, q75 = np.percentile(historical_betas_vector, [25, 75])
    iqr = q75 - q25

    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr

    return lower_bound, upper_bound


def apply_shielded_kalman_step(kalman_beta, lower_bound, upper_bound):
    beta_clipped = np.clip(kalman_beta, lower_bound, upper_bound)
    return beta_clipped


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

    print("[INFO] Deploying Tukey's Fences protective bounding layer...")
    lower_b, upper_b = compute_tukeys_beta_bounds(raw_betas)

    shielded_betas = []
    for beta in raw_betas:
        safe_beta = apply_shielded_kalman_step(beta, lower_b, upper_b)
        shielded_betas.append(safe_beta)

    return np.array(shielded_betas), intercepts


if __name__ == "__main__":
    print("--- IIT-Bombay Quant Apprenticeship: Day 46-49 Engine Test ---")

    np.random.seed(42)
    asset_X = np.cumsum(np.random.normal(0, 1, 100)) + 100
    asset_Y = 1.5 * asset_X + np.random.normal(0, 1, 100)

    safe_hedge_ratios, alphas = run_calibrated_kalman_filter(asset_Y, asset_X)

    print("\n[SUCCESS] Engine successfully resolved processing loops!")
    print(f"Initial 5 Safe Hedge Ratios (Beta): {safe_hedge_ratios[:5]}")
    print(f"Initial 5 Intercepts (Alpha): {alphas[:5]}")
