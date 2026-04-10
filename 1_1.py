import numpy as np
import matplotlib.pyplot as plt

# --- Project Parameters ---
f0 = 1e9                         # Design frequency 1 GHz 
f = np.linspace(1e6, 2*f0, 201)  # 201 frequency points from 0 to 2*f0 [cite: 172]
Z0 = 50                          # Characteristic impedance 50 Ohms 
R_L = 100                        # Load resistance 100 Ohms 
C_load = 2e-12                   # Series load capacitor 2 pF 
C_p = 2.7e-12                    # Shunt capacitor 2.7 pF 

# --- Lengths based on your solution ---
l1_lam = 0.2                     # Fixed line segment 0.2 lambda [cite: 184]
l_match_min = 0.1                # Calculated l = 0.1 lambda 
ls_stub_min = 0.15               # Calculated ls = 0.15 lambda (Open Circuit) 

# --- Next possible lengths for part (d) ---
# Adding 0.5 lambda for the next matching point on the Smith Chart [cite: 174]
l_match_next = l_match_min + 0.5 # 0.6 lambda
ls_stub_next = ls_stub_min + 0.5 # 0.65 lambda

def calculate_gamma(l_match, ls_stub, f_arr):
    # 1. Load Impedance ZL(f)
    ZL = R_L - 1j / (2 * np.pi * f_arr * C_load)
    
    # 2. Transform through l1 = 0.2 lambda line
    # Beta*l formula provided in hint [cite: 186]
    theta1 = 2 * np.pi * l1_lam * (f_arr / f0)
    Z_A_right = Z0 * (ZL + 1j * Z0 * np.tan(theta1)) / (Z0 + 1j * ZL * np.tan(theta1))
    
    # 3. Add Shunt Capacitor at point A
    YA = (1 / Z_A_right) + 1j * 2 * np.pi * f_arr * C_p
    ZA = 1 / YA
    
    # 4. Transform through the matching line 'l'
    theta_m = 2 * np.pi * l_match * (f_arr / f0)
    Z_junc = Z0 * (ZA + 1j * Z0 * np.tan(theta_m)) / (Z0 + 1j * ZA * np.tan(theta_m))
    
    # 5. Add Shunt Open Circuit Stub 'ls'
    theta_s = 2 * np.pi * ls_stub * (f_arr / f0)
    Y_stub = 1j * (1 / Z0) * np.tan(theta_s)
    
    # 6. Final Input Admittance and Reflection Coefficient [cite: 189]
    Yin = (1 / Z_junc) + Y_stub
    Zin = 1 / Yin
    gamma = (Zin - Z0) / (Zin + Z0)
    return gamma

# Calculate gamma for both cases (c) and (d)
gamma_c = calculate_gamma(l_match_min, ls_stub_min, f)
gamma_d = calculate_gamma(l_match_next, ls_stub_next, f)

# Magnitude calculations
mag_c = np.abs(gamma_c)
mag_d = np.abs(gamma_d)

# Conversion to dB [cite: 238]
# Using a -60 dB floor for better readability [cite: 191]
db_c = np.maximum(20 * np.log10(mag_c + 1e-10), -60)
db_d = np.maximum(20 * np.log10(mag_d + 1e-10), -60)

# --- Plotting Question (c) ---
plt.figure(figsize=(10, 5))
plt.plot(f/1e9, mag_c, color='blue', linewidth=2)
plt.title('Question (c): Reflection Coefficient Magnitude (Linear)')
plt.xlabel('Frequency (GHz)')
plt.ylabel(r'$|\Gamma_{in}|$')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(f/1e9, db_c, color='red', linewidth=2)
plt.title('Question (c): Reflection Coefficient Magnitude (dB)')
plt.xlabel('Frequency (GHz)')
plt.ylabel(r'$|\Gamma_{in}|$ (dB)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# --- Plotting Question (d): Comparison ---
plt.figure(figsize=(10, 5))
plt.plot(f/1e9, mag_c, color='blue', label='Case (c): $l=0.1\lambda, l_s=0.15\lambda$')
plt.plot(f/1e9, mag_d, color='green', linestyle='--', label='Case (d): $l=0.6\lambda, l_s=0.65\lambda$')
plt.title('Bandwidth Comparison (Linear Scale)')
plt.xlabel('Frequency (GHz)')
plt.ylabel(r'$|\Gamma_{in}|$')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(f/1e9, db_c, color='red', label='Case (c): $l=0.1\lambda, l_s=0.15\lambda$')
plt.plot(f/1e9, db_d, color='magenta', linestyle='--', label='Case (d): $l=0.6\lambda, l_s=0.65\lambda$')
plt.title('Bandwidth Comparison (dB)')
plt.xlabel('Frequency (GHz)')
plt.ylabel(r'$|\Gamma_{in}|$ (dB)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()