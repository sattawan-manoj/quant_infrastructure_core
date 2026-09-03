import numpy as np
import matplotlib.pyplot as plt

# --- स्टेप 1: एक बहुत ही अजीब/टेढ़ा-मेढ़ा (Skewed) डेटा बनाना ---
# हम 100,000 ऐसे नंबर्स जनरेट कर रहे हैं जो नॉर्मल नहीं हैं (Exponential Data)
skewed_population = np.random.exponential(scale=2.0, size=100000)

# --- स्टेप 2: सिमुलेशन के पैरामीटर्स सेट करना ---
num_samples = 5000  # हमें कुल 5000 बार सैंपल लेने हैं
sample_size = 100   # हर बार डेटा में से 100 रैंडम नंबर्स उठाने हैं

# सभी 5000 औसतों को स्टोर करने के लिए एक खाली लिस्ट
sample_means = []

# --- स्टेप 3: लूप चलाकर सैंपल का औसत निकालना ---
for i in range(num_samples):
    # आबादी में से रैंडमली 100 नंबर्स चुनना
    random_sample = np.random.choice(skewed_population, size=sample_size)
    
    # उन 100 नंबर्स का औसत (Mean) निकालना
    sample_mean = np.mean(random_sample)
    
    # इस औसत को अपनी लिस्ट में जोड़ते जाना
    sample_means.append(sample_mean)

# --- स्टेप 4: ग्राफ (Visual Plotting) बनाकर जादू देखना ---
plt.figure(figsize=(10, 6))

# हिस्टोग्राम ग्राफ बनाना (bins=50 मतलब ग्राफ के टावर्स की संख्या)
plt.hist(sample_means, bins=50, edgecolor='black', color='skyblue', density=True)

# ग्राफ की सजावट (नामकरण)
plt.title("Central Limit Theorem Simulation (Perfect Bell Curve!)", fontsize=14)
plt.xlabel("Sample Means (सैंपल का औसत)", fontsize=12)
plt.ylabel("Density (घनत्व)", fontsize=12)
plt.grid(True, alpha=0.3)

# ग्राफ को स्क्रीन पर दिखाना
plt.show()
