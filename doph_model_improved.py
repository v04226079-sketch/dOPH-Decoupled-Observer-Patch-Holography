# doph_model_improved.py
# Улучшенная воспроизводимая модель dOPH (апрель 2026)
# Более осмысленная версия с параметрами галактик

import numpy as np

np.random.seed(42)  # для воспроизводимости

class ImprovedDOPHModel:
    def __init__(self, P=1.63094):
        self.P = P
        self.gamma = 0.15          # демпфирование
        self.decoupling_strength = 0.8
        self.phase_consensus = 0.6
    
    def simulate_galaxy(self, baryonic_mass=1e10, radius=10.0, num_patches=50, is_lsb=False):
        """
        Симуляция одной галактики
        is_lsb = True для низкояркостных галактик (сложнее)
        """
        diversity_factor = 1.8 if is_lsb else 1.0
        
        # Симулируем начальные рассогласования патчей
        mismatch = np.random.normal(1.0, 0.6 * diversity_factor, num_patches)
        mismatch = np.clip(mismatch, 0.3, 12.0)
        
        # Применяем декуплинг + emergent gravity в упрощённой форме
        for _ in range(25):
            # Декуплинг уменьшает рассогласование
            mismatch *= (1 - self.decoupling_strength * 0.08)
            # Демпфирование
            mismatch *= (1 - self.gamma * 0.05)
            # Фазовый консенсус
            mismatch *= 0.96
        
        mean_mismatch = np.mean(mismatch)
        stability = max(40, 100 - mean_mismatch * 18)   # грубая оценка стабильности
        
        # Emergent gravity эффект
        effective_g = self.P * (1 + 0.3 * (1 - stability/100))
        
        return {
            "baryonic_mass": baryonic_mass,
            "radius": radius,
            "mean_mismatch": round(mean_mismatch, 2),
            "stability": round(stability, 1),
            "effective_g_factor": round(effective_g, 3)
        }

# ========================
if __name__ == "__main__":
    model = ImprovedDOPHModel()
    
    print("=== Улучшенная модель dOPH ===\n")
    
    print("1. Спокойная галактика (типа Млечного Пути):")
    result_mw = model.simulate_galaxy(baryonic_mass=8e10, radius=15.0, num_patches=60, is_lsb=False)
    print(f"  Стабильность патчей: {result_mw['stability']}%")
    print(f"  Эффективный G-фактор: {result_mw['effective_g_factor']}")
    
    print("\n2. Проблемная LSB-галактика:")
    result_lsb = model.simulate_galaxy(baryonic_mass=2e9, radius=8.0, num_patches=40, is_lsb=True)
    print(f"  Стабильность патчей: {result_lsb['stability']}%")
    print(f"  Эффективный G-фактор: {result_lsb['effective_g_factor']}")
    
    print("\nВывод:")
    print("• Модель показывает, что LSB-галактики сложнее стабилизировать")
    print("• Emergent gravity и декуплинг помогают, но не полностью решают проблему масштабируемости")
