import numpy as np

class DOPH_Calculator:
    def __init__(self):
        self.P = np.sqrt(8.0 / 3.0)  # Главный параметр ≈ 1.633
        self.rho_c_gas = 3.0e-24
        self.rho_c_stars = 2.3e-25
        self.rho_trans = 4.5e-25
        self.gamma = 1.80
        self.delta_gas = 1.60
        self.delta_stars = 1.55
    
    def local_weight(self, rho):
        if rho < 1e-25:
            return 1.35
        elif rho < 5e-25:
            return 1.18
        return 1.0
    
    def pi_eff(self, sb_disk):
        """Простой расчёт π_eff по SBdisk"""
        rho_stars = sb_disk * 1e-22   # Примерный перевод
        rho_gas = rho_stars * 0.1
        
        pi_gas = self.P / (1 + (rho_gas / self.rho_c_gas)**self.delta_gas)
        pi_stars = self.P / (1 + (rho_stars / self.rho_c_stars)**self.delta_stars)
        
        w_gas = 1 / (1 + (rho_gas / self.rho_trans)**self.gamma)
        w_stars = 1 - w_gas
        
        pi_base = w_gas * pi_gas + w_stars * pi_stars
        weight = self.local_weight((rho_gas + rho_stars)/2)
        
        return pi_base * weight
    
    def predict_v(self, v_bary, sb_disk):
        """Предсказанная скорость"""
        pie = self.pi_eff(sb_disk)
        return np.sqrt(v_bary**2 * pie)


# ====================== КАЛЬКУЛЯТОР ======================
if __name__ == "__main__":
    model = DOPH_Calculator()
    
    print("=== dOPH Калькулятор ===\n")
    print("Вводи данные по одной точке за раз.")
    print("Для выхода напиши 'exit'\n")
    
    while True:
        try:
            sb = float(input("SBdisk (L/pc²): "))
            if sb < 0:
                break
            v_bary = float(input("V_bary (km/s): "))
            
            pi = model.pi_eff(sb)
            v_model = model.predict_v(v_bary, sb)
            
            print(f"π_eff = {pi:.3f}")
            print(f"V_model = {v_model:.1f} km/s\n")
            
        except:
            print("Выход.")
            break
