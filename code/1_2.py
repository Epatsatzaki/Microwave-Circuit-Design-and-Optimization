import numpy as np
import matplotlib.pyplot as plt

# --- Παράμετροι Σχεδίασης ---
f0 = 1e9                         # Συχνότητα σχεδιασμού 1 GHz
f = np.linspace(0, 2e9, 500) # Εύρος συχνοτήτων από 0.1 έως 4 GHz
Z0_sys = 50                      # Χαρακτηριστική αντίσταση συστήματος (50 Ohm)

# Τιμές Αντιστάσεων από το Layout (όπως τις βάλαμε στο κυκλωματικό)
Z_stubs = [129.3, 24.0, 19.7, 24.0, 129.3] # Shunt Open Stubs
Z_lines = [81.5, 80.0, 80.0, 81.5]         # Series Lines (Κορμός)
EL = 45                                    # Ηλεκτρικό μήκος lambda/8 = 45 μοίρες στο 1 GHz

def get_Zin_line(ZL, Z0, f, f0, el_deg):
    """Υπολογισμός σύνθετης αντίστασης εισόδου για τμήμα γραμμής σειράς"""
    theta = np.radians(el_deg) * (f / f0)
    return Z0 * (ZL + 1j * Z0 * np.tan(theta)) / (Z0 + 1j * ZL * np.tan(theta))

def get_Y_stub(Z0, f, f0, el_deg):
    """Υπολογισμός αγωγιμότητας για ανοιχτοκυκλωμένο κλαδωτή (shunt open stub)"""
    theta = np.radians(el_deg) * (f / f0)
    return 1j * (1/Z0) * np.tan(theta)

# --- Υπολογισμός (Αναδρομικά από το Φορτίο προς την Είσοδο) ---
ZL = Z0_sys + 0j # Ξεκινάμε με το φορτίο 50 Ohm στη δεξιά πλευρά

# 1. Πρόσθεση του τελευταίου (5ου) stub παράλληλα στο φορτίο
Yin = (1/ZL) + get_Y_stub(Z_stubs[4], f, f0, EL)
Zin = 1/Yin

# 2. Loop για τα υπόλοιπα 4 τμήματα (Κορμός + Stub)
for i in range(3, -1, -1):
    # Μετασχηματισμός μέσω της γραμμής του κορμού (σειρά)
    Zin = get_Zin_line(Zin, Z_lines[i], f, f0, EL)
    # Πρόσθεση του αντίστοιχου stub (παράλληλα)
    Yin = (1/Zin) + get_Y_stub(Z_stubs[i], f, f0, EL)
    Zin = 1/Yin

# --- Υπολογισμός S11 σε dB ---
gamma = (Zin - Z0_sys) / (Zin + Z0_sys)
s11_db = 20 * np.log10(np.abs(gamma) + 1e-10) # Προσθήκη μικρής τιμής για αποφυγή log(0)

# --- Σχεδίαση Γραφήματος ---
plt.figure(figsize=(10, 6))
plt.plot(f/1e9, s11_db, color='blue', linewidth=2, label='|S11| (dB)')
plt.axvline(x=1.0, color='red', linestyle='--', label='f0 = 1 GHz (Cutoff approx.)')
plt.title('Απόκριση Χαμηλοπερατού Φίλτρου (Άσκηση 1.2β)')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Return Loss |S11| (dB)')
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.ylim(-50, 5)
plt.legend()
plt.show()
