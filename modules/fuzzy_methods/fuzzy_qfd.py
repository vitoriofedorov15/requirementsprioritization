import numpy as np
import pandas as pd

def fuzzy_qfd_type2(data):
    """Рассчитывает нечеткие веса требований с учетом неопределенности (Type-2 Fuzzy Logic)."""

    # Проверка наличия столбца 'Weight'
    if "Weight" not in data.columns:
        raise KeyError("❌ Ошибка: Колонка 'Weight' отсутствует в `input.csv`!")

    # Преобразуем Weight в числовой формат (на случай строк)
    data = data.copy()
    data["Weight"] = pd.to_numeric(data["Weight"], errors="coerce")

    # Удаляем строки с NaN в Weight
    data = data.dropna(subset=["Weight"])

    # Проверяем, не пуст ли DataFrame после очистки
    if data.empty:
        raise ValueError("Ошибка: После очистки данных таблица пуста. Проверьте корректность входных значений.")

    # Вычисление нечетких границ: (min, likely, max)
    aggregated_weights = []
    for weight in data["Weight"]:
        min_val = weight * 0.8  # Нижняя граница (учет неопределенности)
        likely_val = weight      # Основное значение
        max_val = weight * 1.2   # Верхняя граница (учет неопределенности)
        aggregated_weights.append([min_val, likely_val, max_val])

    return np.array(aggregated_weights)


