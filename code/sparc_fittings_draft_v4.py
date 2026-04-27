# code/sparc_fittings_draft_v4.py
# ЧЕРНОВИК v4 — 27 апреля 2026
# Максимально простой и честный вариант для dOPH + SPARC
# Ничего не выдумываем, только то, что реально работает

import numpy as np
import pandas as pd
import zipfile
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

print("="*60)
print("dOPH SPARC FITTINGS — ЧЕРНОВИК v4")
print("="*60)

# ====================== КОНСТАНТЫ dOPH ======================
P_THEORY = np.sqrt(8.0 / 3.0)
print(f"dOPH: Theoretical P = {P_THEORY:.5f} ≈ 1.63299\n")

# ====================== ЗАГРУЗКА ЗИПА ======================
def load_sparc_from_zip():
    zip_path = Path("data/sparc/Rotmod_LTG.zip")
    
    if not zip_path.exists():
        print(f"❌ Зип не найден по пути: {zip_path}")
        print("   Положи Rotmod_LTG.zip в папку data/sparc/")
        return []
    
    print(f"✅ Зип найден: {zip_path}")
    
    extract_dir = Path("data/sparc/Rotmod_LTG")
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    # Распаковываем, если ещё не распаковано
    if len(list(extract_dir.glob("*.dat"))) < 50:
        print("Распаковываем Rotmod_LTG.zip ...")
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(extract_dir)
        print(f"Распаковано файлов .dat: {len(list(extract_dir.glob('*.dat')))}")
    else:
        print("Папка с .dat файлами уже существует.")
    
    # Загружаем галактики
    galaxies = []
    for file in extract_dir.glob("*.dat"):
        gal_name = file.stem.upper()
        try:
            df = pd.read_csv(file, delim_whitespace=True, comment='#', header=None)
            if len(df.columns) >= 6:
                df.columns = ['R', 'Vobs', 'Verr', 'Vgas', 'Vdisk', 'Vbul'] + list(df.columns[6:])
            
            df = df[(df['R'] > 0) & (df['Vobs'] > 0)].copy()
            if len(df) >= 8:
                galaxies.append((gal_name, df))
        except:
            pass
    
    print(f"✅ Успешно загружено галактик: {len(galaxies)} из ~175\n")
    return galaxies

# ====================== ЗАГЛУШКА МОДЕЛИ (пока настоящая модель не подключается) ======================
def doph_velocity_model(R, params, galaxy_data=None):
    """Простая заглушка. Заменить на импорт из doph_model_improved.py позже"""
    if galaxy_data is not None and 'Vdisk' in galaxy_data.columns:
        Y_star = params[0] if len(params) > 0 else 1.0
        Vbar2 = Y_star * galaxy_data['Vdisk']**2 + galaxy_data.get('Vgas', 0)**2
        return np.sqrt(Vbar2)
    else:
        return np.full_like(R, 180.0)  # заглушка

# ====================== ПРОСТОЙ ФИТИНГ ======================
def fit_single_galaxy(gal_name, df):
    R = df['R'].values
    Vobs = df['Vobs'].values
    Verr = df.get('Verr', pd.Series(np.ones_like(Vobs)*8.0)).values
    
    def model_wrapper(R, Y_star=1.0):
        return doph_velocity_model(R, [Y_star], galaxy_data=df)
    
    try:
        from scipy.optimize import curve_fit
        popt, _ = curve_fit(model_wrapper, R, Vobs, p0=[0.8], sigma=Verr, bounds=(0.1, 5.0))
        chi2_red = np.sum(((Vobs - model_wrapper(R, *popt)) / Verr)**2) / (len(R) - 1)
        
        print(f"✓ {gal_name:12}  χ²_red = {chi2_red:.3f}   Y_star = {popt[0]:.3f}")
        return chi2_red
    except Exception as e:
        print(f"✗ {gal_name:12}  ошибка фита")
        return None

# ====================== MAIN ======================
if __name__ == "__main__":
    galaxies = load_sparc_from_zip()
    
    if not galaxies:
        print("Не удалось загрузить данные. Проверь наличие зипа.")
    else:
        print("Начинаем фитинг (первые 30 галактик для теста)...\n")
        results = []
        
        for gal_name, df in galaxies[:30]:   # первые 30, чтобы не висело долго
            chi2 = fit_single_galaxy(gal_name, df)
            if chi2 is not None:
                results.append(chi2)
        
        if results:
            mean_chi2 = np.mean(results)
            print("\n" + "="*50)
            print(f"ИТОГ по первым 30 галактикам:")
            print(f"Средний reduced χ² = {mean_chi2:.3f}")
            print(f"Минимум χ
²     = {np.min(results):.3f}")
            print("="*50)
            
            # Сохраняем результаты
            Path("results").mkdir(exist_ok=True)
            pd.DataFrame({'red_chi2': results}).to_csv("results/sparc_doph_v4_results.csv", index=False)
            print("Результаты сохранены в results/sparc_doph_v4_results.csv")
