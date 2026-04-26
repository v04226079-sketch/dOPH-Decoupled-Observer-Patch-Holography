# code/sparc_fitting.py
# dOPH v2.1 — Работа с реальными данными SPARC
# Отдельный файл, синтетический тест не трогаем

import numpy as np
import os

np.random.seed(42)

class ImprovedDOPHModel:
    def __init__(self, strict_decoupling=True):
        self.P = np.sqrt(8.0 / 3.0)   # теоретическое значение
        self.gamma = 0.15
        self.strict_decoupling = strict_decoupling
    
    def simulate_galaxy(self, num_patches=50, is_lsb=False):
        """Упрощённая симуляция галактики для теста"""
        diversity_factor = 1.8 if is_lsb else 1.0
        mismatch = np.random.normal(1.0, 0.6 * diversity_factor, num_patches)
        mismatch = np.clip(mismatch, 0.3, 12.0)
        
        for _ in range(25):
            if self.strict_decoupling:
                overlap_factor = np.abs(np.cos(np.random.uniform(0, np.pi/2, num_patches))) ** 2
                correction = (1 - overlap_factor) * 0.12
                mismatch *= (1 - correction)
            mismatch *= (1 - self.gamma * 0.05)
            mismatch *= 0.96
        
        mean_mismatch = np.mean(mismatch)
        stability = max(40, 100 - mean_mismatch * 18)
        effective_g = self.P * (1 + 0.3 * (1 - stability/100))
        
        return {
            "stability": round(stability, 1),
            "effective_g_factor": round(effective_g, 5)
        }


def test_sparc_integration():
    model = ImprovedDOPHModel(strict_decoupling=True)
    
    print("=== dOPH v2.1 — Интеграция с реальными данными SPARC ===\n")
    print(f"Теоретический P = {model.P:.5f} (√(8/3))\n")
    
    print("Текущий статус:")
    print("• Модель готова к работе с реальными данными")
    print("• Синтетический тест остаётся в doph_reproducible_test.py")
    print("• Следующий шаг — чтение файлов из папки Rotmod_LTG\n")
    
    # Пример теста
    print("Тестовый запуск модели:")
    res_normal = model.simulate_galaxy(num_patches=60, is_lsb=False)
    print(f"Обычная галактика     → Стабильность: {res_normal['stability']}%")
    
    res_lsb = model.simulate_galaxy(num_patches=40, is_lsb=True)
    print(f"LSB-галактика         → Стабильность: {res_lsb['stability']}%")
    
    print("\nГотов к загрузке реальных данных SPARC.")
    print("Когда скачаешь sparc_database.zip и распакуешь папку Rotmod_LTG — скажи.")

if __name__ == "__main__":
    test_sparc_integration()
