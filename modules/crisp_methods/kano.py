import pandas as pd


def kano_model(data):
    """Рассчитывает модель Кано и классифицирует требования."""

    # Проверка наличия необходимых колонок
    required_columns = {'Satisfaction', 'Effect'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Отсутствуют необходимые столбцы: {required_columns - set(data.columns)}")

    # Преобразуем к числовому типу (на случай строковых значений)
    data = data.copy()
    data[['Satisfaction', 'Effect']] = data[['Satisfaction', 'Effect']].apply(pd.to_numeric, errors='coerce')

    # Определение категорий
    categories = {
        "Basic": data[(data['Satisfaction'] < 0.5) & (data['Effect'] < 0.5)].copy(),  # Базовые требования
        "Attractive": data[(data['Satisfaction'] < 0.5) & (data['Effect'] >= 0.5)].copy(),  # Привлекательные требования
        "Indifferent": data[(data['Satisfaction'] >= 0.5) & (data['Effect'] >= 0.5)].copy(),  # Равнодушные
        "Reverse": data[(data['Satisfaction'] >= 0.5) & (data['Effect'] < 0.5)].copy(),  # Обратные
    }

    return categories
