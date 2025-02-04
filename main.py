import logging
import os
import pandas as pd
import numpy as np

from modules.data_loader import load_data
from modules.fuzzy_methods.fuzzy_topsis import fuzzy_topsis_type2
from modules.fuzzy_methods.fuzzy_qfd import fuzzy_qfd_type2
from modules.fuzzy_methods.fuzzy_delphi import intuitionistic_fuzzy_delphi
from modules.crisp_methods.moscow import moscow_method
from modules.crisp_methods.kano import kano_model
from modules.crisp_methods.topsis import topsis_method
from modules.visualization.plot_results import plot_results
from modules.export import export_results

# ✅ Создаем папки, если их нет
os.makedirs("logs", exist_ok=True)
os.makedirs("data/output", exist_ok=True)

logging.basicConfig(
    filename="logs/project.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def convert_to_dataframe(data, index_label="Requirement ID", value_label="Value"):
    """Конвертирует данные в DataFrame перед экспортом."""
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, dict):
        return pd.DataFrame(list(data.items()), columns=[index_label, value_label])
    elif isinstance(data, np.ndarray):
        if data.ndim == 1:  # Если одномерный массив
            return pd.DataFrame({value_label: data})
        elif data.ndim == 2 and data.shape[1] == 3:  # Если трехмерный Type-2 Fuzzy
            return pd.DataFrame(data, columns=["Min", "Likely", "Max"])
        else:
            raise ValueError("Ошибка: Неподдерживаемая размерность массива для DataFrame.")
    elif isinstance(data, list):
        return pd.DataFrame({value_label: data})
    else:
        return pd.DataFrame({value_label: [data]})  # Если одно значение


def safe_mean(data):
    """Вычисляет среднее значение, даже если данные - это dict или list."""
    if isinstance(data, dict):
        values = list(data.values())
    elif isinstance(data, (list, np.ndarray)):
        values = np.array(data)
    else:
        return 0
    if len(values) == 0:
        return 0
    return np.mean(values)

def main():
    try:
        print("🔹 Загружаем данные...")
        data = load_data("data/input/input.csv")

        if data is None or data.empty:
            logging.error("Ошибка загрузки данных. Проверь input.csv")
            print("❌ Ошибка: данные не загружены! Проверь input.csv")
            return

        print("✅ Данные загружены успешно!")
        logging.info("Данные успешно загружены.")

        print("🔹 Запускаем анализ...")
        fuzzy_topsis_res = fuzzy_topsis_type2(data)
        fuzzy_qfd_res = fuzzy_qfd_type2(data)
        fuzzy_delphi_res = intuitionistic_fuzzy_delphi(data)
        moscow_res = moscow_method(data)
        kano_res = kano_model(data)
        topsis_res = topsis_method(data)

        print("✅ Анализ выполнен!")
        logging.info("Анализ успешно завершен.")


        print("🔹 Сохраняем результаты в файлы...")
        export_results(convert_to_dataframe(fuzzy_topsis_res), "data/output/fuzzy_topsis.csv")
        export_results(convert_to_dataframe(fuzzy_qfd_res), "data/output/fuzzy_qfd.csv")
        export_results(convert_to_dataframe(fuzzy_delphi_res), "data/output/fuzzy_delphi.csv")
        export_results(convert_to_dataframe(moscow_res), "data/output/moscow.csv")
        export_results(convert_to_dataframe(topsis_res), "data/output/topsis.csv")

        # Отдельно экспортируем Kano-модель
        for category, df in kano_res.items():
            export_results(df, f"data/output/kano_{category}.csv")

        print("✅ Результаты сохранены в `data/output/`!")
        logging.info("Результаты сохранены в файлы.")

        print("🔹 Запускаем визуализацию...")
        plot_results(
            safe_mean(fuzzy_topsis_res),
            safe_mean(fuzzy_qfd_res),
            safe_mean(fuzzy_delphi_res),
            safe_mean(moscow_res),
            safe_mean(kano_res),
            safe_mean(topsis_res),
        )

        logging.info("Визуализация завершена!")
        print("🎉 Анализ завершен! Смотри графики и файлы в `data/output/`.")

    except Exception as e:
        logging.error(f"❌ Ошибка в main.py: {str(e)}")
        print(f"❌ Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
