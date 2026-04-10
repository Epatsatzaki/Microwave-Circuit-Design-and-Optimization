# Microwave-Circuit-Design-and-Optimization
A comprehensive study of microwave circuits featuring transmission line matching, MATLAB-based filter optimization, and 180° hybrid ring coupler analysis.

## 📌 Project Overview
This repository contains a comprehensive analysis and computational design of high-frequency microwave circuits. The project bridges theoretical Smith Chart calculations with algorithmic optimization to design and analyze transmission lines, matching networks, and microstrip filters. 

## 🛠️ Tools & Technologies
* **Languages:** MATLAB, Python
* **Algorithms:** Non-linear optimization (`fmincon`), Gradient-based solvers
* **Concepts:** Transmission Line Theory, Impedance Matching, Low-Pass Filter Design, Rat-Race Couplers (180° Hybrid Ring)
* **Simulation:** Online Smith Chart, Falstad Circuit Simulator

## 🚀 Key Modules & Capabilities

### 1. Frequency-Dependent Transmission Line Matching
* Calculated complex input impedances using normalized Smith Chart techniques.
* Designed open/short stubs for optimal impedance matching to minimize signal reflection ($S_{11}$).
* Visualized reflection coefficients (Magnitude and dB) across a 0-2 GHz frequency band using automated scripting.

### 2. Microstrip Low-Pass Filter Optimization
* Analyzed a multi-stub microstrip filter using cascaded ABCD transmission matrices.
* Implemented a custom `Fitness Function` in MATLAB to rigorously optimize line characteristic impedances ($Z_0$).
* Minimized passband reflection while strictly enforcing stopband attenuation up to the 3rd harmonic ($3 \times f_c$), avoiding spurious resonances and "stopband leakage."

### 3. Non-Tree Structures: Rat-Race Coupler Analysis
* Modeled a 4-port Hybrid Ring Coupler using nodal analysis and Kirchhoff's laws.
* Solved the resulting $8 \times 8$ matrix system $Ax = b$ across 201 frequencies (2.5 GHz - 7.5 GHz).
* Verified 3dB power splitting, 180-degree phase shifts, and port isolation.

### 4. Microwave Amplifier Conjugate Matching
* Designed matching networks to maximize power transfer between two transistor stages.
* Calculated mismatch factor penalties due to frequency shifts (e.g., from 2.5 GHz to 3 GHz).

## 📂 Repository Structure
* `/scripts/` - MATLAB and Python source code for $$S_{11}$$ plotting and `fmincon` filter optimization.
* `/docs/` - Full technical report detailing theoretical derivations, Smith Chart movements, and mathematical proofs.
* `/assets/` - High-resolution plots of filter responses and optimization iterations.
