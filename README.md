# dOPH — Decoupled Observer Patch Holography

**Улучшенная holographic модель для описания кривых вращения галактик без тёмной материи**

### Основная идея
dOPH (Decoupled Observer Patch Holography) — это развитие идеи [Observer Patch Holography](https://github.com/FloatingPragma/observer-patch-holography). Модель использует концепцию "наблюдательных патчей" на голографическом экране и механизм **decoupling** для исправления локальных рассогласований.

### Ключевые особенности
- Фиксированный теоретический параметр **P = √(8/3) ≈ 1.633**
- Density-dependent усиление гравитации
- Механизм decoupling (локальное исправление)
- Двухкомпонентная модель (газ + звёзды)

### Результаты
- Хорошо описывает плоские кривые вращения галактик
- Средний reduced χ² на тестовых галактиках ≈ **1.9**

### Структура репозитория

- [`doph_model_improved2.py`](doph_model_improved2.py) — основная математическая модель
- [`tools/doph_calculator.py`](tools/doph_calculator.py) — **простой калькулятор** для быстрого расчёта
- `docs/` и PDF-файлы — подробное описание теории

### Как использовать калькулятор

```bash
python tools/doph_calculator.py
