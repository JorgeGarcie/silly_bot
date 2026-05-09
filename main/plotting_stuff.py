import re
import matplotlib.pyplot as plt

sk = r"""31.25 Hz: 1.11
62.50 Hz: 30.88
93.75 Hz: 17.22
125.00 Hz: 1.78
156.25 Hz: 4.59
187.50 Hz: 3.31
218.75 Hz: 1.40
250.00 Hz: 4.62
281.25 Hz: 3.10
312.50 Hz: 19.43
343.75 Hz: 43.62
375.00 Hz: 323.45
406.25 Hz: 275.02
437.50 Hz: 26.48
468.75 Hz: 19.61
500.00 Hz: 19.38
531.25 Hz: 1.09
562.50 Hz: 3.72
593.75 Hz: 5.79
625.00 Hz: 1.29
656.25 Hz: 4.04
687.50 Hz: 4.27
718.75 Hz: 19.75
750.00 Hz: 113.59
781.25 Hz: 157.51
812.50 Hz: 48.53
843.75 Hz: 130.18
875.00 Hz: 174.61
906.25 Hz: 41.34
937.50 Hz: 10.91
968.75 Hz: 5.99
1000.00 Hz: 2.81
1031.25 Hz: 2.56
1062.50 Hz: 4.51
1093.75 Hz: 2.99
1125.00 Hz: 12.04
1156.25 Hz: 29.54
1187.50 Hz: 16.47
1218.75 Hz: 6.12
1250.00 Hz: 38.37
1281.25 Hz: 48.11
1312.50 Hz: 13.97
1343.75 Hz: 3.38
1375.00 Hz: 4.07
1406.25 Hz: 4.51
1437.50 Hz: 5.30
1468.75 Hz: 4.21
1500.00 Hz: 12.81
1531.25 Hz: 92.32
1562.50 Hz: 94.75
1593.75 Hz: 13.69
1625.00 Hz: 47.01
1656.25 Hz: 129.36
1687.50 Hz: 67.14
1718.75 Hz: 4.51
1750.00 Hz: 2.11
1781.25 Hz: 2.50
1812.50 Hz: 1.52
1843.75 Hz: 0.88
1875.00 Hz: 4.90
1906.25 Hz: 71.39
1937.50 Hz: 141.58
1968.75 Hz: 60.28"""

# Extract frequency and magnitude
matches = re.findall(r"([-+]?\d*\.?\d+)\s*Hz:\s*([-+]?\d*\.?\d+)", sk)

frequencies = [float(f) for f, m in matches]
magnitudes = [float(m) for f, m in matches]

# Plot
plt.figure(figsize=(12, 6))
plt.plot(frequencies, magnitudes, marker='o')

plt.title("Magnitude vs Frequency")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)

plt.tight_layout()
plt.show() 
