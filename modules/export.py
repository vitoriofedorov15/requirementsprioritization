import pandas as pd
import os


def export_results(data, file_path):
    """Сохраняет результаты в CSV-файл с проверками."""
    try:
        # Если данные не DataFrame, преобразуем
        if not isinstance(data, pd.DataFrame):
            data = convert_to_dataframe(data)

        # Проверяем, что DataFrame не пустой
        if data.empty:
            raise ValueError(f"⚠️ Данные пустые, файл {file_path} не будет создан.")

        # Создаём директорию, если её нет
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Сохраняем данные в CSV
        data.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"✅ Результаты успешно сохранены в {file_path}")

    except Exception as e:
        raise ValueError(f"❌ Ошибка сохранения файла {file_path}: {e}")
