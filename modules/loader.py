import pandas as pd


def load_data(file_path):
    """Загружает CSV-файл с требованиями и весами, выполняя валидацию данных."""

    try:
        # Читаем CSV-файл
        data = pd.read_csv(file_path)

        # Проверяем, не пуст ли файл
        if data.empty:
            raise ValueError(f"❌ Ошибка: Файл {file_path} пуст или не содержит данных.")

        # Проверяем наличие нужных столбцов
        required_columns = {"Satisfaction", "Effect", "Weight"}
        missing_columns = required_columns - set(data.columns)

        if missing_columns:
            raise ValueError(f"❌ Ошибка: В файле {file_path} отсутствуют колонки {missing_columns}.")

        # Приводим числовые колонки к float
        for col in required_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

        # Удаляем строки, где есть NaN в критически важных колонках
        data.dropna(subset=required_columns, inplace=True)

        # Проверяем, не стал ли DataFrame пустым после удаления NaN
        if data.empty:
            raise ValueError(
                f"❌ Ошибка: После обработки данных таблица пуста. Проверьте корректность входного файла {file_path}.")

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Ошибка: Файл {file_path} не найден.")

    except pd.errors.EmptyDataError:
        raise ValueError(f"❌ Ошибка: Файл {file_path} пуст или не содержит данных.")

    except pd.errors.ParserError:
        raise ValueError(f"❌ Ошибка: Некорректный формат CSV в файле {file_path}.")

    except Exception as e:
        raise ValueError(f"❌ Ошибка загрузки данных из {file_path}: {e}")
