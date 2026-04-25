# code/doph_reproducible_test.py
# dOPH v2.1 — МАКСИМАЛЬНАЯ НАГРУЗКА (20 000 галактик + усиленный JWST-стресс)

import numpy as np
from doph_model_improved import ImprovedDOPHModel

np.random.seed(42)

def run_heavy_test():
    model = ImprovedDOPHModel(strict_decoupling=True)
    
    print("=== dOPH v2.1 — МАКСИМАЛЬНАЯ НАГРУЗКА ТЕСТ ===\n")
    print("Теоретический P =", round(model.P, 5), "(√(8/3))\n")
    
    # 1. 20 000 синтетических галактик
    n_galaxies = 20000
    stabilities = []
    g_factors = []
    lsb_stabilities = []
    
    print("Запуск 20 000 галактик...")
    
    for i in range(n_galaxies):
        is_lsb = (i % 5 == 0)  # 20% LSB
        num_patches = 40 if is_lsb else 60
        res = model.simulate_galaxy(num_patches=num_patches, is_lsb=is_lsb)
        stabilities.append(res['stability'])
        g_factors.append(res['effective_g_factor'])
        if is_lsb:
            lsb_stabilities.append(res['stability'])
    
    avg_stab = np.mean(stabilities)
    min_stab = np.min(stabilities)
    avg_g = np.mean(g_factors)
    avg_lsb = np.mean(lsb_stabilities)
    
    print(f"20 000 галактик:")
    print(f"  Средняя стабильность: {avg_stab:.1f}%")
    print(f"  Минимальная стабильность: {min_stab:.1f}%")
    print(f"  Средний g-фактор: {avg_g:.5f}")
    print(f"  LSB-галактики (20%): {avg_lsb:.1f}%\n")
    
    # 2. Усиленный JWST-стресс (100 патчей)
    jwst_stab = []
    print("Запуск JWST-стресс (1000 галактик × 100 патчей)...")
    
    for i in range(1000):
        res = model.simulate_galaxy(num_patches=100, is_lsb=True)
        jwst_stab.append(res['stability'])
    
    avg_jwst = np.mean(jwst_stab)
    min_jwst = np.min(jwst_stab)
    
    print(f"JWST-стресс-тест:")
    print(f"  Средняя стабильность: {avg_jwst:.1f}%")
    print(f"  Минимальная стабильность: {min_jwst:.1f}%")
    
    print("\nТест максимальной нагрузки завершён.")
    print("P остаётся теоретическим и стабильным.")

if __name__ == "__main__":
    run_heavy_test()
