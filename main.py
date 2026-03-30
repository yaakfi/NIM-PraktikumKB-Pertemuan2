import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Variabel Input & Output
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kecepatan_kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan_kipas')

# 2. Himpunan Fuzzy
suhu['dingin'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['normal'] = fuzz.trimf(suhu.universe, [15, 22.5, 30])
suhu['panas'] = fuzz.trimf(suhu.universe, [25, 40, 40])

kelembapan['kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 40])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['basah'] = fuzz.trimf(kelembapan.universe, [60, 100, 100])

kecepatan_kipas['lambat'] = fuzz.trimf(kecepatan_kipas.universe, [0, 0, 40])
kecepatan_kipas['sedang'] = fuzz.trimf(kecepatan_kipas.universe, [30, 50, 70])
kecepatan_kipas['cepat'] = fuzz.trimf(kecepatan_kipas.universe, [60, 100, 100])

# 3. Aturan Fuzzy
rule1 = ctrl.Rule(suhu['dingin'] & kelembapan['basah'], kecepatan_kipas['lambat'])
rule2 = ctrl.Rule(suhu['dingin'] & kelembapan['kering'], kecepatan_kipas['lambat'])
rule3 = ctrl.Rule(suhu['normal'] & kelembapan['sedang'], kecepatan_kipas['sedang'])
rule4 = ctrl.Rule(suhu['panas'] & kelembapan['sedang'], kecepatan_kipas['cepat'])
rule5 = ctrl.Rule(suhu['panas'] | kelembapan['kering'], kecepatan_kipas['cepat'])

# 4. Sistem Kontrol & Simulasi
sistem_kontrol = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
simulasi_kipas = ctrl.ControlSystemSimulation(sistem_kontrol)

# 5. Menguji Sistem
suhu_input = 32
kelembapan_input = 45

simulasi_kipas.input['suhu'] = suhu_input
simulasi_kipas.input['kelembapan'] = kelembapan_input
simulasi_kipas.compute()

# 6. Menampilkan Hasil
print("=" * 40)
print("  SISTEM LOGIKA FUZZY - KIPAS ANGIN  ")
print("=" * 40)
print(f"| Input Suhu       : {suhu_input:>5.1f} °C       |")
print(f"| Input Kelembapan : {kelembapan_input:>5.1f} %        |")
print("-" * 40)
if 'kecepatan_kipas' in simulasi_kipas.output:
    output_val = simulasi_kipas.output['kecepatan_kipas']
    print(f"| Output Kecepatan : {output_val:>5.2f}          |")
else:
    print(f"| Output Kecepatan : (Tidak terdefinisi) |")
print("=" * 40)

# 7. Menampilkan Grafik Fuzzy
import matplotlib.pyplot as plt
suhu.view(sim=simulasi_kipas)
kelembapan.view(sim=simulasi_kipas)
kecepatan_kipas.view(sim=simulasi_kipas)
plt.show()
