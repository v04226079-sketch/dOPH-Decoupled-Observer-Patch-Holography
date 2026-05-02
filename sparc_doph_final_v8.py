import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

from doph_model_improved import ImprovedDOPHModel

print("="*90)
print("dOPH SPARC — ФИНАЛЬНАЯ УСИЛЕННАЯ v8 (Y_star=1.0 фиксировано)")
print("="*90)

model = ImprovedDOPHModel(strict_decoupling=True)
P = model.P
print(f"Фиксированное P = {P:.5f}\n")

def load_galaxy(file_path):
    name = file_path.stem.replace("_rotmod", "").upper()
    df = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None, skiprows=1)
    if len(df.columns) >= 6:
        df.columns = ['R', 'Vobs', 'Verr', 'Vgas', 'Vdisk', 'Vbul'] + list(df.columns[6:])
    df = df[(df['R'] > 0) & (df['Vobs'] > 0)].copy()
    return name, df

def doph_velocity_final(R, df):
    Vdisk2 = df['Vdisk'].values**2
    Vgas2  = df['Vgas'].values**2
    Vbul2  = df.get('Vbul', pd.Series(0.0)).values**2
    V_baryon2 = Vdisk2 + Vgas2 + Vbul2
    
    R_max_kpc = np.max(R)
    R_Mpc = R_max_kpc / 1000.0
    M_proxy = np.sum(V_baryon2 * R) / 1e5
    
    scale_factor = 1.0 + 2.8 * np.log10(1 + R_Mpc) * np.log10(1 + M_proxy / 1e8)
    effective_P = P * scale_factor ** 1.05
    
    V_doph2 = V_baryon2 * (effective_P**2 - 1.0) * np.log(1 + 25 * (R / R_max_kpc))
    
    V_theo = np.sqrt(V_baryon2 + np.maximum(V_doph2, 0))
    return V_theo

def calculate_chi2(name, df):
    R = df['R'].values
    Vobs = df['Vobs'].values
    Verr = df.get('Verr', pd.Series(np.full(len(R), 8.0))).values
    
    V_theo = doph_velocity_final(R, df)
    chi2_red = np.sum(((Vobs - V_theo) / Verr)**2) / (len(R) - 1)
    
    print(f"{name:12}   χ²_red = {chi2_red:.3f}")
    return chi2_red

if __name__ == "__main__":
    data_dir = Path("data/sparc/code")
    files = list(data_dir.glob("*.dat"))
    print(f"Найдено файлов: {len(files)}\n")
    
    results = []
    for file in files:
        name, df = load_galaxy(file)
        if len(df) < 8: continue
        chi2_red = calculate_chi2(name, df)
        results.append(chi2_red)
    
    results = np.array(results)
    print("\n" + "="*90)
    print("ФИНАЛЬНЫЙ ИТОГ v8")
    print("="*90)
    print(f"Галактик обработано: {len(results)}")
    print(f"Средний χ²_red     : {np.mean(results):.3f}")
    print(f"Медианный χ²_red   : {np.median(results):.3f}")
    print(f"Min χ²_red         : {np.min(results):.3f}")
    print("="*90)
