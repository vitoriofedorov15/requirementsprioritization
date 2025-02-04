import numpy as np
import pandas as pd


def intuitionistic_fuzzy_delphi(data):
    """Реализует интуиционистский нечеткий метод Delphi для приоритизации требований."""

    # Проверяем наличие необходимых столбцов
    required_columns = {"Satisfaction", "Effect"}
    if not required_columns.issubset(data.columns):
        raise KeyError(f"❌ Ошибка: Отсутствуют столбцы {required_columns - set(data.columns)} в `input.csv`!")

    # Преобразуем данные в числовой формат (на случай строк)
    data = data.copy()
    data[["Satisfaction", "Effect"]] = data[["Satisfaction", "Effect"]].apply(pd.to_numeric, errors="coerce")

    # Удаляем строки с NaN
    data = data.dropna(subset=["Satisfaction", "Effect"])

    # Проверяем, не пуст ли DataFrame после очистки
    if data.empty:
        raise ValueError("Ошибка: После очистки данных таблица пуста. Проверьте корректность входных значений.")

    # Интуиционистские нечеткие оценки
    membership = data["Satisfaction"].mean()  # Среднее значение принадлежности
    non_membership = data["Effect"].apply(lambda x: 1 - x).mean()  # Среднее значение не-принадлежности
    uncertainty = 1 - (membership + non_membership)  # Уровень неопределенности

    # Коррекция значений (чтобы избежать отрицательной неопределенности)
    if uncertainty < 0:
        uncertainty = 0  # Если сумма membership + non_membership > 1, то неопределенность обнуляется

    return np.array([membership, non_membership, uncertainty])
