import numpy as np
import sys
import time

print("🏛️ IIT-B QUANT APPRENTICESHIP: DAY 1 RUN TIME")
print("==============================================")

# 1. Initialize a native Python List vs a C-Contiguous NumPy float64 array
size = 1_000_000
py_list = list(range(size))
np_arr = np.array(py_list, dtype=np.float64) # Your first float64 array initialization

# 2. Performance Test: Python List Loop Speed
start_py = time.time()
py_list_result = [x + 1.0 for x in py_list]
end_py = time.time()
py_time = (end_py - start_py) * 1000

# 3. Performance Test: NumPy C-Contiguous Raw Hardware Clock Vectorization
start_np = time.time()
np_arr_result = np_arr + 1.0
end_np = time.time()
np_time = (end_np - start_np) * 1000

# 4. Display Real-World Memory Layout Mapping
print(f"🔹 NumPy Array Datatype: {np_arr.dtype}")
print(f"🔹 Is the matrix C-Contiguous in RAM? {np_arr.flags['C_CONTIGUOUS']}")
print(f"🔹 Python List Execution Speed: {py_time:.2f} ms")
print(f"🔹 NumPy Array Hardware Speed: {np_time:.2f} ms")
print(f"🚀 Speed Multiplier (NumPy Advantage): {py_time / np_time:.1f}x Faster")
print("==============================================")
print("✅ DAY 1 SPECIFICATION 100% COMPLETE.")
