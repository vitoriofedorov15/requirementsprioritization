import pandas as pd


def load_data(file_path):
    """Загружает CSV-файл и приводит числовые столбцы к корректному формату."""

    try:
        # Читаем CSV-файл
        data = pd.read_csv(file_path)

        # Проверяем, не пуст ли файл
        if data.empty:
            raise ValueError("Файл пуст или не содержит данных.")

        # Проверяем наличие нужных столбцов
        required_columns = {"Satisfaction", "Effect", "Weight"}
        missing_columns = required_columns - set(data.columns)

        if missing_columns:
            raise ValueError(f"Ошибка: отсутствуют колонки {missing_columns} в CSV-файле.")

        # Преобразуем числовые колонки в float
        for col in required_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

        # Удаляем строки, где есть NaN в критически важных колонках
        data.dropna(subset=required_columns, inplace=True)

        # Проверяем, не стал ли DataFrame пустым после удаления NaN
        if data.empty:
            raise ValueError("Ошибка: после обработки данных таблица пуста. Проверьте корректность входного файла.")

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Ошибка: Файл {file_path} не найден.")

    except pd.errors.EmptyDataError:
        raise ValueError(f"❌ Ошибка: Файл {file_path} пуст или не содержит данных.")

    except Exception as e:
        raise ValueError(f"❌ Ошибка загрузки данных: {e}")
