import pandas as pd

def moscow_method(data):
    """Рассчитывает приоритеты по MoSCoW."""

    # Проверяем, есть ли нужный столбец
    if 'Category' not in data.columns:
        raise ValueError("Ошибка: Входные данные должны содержать столбец 'Category'.")

    # Преобразуем в строковый формат (если данные не строковые)
    data['Category'] = data['Category'].astype(str)

    # Убираем возможные пропущенные значения (NaN)
    data = data.dropna(subset=['Category'])

    # Подсчет количества требований в каждой категории
    categories = data['Category'].value_counts().to_dict()

    return categories
