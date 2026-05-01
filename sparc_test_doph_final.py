import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore")

from doph_model_improved import ImprovedDOPHModel

print("="*80)
print("dOPH SPARC Test — Improved Version with Fixed P = √(8/3)")
print("="*80)

model = ImprovedDOPHModel(strict_decoupling=True)
P = model.P
print(f"Используется фиксированное P = {P:.5f}\n")

def load_galaxies(folder="data/sparc/code"):
    path = Path(folder)
    if not path.exists():
        print(f"❌ Папка {folder} не найдена!")
        return []
    
    galaxies = []
    for file in path.glob("*.dat"):
        name = file.stem.replace("_rotmod", "").upper()
        try:
            df = pd.read_csv(file, delim_whitespace=True, comment='#', header=None, skiprows=1)
            if len(df.columns) >= 6:
                df.columns = ['R', 'Vobs', 'Verr', 'Vgas', 'Vdisk', 'Vbul'] + list(df.columns[6:])
            df = df[(df['R'] > 0) & (df['Vobs'] > 0)].copy()
            if len(df) >= 8:
                galaxies.append((name, df))
        except:
            pass
    print(f"✅ Загружено галактик: {len(galaxies)}\n")
    return galaxies


def model_func(R, Y_star, df):
    Vdisk2 = Y_star * df['Vdisk'].values**2
    Vgas2  = df['Vgas'].values**2
    Vbul2  = df.get('Vbul', pd.Series(0.0)).values**2
    V_baryon2 = Vdisk2 + Vgas2 + Vbul2
    
    R_max = np.max(R)
    V_doph2 = V_baryon2 * (P**2 - 1.0) * np.log(1 + 12 * (R / R_max))
    
    return np.sqrt(V_baryon2 + np.maximum(V_doph2, 0))


def fit_galaxy(name, df):
    R = df['R'].values
    Vobs = df['Vobs'].values
    Verr = df.get('Verr', pd.Series(np.ones_like(Vobs)*5.0)).values

    try:
        popt, _ = curve_fit(lambda r, ys: model_func(r, ys, df), 
                           R, Vobs, p0=[0.8], sigma=Verr, bounds=(0.2, 3.0))
        
        V_theo = model_func(R, popt[0], df)
        chi2_red = np.sum(((Vobs - V_theo) / Verr)**2) / (len(R) - 1)
        
        print(f"✓ {name:12}  χ²_red = {chi2_red:.3f}   Y_star = {popt[0]:.3f}")
        return chi2_red
    except:
        print(f"✗ {name:12}  ошибка фита")
        return None


# ====================== ЗАПУСК ======================
if __name__ == "__main__":
    galaxies = load_galaxies(folder="data/sparc/code")   # исправленный путь
    
    if not galaxies:
        print("Данные не найдены.")
    else:
        results = []
        print("Запуск фиттинга (первые 50 галактик)...\n")
        
        for name, df in galaxies[:50]:
            chi2 = fit_galaxy(name, df)
            if chi2 is not None:
                results.append(chi2)
        
        if results:
            print("\n" + "="*70)
            print(f"ИТОГО по {len(results)} галактикам:")
            print(f"Средний reduced χ²   = {np.mean(results):.3f}")
            print(f"Медианный reduced χ² = {np.median(results):.3f}")
            print(f"Лучший χ²            = {np.min(results):.3f}")
            print("="*70)
