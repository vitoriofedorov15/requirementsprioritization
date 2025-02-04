import numpy as np
import pandas as pd


def topsis_method(data):
    """Рассчитывает классический TOPSIS."""

    # Проверка, что в данных есть нужные колонки
    if 'Weight' not in data.columns:
        raise ValueError("Ошибка: Входные данные должны содержать столбец 'Weight'.")

    # Выделяем числовые колонки (исключая Weight)
    numeric_cols = data.drop(columns=['Weight'], errors='ignore').select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        raise ValueError("Ошибка: В таблице нет числовых данных для анализа TOPSIS.")

    # Нормализация по числовым столбцам
    normalized = data[numeric_cols] / np.sqrt((data[numeric_cols] ** 2).sum())

    # Применение весов
    weights = data["Weight"].values
    weighted = normalized.mul(weights, axis=0)

    # Определение идеального положительного и отрицательного решений
    ideal_positive = weighted.max()
    ideal_negative = weighted.min()

    # Вычисление расстояний
    dist_positive = np.sqrt(((weighted - ideal_positive) ** 2).sum(axis=1))
    dist_negative = np.sqrt(((weighted - ideal_negative) ** 2).sum(axis=1))

    # Индекс близости к идеальному решению
    closeness = dist_negative / (dist_positive + dist_negative)

    return closeness


def fuzzy_topsis(data):
    """Рассчитывает нечеткий TOPSIS."""

    if not {'Min', 'Likely', 'Max', 'Weight'}.issubset(data.columns):
        raise ValueError("Ошибка: Входные данные должны содержать столбцы 'Min', 'Likely', 'Max' и 'Weight'.")

    # Выделяем только нужные числовые колонки
    fuzzy_cols = ['Min', 'Likely', 'Max']

    # Нормализация по нечетким числам
    normalized = data[fuzzy_cols] / np.sqrt((data[fuzzy_cols] ** 2).sum())

    # Применение весов
    weights = data["Weight"].values
    weighted = normalized.mul(weights, axis=0)

    # Определение расстояний до идеального и анти-идеального решений
    ideal_positive = weighted['Max']
    ideal_negative = weighted['Min']

    dist_positive = np.sqrt(((weighted['Likely'] - ideal_positive) ** 2).sum())
    dist_negative = np.sqrt(((weighted['Likely'] - ideal_negative) ** 2).sum())

    closeness = dist_negative / (dist_positive + dist_negative)

    return closeness

