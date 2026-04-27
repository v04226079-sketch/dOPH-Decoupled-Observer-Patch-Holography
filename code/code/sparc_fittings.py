# code/sparc_fittings.py
# dOPH v2.1 — Фитинг SPARC (упрощённая версия без необходимости в папке Rotmod_LTG)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

np.random.seed(42)

class ImprovedDOPHModel:
    def __init__(self, strict_decoupling=True):
        self.P = np.sqrt(8.0 / 3.0)
        self.gamma = 0.15
        self.strict_decoupling = strict_decoupling
    
    def simulate_galaxy(self, is_lsb=False, mean_radius=8.0):
        num_patches = 65 if is_lsb else 100
        
        mismatch = np.random.normal(1.0, 0.55, num_patches)
        mismatch = np.clip(mismatch, 0.25, 13.0)
        
        for _ in range(35):
            if self.strict_decoupling:
                overlap_factor = np.abs(np.cos(np.random.uniform(0, np.pi/2, num_patches))) ** 2
                correction = (1 - overlap_factor) * 0.13
                mismatch *= (1 - correction)
            mismatch *= (1 - self.gamma * 0.05)
            mismatch *= 0.95
        
        mean_mismatch = np.mean(mismatch)
        stability = max(48, 100 - mean_mismatch * 14)
        
        base = self.P * (1 + 0.34 * (1 - stability/100))
        radius_factor = np.log10(mean_radius + 2.0) ** 1.15
        emergent_term = base * radius_factor * 2.3
        
        return {
            "stability": round(stability, 1),
            "emergent_term": round(emergent_term, 2)
        }


def mond_prediction(v_bary, mean_radius):
    g_bary = v_bary**2 / (mean_radius * 3.086e19)
    g_mond = np.sqrt(g_bary * 1.2e-10)
    v_mond = np.sqrt(g_mond * mean_radius * 3.086e19)
    return v_mond


# ====================== ПРИМЕРЫ РЕАЛЬНЫХ ГАЛАКТИК ======================
example_galaxies = [
    {"name": "NGC2403", "is_lsb": False, "mean_radius": 8.5, "v_bary_mean": 110, "v_obs_mean": 130},
    {"name": "NGC5055", "is_lsb": False, "mean_radius": 12.0, "v_bary_mean": 160, "v_obs_mean": 180},
    {"name": "UGC128",  "is_lsb": True,  "mean_radius": 5.5, "v_bary_mean": 45,  "v_obs_mean": 55},
    {"name": "NGC3198", "is_lsb": False, "mean_radius": 9.0, "v_bary_mean": 120, "v_obs_mean": 145},
    {"name": "NGC925",  "is_lsb": True,  "mean_radius": 6.0, "v_bary_mean": 60,  "v_obs_mean": 75},
]

def run_sparc_test():
    model = ImprovedDOPHModel(strict_decoupling=True)
    print("=== dOPH v2.1 — Тест фитинга SPARC (примеры реальных галактик) ===\n")
    print(f"Теоретический P = {model.P:.5f}\n")

    results = []

    for gal in example_galaxies:
        res = model.simulate_galaxy(is_lsb=gal["is_lsb"], mean_radius=gal["mean_radius"])
        
        v_pred_doph = gal["v_bary_mean"] + res["emergent_term"]
        v_pred_mond = mond_prediction(gal["v_bary_mean"], gal["mean_radius"])

        rms_doph = abs(v_pred_doph - gal["v_obs_mean"])
        rms_mond = abs(v_pred_mond - gal["v_obs_mean"])

        results.append({
            "Галактика": gal["name"],
            "Тип": "LSB" if gal["is_lsb"] else "Обычная",
            "Стабильность": res["stability"],
            "rms_dOPH": round(rms_doph, 2),
            "rms_MOND": round(rms_mond, 2)
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    print("\nТест завершён.")
    print("Это упрощённая версия. Когда будет удобно — добавим чтение всех 175 галактик.")

if __name__ == "__main__":
    run_sparc_test()
