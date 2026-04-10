import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
Z0 = 50.0              # Characteristic impedance of ports (Ohms)
Zc = np.sqrt(2) * Z0   # Characteristic impedance of the ring (Ohms)
Yc = 1.0 / Zc
f0 = 5e9               # Design frequency (5 GHz)

# Frequency range: 2.5 GHz to 7.5 GHz, 201 points
freq = np.linspace(2.5e9, 7.5e9, 201)

# --- Arrays to store results ---
S11_dB = np.zeros(len(freq))
P_out = np.zeros((3, len(freq)))
V_ang = np.zeros((3, len(freq)))

# --- Main Simulation Loop ---
for k, f in enumerate(freq):
    theta = (np.pi / 2) * (f / f0)
    
    # Coefficients without divisions (Absolute Singularity Avoidance)
    c1, s1 = np.cos(theta), np.sin(theta)
    c3, s3 = np.cos(3*theta), np.sin(3*theta)
    
    Zc_s1 = 1j * Zc * s1; Yc_s1 = 1j * Yc * s1
    Zc_s3 = 1j * Zc * s3; Yc_s3 = 1j * Yc * s3
    
    # --- System Construction (16x16) ---
    # Python uses 0-based indexing!
    A = np.zeros((16, 16), dtype=complex)
    b = np.zeros(16, dtype=complex)
    
    # Indices for readability
    iV1, iV2, iV3, iV4 = 0, 1, 2, 3
    iIin1, iIout2, iIout3, iIout4 = 4, 5, 6, 7
    iI12, iI21, iI23, iI32, iI34, iI43, iI41, iI14 = 8, 9, 10, 11, 12, 13, 14, 15
    
    # 1. Transmission Line Equations (ABCD based)
    # Branch 1-2
    A[0, iV1] = 1; A[0, iV2] = -c1; A[0, iI21] = Zc_s1
    A[1, iI12] = 1; A[1, iV2] = -Yc_s1; A[1, iI21] = c1
    
    # Branch 2-3
    A[2, iV2] = 1; A[2, iV3] = -c1; A[2, iI32] = Zc_s1
    A[3, iI23] = 1; A[3, iV3] = -Yc_s1; A[3, iI32] = c1
    
    # Branch 3-4
    A[4, iV3] = 1; A[4, iV4] = -c1; A[4, iI43] = Zc_s1
    A[5, iI34] = 1; A[5, iV4] = -Yc_s1; A[5, iI43] = c1
    
    # Branch 4-1
    A[6, iV4] = 1; A[6, iV1] = -c3; A[6, iI14] = Zc_s3
    A[7, iI41] = 1; A[7, iV1] = -Yc_s3; A[7, iI14] = c3
    
    # 2. KCL Equations at the 4 nodes
    A[8, iIin1] = 1; A[8, iI12] = -1; A[8, iI14] = -1
    A[9, iI21] = 1; A[9, iI23] = 1; A[9, iIout2] = 1
    A[10, iI32] = 1; A[10, iI34] = 1; A[10, iIout3] = 1
    A[11, iI43] = 1; A[11, iI41] = 1; A[11, iIout4] = 1
    
    # 3. Boundary Conditions (Source and Loads)
    A[12, iV1] = 1; b[12] = 1.0                     # V1 = 1V (Source)
    A[13, iV2] = 1; A[13, iIout2] = -Z0             # V2 = Iout2 * Z0
    A[14, iV3] = 1; A[14, iIout3] = -Z0             # V3 = Iout3 * Z0
    A[15, iV4] = 1; A[15, iIout4] = -Z0             # V4 = Iout4 * Z0
    
    # --- Solving the System ---
    x = np.linalg.solve(A, b)
    
    # --- Extracting Results ---
    V1 = x[iV1]
    Iin1 = x[iIin1]
    
    Zin = V1 / Iin1
    S11 = (Zin - Z0) / (Zin + Z0)
    
    # Calculate dB safely (avoiding log10(0) if perfectly matched)
    mag_S11 = np.abs(S11)
    if mag_S11 > 1e-15:
        S11_dB[k] = 20 * np.log10(mag_S11)
    else:
        S11_dB[k] = -300 # Effectively negative infinity
        
    V_ports = [x[iV2], x[iV3], x[iV4]]
    
    for p in range(3):
        V_p = V_ports[p]
        P_out[p, k] = 0.5 * (np.abs(V_p)**2) / Z0
        V_ang[p, k] = np.angle(V_p, deg=True)

# --- Plotting ---
plt.figure(figsize=(10, 8))

# Return Loss
plt.subplot(3, 1, 1)
plt.plot(freq / 1e9, S11_dB, linewidth=1.5)
plt.title('Return Loss |S11| (dB)')
plt.ylabel('dB')
plt.xlabel('Frequency (GHz)')
plt.grid(True)
plt.ylim([-70, 0])

# Output Power
plt.subplot(3, 1, 2)
plt.plot(freq / 1e9, P_out[0], label='Port 2', linewidth=1.5)
plt.plot(freq / 1e9, P_out[1], label='Port 3', linewidth=1.5)
plt.plot(freq / 1e9, P_out[2], label='Port 4', linewidth=1.5)
plt.title('Output Power (Watts)')
plt.ylabel('Power (W)')
plt.xlabel('Frequency (GHz)')
plt.legend(loc='best')
plt.grid(True)

# Phase
plt.subplot(3, 1, 3)
plt.plot(freq / 1e9, V_ang[0], label='Port 2', linewidth=1.5)
plt.plot(freq / 1e9, V_ang[1], label='Port 3', linewidth=1.5)
plt.plot(freq / 1e9, V_ang[2], label='Port 4', linewidth=1.5)
plt.title('Phase of Output Voltages')
plt.ylabel('Degrees')
plt.xlabel('Frequency (GHz)')
plt.legend(loc='best')
plt.grid(True)

plt.tight_layout()
plt.show()