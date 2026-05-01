import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore")

from doph_model_improved import ImprovedDOPHModel

print("="*70)
print("Тест SPARC с ImprovedDOPHModel (фиксированный P)")
print("="*70)

model = ImprovedDOPHModel(strict_decoupling=True)
print(f"Используется P = {model.P:.5f}\n")

def load_galaxies(folder="data/spark/code"):
    path = Path(folder)
    if not path.exists():
        print(f"Папка {folder} не найдена!")
        return []

    galaxies = []
    for file in path.glob("*.dat"):
        name = file.stem.upper()
        try:
            df = pd.read_csv(file, delim_whitespace=True, comment='#', header=None, skiprows=2)
            if len(df.columns) >= 6:
                df.columns = ['R', 'Vobs', 'Verr', 'Vgas', 'Vdisk', 'Vbul'] + list(df.columns[6:])
            df = df[(df['R'] > 0) & (df['Vobs'] > 0)].copy()
            if len(df) >= 8:
                galaxies.append((name, df))
        except:
            pass
    print(f"Загружено галактик: {len(galaxies)}\n")
    return galaxies

def fit_galaxy(name, df):
    R = df['R'].values
    Vobs = df['Vobs'].values
    Verr = df.get('Verr', pd.Series(np.ones_like(Vobs)*5)).values

    def model_func(R, Y_star):
        # Упрощённая обёртка (пока используем базовую логику)
        Vbar2 = Y_star * df['Vdisk']**2 + df['Vgas']**2
        # Здесь можно подключить более сложную логику из модели
        V_doph = np.sqrt(Vbar2) * 0.25 * model.P
        return np.sqrt(Vbar2 + V_doph**2)

    try:
        popt, _ = curve_fit(model_func, R, Vobs, p0=[0.7], sigma=Verr, bounds=(0.1, 5.0))
        chi2 = np.sum(((Vobs - model_func(R, *popt)) / Verr)**2) / (len(R) - 1)
        print(f"✓ {name:12}  χ²_red = {chi2:.3f}   Y_star = {popt[0]:.3f}")
        return chi2
    except Exception as e:
        print(f"✗ {name:12}  ошибка")
        return None

# ====================== ЗАПУСК ======================
if __name__ == "__main__":
    galaxies = load_galaxies()

    if galaxies:
        results = []
        for name, df in galaxies[:40]:   # сначала 40 галактик, чтобы не висело долго
            chi2 = fit_galaxy(name, df)
            if chi2 is not None:
                results.append(chi2)

        if results:
            print("\n" + "="*60)
            print(f"Средний reduced χ² по {len(results)} галактикам: {np.mean(results):.3f}")
            print(f"Минимум χ² = {np.min(results):.3f}")
            print("="*60)
