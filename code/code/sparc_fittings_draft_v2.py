# code/sparc_fittings_draft_v2.py
# ЧЕРНОВИК v2 — 27 апреля 2026
# Только для доработки sparc_fittings. НИЧЕГО НЕ УДАЛЯЕМ ИЗ РЕПО.

import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# Импортируем готовую модель из главного файла (он уже в репо)
try:
    from doph_model_improved import doph_velocity_model, P_THEORY
    print(f"dOPH: Загружена модель improved с P = {P_THEORY:.5f}")
except ImportError:
    print("Внимание: doph_model_improved.py не найден рядом. Проверь путь.")
    # Заглушка, чтобы код не падал
    P_THEORY = np.sqrt(8.0 / 3.0)
    def doph_velocity_model(R, params, galaxy_data=None):
        return np.zeros_like(R) + 150.0  # временная заглушка

# ====================== ЗАГРУЗКА SPARC (упрощённая, без зипов пока) ======================
def load_sparc_data_dummy(num_galaxies=5):
    """Пока синтетические данные, чтобы можно было тестировать на телефоне/Colab.
    Позже заменим на реальные SPARC."""
    print(f"Генерируем {num_galaxies} синтетических галактик для черновика...")
    galaxies = []
    for i in range(num_galaxies):
        R = np.linspace(0.5, 35, 60)
        Vobs = 180 * (1 - np.exp(-R / 5)) + np.random.normal(0, 8, len(R))
        Verr = np.ones_like(R) * 6.0
        df = pd.DataFrame({'R': R, 'Vobs': Vobs, 'Verr': Verr})
        galaxies.append((f"GAL{i+1:03d}", df))
    return galaxies

# ====================== ФИТИНГ ОДНОЙ ГАЛАКТИКИ ======================
def fit_single_galaxy(gal_name, df):
    R = df['R'].values
    Vobs = df['Vobs'].values
    Verr = df['Verr'].values
    
    def model_wrapper(R, *params):
        # params[0] — например, Υ_star или другой свободный параметр
        return doph_velocity_model(R, params, galaxy_data=df)
    
    try:
        from scipy.optimize import curve_fit
        popt, pcov = curve_fit(model_wrapper, R, Vobs, p0=[0.7],
                               sigma=Verr, absolute_sigma=True, bounds=(0, 5))
        chi2_red = np.sum(((Vobs - model_wrapper(R, *popt)) / Verr)**2) / (len(R) - len(popt))
        print(f"✓ {gal_name} → χ²_red = {chi2_red:.3f} | params = {popt}")
        return gal_name, popt, chi2_red, True
    except Exception as e:
        print(f"✗ {gal_name} → ошибка: {e}")
        return gal_name, None, np.inf, False

# ====================== MAIN (ЧЕРНОВИК) ======================
if __name__ == "__main__":
    print("=== dOPH SPARC FITTINGS — ЧЕРНОВИК v2 ===\n")
    
    galaxies = load_sparc_data_dummy(num_galaxies=10)  # сейчас синтетика, потом заменим
    
    results = []
    for gal_name, df in galaxies:
        name, popt, red_chi2, ok = fit_single_galaxy(gal_name, df)
        if ok:
            results.append({'galaxy': name, 'red_chi2': red_chi2, 'P': P_THEORY})
    
    if results:
        df_res = pd.DataFrame(results)
        print("\nИтог черновика:")
        print(df_res.describe())
        # Сохраняем только в results/ — ничего не трогаем
        Path("results").mkdir(exist_ok=True)
        df_res.to_csv("results/sparc_doph_draft_v2.csv", index=False)
        print("Результаты сохранены в results/sparc_doph_draft_v2.csv")
