# Decoupled Observer Patch Holography (dOPH)

**Декуплированная Голография Наблюдательных Патчей**

Улучшенная версия Observer Patch Holography Бернхарда Мюллера с аксиомой **Декуплинг** и комбинированными механизмами стабилизации (emergent gravity, фазовый консенсус, демпфирование, инерция).

### Основные материалы

- **[Русская версия — Финальный анализ (апрель 2026)](docs/dOPH_Final_Fixed_April2026.tex)**
- **[English version — Final Analysis (April 2026)](docs/dOPH_Final_April2026_EN.tex)**

### Код и тесты

В папке [`code/`](code/) находятся скрипты для тестирования модели:

- `doph_reproducible_test.py` — основной воспроизводимый тест (рекомендуется запускать первым)
- `doph_results_table.py` — красивая таблица результатов
- `doph_model_basic.py` — базовая модель патчей

**Как запустить скрипты:**

```bash
cd code
python doph_reproducible_test.py
