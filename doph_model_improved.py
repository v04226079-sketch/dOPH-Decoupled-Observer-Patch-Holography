# doph_model_improved.py
# dOPH v2.2 — с проверяемыми тестами и нулевыми контролями.
#
# Что честно:
#   - P = sqrt(8/3) задаётся как гипотеза, НЕ выводится в этом коде.
#   - "Decoupling" — феноменологический множитель, не оператор из 4-й аксиомы.
#   - "Stability" — доля патчей ниже порога. Может быть 0%.
#   - Модель — игрушечная. Тесты проверяют внутреннюю согласованность,
#     а не физическую правильность.

import numpy as np


MW_MASS = 8e10   # Msun
MW_RADIUS = 15.0 # kpc
MW_SIGMA = MW_MASS / MW_RADIUS**2


class ImprovedDOPHModel:
    def __init__(self, strict_decoupling=True, P=None, seed=42,
                 mismatch_threshold=0.5, decouple_steps=25):
        # P: если None — гипотеза sqrt(8/3). Явно задаётся, не выводится.
        self.P = float(P) if P is not None else float(np.sqrt(8.0 / 3.0))
        self.gamma = 0.15
        self.decoupling_strength = 0.8
        self.phase_consensus = 0.6
        self.strict_decoupling = strict_decoupling
        self.mismatch_threshold = mismatch_threshold
        self.decouple_steps = decouple_steps
        self.rng = np.random.default_rng(seed)

    # ---------- инициализация рассогласования ----------
    def initial_mismatch(self, baryonic_mass, radius, num_patches, is_lsb):
        """
        Начальное рассогласование патчей.
        Зависит от log10(sigma/sigma_MW), где sigma = M/R^2.
        LSB: тот же M, но больший R → меньшая sigma → меньше начальное
        рассогласование (в этой игрушечной модели).
        """
        sigma = baryonic_mass / (radius ** 2)
        ratio = max(sigma / MW_SIGMA, 1e-10)
        base = np.log10(ratio) + 1.0        # ~1.0 для Млечного Пути
        scatter = 0.3 * (1.8 if is_lsb else 1.0)
        raw = self.rng.normal(base, scatter, num_patches)
        return np.clip(raw, 0.01, 5.0)

    # ---------- декуплинг (детерминированный) ----------
    def decouple(self, mismatch):
        for _ in range(self.decouple_steps):
            if self.strict_decoupling:
                # Фиксированное перекрытие 0.95 → коррекция 0.006
                correction = (1.0 - 0.95) * 0.12
            else:
                correction = self.decoupling_strength * 0.08
            mismatch = mismatch * (1.0 - correction)
            mismatch = mismatch * (1.0 - self.gamma * 0.05)
            mismatch = mismatch * 0.96
        return mismatch

    # ---------- метрики ----------
    def _metrics(self, mismatch, baryonic_mass, radius, num_patches, is_lsb):
        mean_m = float(np.mean(mismatch))
        stability = float(np.mean(mismatch < self.mismatch_threshold) * 100.0)
        effective_g = self.P * (1.0 + 0.3 * (1.0 - stability / 100.0))
        return {
            "baryonic_mass": float(baryonic_mass),
            "radius": float(radius),
            "num_patches": int(num_patches),
            "is_lsb": bool(is_lsb),
            "mean_mismatch": round(mean_m, 4),
            "stability": round(stability, 1),
            "effective_g_factor": round(effective_g, 5),
            "P": round(self.P, 5),
        }

    # ---------- публичные симуляции ----------
    def simulate_galaxy(self, baryonic_mass=1e10, radius=10.0,
                        num_patches=50, is_lsb=False):
        mismatch = self.initial_mismatch(baryonic_mass, radius, num_patches, is_lsb)
        mismatch = self.decouple(mismatch)
        return self._metrics(mismatch, baryonic_mass, radius, num_patches, is_lsb)

    def simulate_galaxy_null(self, baryonic_mass=1e10, radius=10.0,
                             num_patches=50, is_lsb=False):
        """Нулевой контроль №1: те же входы, БЕЗ декуплина."""
        mismatch = self.initial_mismatch(baryonic_mass, radius, num_patches, is_lsb)
        return self._metrics(mismatch, baryonic_mass, radius, num_patches, is_lsb)

    def simulate_galaxy_random(self, num_patches=50):
        """Нулевой контроль №2: полностью случайные входы, без физики M/R."""
        mismatch = self.rng.uniform(0.01, 5.0, num_patches)
        return self._metrics(mismatch, 0.0, 0.0, num_patches, False)


if __name__ == "__main__":
    m = ImprovedDOPHModel()
    print(f"P = {m.P:.5f}  (гипотеза, не вывод)\n")
    for label, kw in [
        ("MW",   dict(baryonic_mass=8e10, radius=15.0, is_lsb=False)),
        ("LSB",  dict(baryonic_mass=2e9,  radius=8.0,  is_lsb=True)),
        ("Big",  dict(baryonic_mass=1e12, radius=30.0, is_lsb=False)),
    ]:
        r = m.simulate_galaxy(**kw)
        n = m.simulate_galaxy_null(**kw)
        print(f"{label}: model mm={r['mean_mismatch']:.4f}  null mm={n['mean_mismatch']:.4f}  "
              f"stab={r['stability']}%")
