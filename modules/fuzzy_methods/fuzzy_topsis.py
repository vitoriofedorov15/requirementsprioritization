import numpy as np
import pandas as pd

def fuzzy_topsis_type2(data):
    """Рассчитывает Type-2 Fuzzy TOPSIS."""

    # Проверяем, есть ли нужные столбцы
    required_columns = {"Weight", "Satisfaction", "Effect"}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise KeyError(f"❌ Ошибка: Отсутствуют столбцы: {missing_columns}")

    # Приводим данные к числовому формату
    data = data.copy()
    data[["Weight", "Satisfaction", "Effect"]] = data[["Weight", "Satisfaction", "Effect"]].apply(pd.to_numeric, errors="coerce")

    # Удаляем строки с NaN
    data = data.dropna(subset=["Weight", "Satisfaction", "Effect"])

    # Проверяем, не пуст ли DataFrame после очистки
    if data.empty:
        raise ValueError("Ошибка: После очистки данных таблица пуста. Проверьте корректность входных значений.")

    # Функция для генерации нечётких границ Type-2
    def to_type2_fuzzy(value):
        spread = value * 0.1  # 10% диапазон неопределённости
        return (value - spread, value, value + spread)

    # Генерация Type-2 нечётких чисел
    fuzzy_weights = np.array([to_type2_fuzzy(w) for w in data["Weight"].values])

    LMF = fuzzy_weights[:, 0]  # Нижняя граница (Lower Membership Function)
    Likely = fuzzy_weights[:, 1]  # Наиболее вероятное значение
    UMF = fuzzy_weights[:, 2]  # Верхняя граница (Upper Membership Function)

    # Нормализация по каждому критерию
    norm_LMF = LMF / np.sqrt((LMF ** 2).sum())
    norm_UMF = UMF / np.sqrt((UMF ** 2).sum())

    # Взвешивание нормализованных значений
    weighted_LMF = norm_LMF * data["Weight"].values
    weighted_UMF = norm_UMF * data["Weight"].values

    # Определение идеального положительного и отрицательного решений
    ideal_positive = weighted_UMF.max()
    ideal_negative = weighted_LMF.min()

    # Вычисление расстояний для каждого требования
    dist_positive = np.sqrt(((weighted_UMF - ideal_positive) ** 2).sum(axis=0))
    dist_negative = np.sqrt(((weighted_LMF - ideal_negative) ** 2).sum(axis=0))

    # Индекс близости к идеальному решению
    closeness = dist_negative / (dist_positive + dist_negative)

    return closeness
