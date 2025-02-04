import matplotlib.pyplot as plt
import numpy as np


def plot_results(fuzzy_topsis, fuzzy_qfd, fuzzy_delphi, moscow, kano, topsis):
    """Строит графики для анализа результатов методов приоритизации."""

    def safe_mean(data):
        """Безопасно вычисляет среднее значение, обрабатывая возможные ошибки."""
        if isinstance(data, dict):  # Если словарь, берем среднее по значениям
            values = list(data.values())
        elif isinstance(data, (list, np.ndarray)):  # Если список или массив
            values = np.array(data)
        else:
            return 0  # Если формат неизвестен, возвращаем 0

        if len(values) == 0:  # Если пусто, тоже 0
            return 0

        return np.mean(values)  # Вычисляем среднее

    # Вычисление средних значений
    fuzzy_means = [safe_mean(fuzzy_topsis), safe_mean(fuzzy_qfd), safe_mean(fuzzy_delphi)]
    crisp_means = [safe_mean(moscow), safe_mean(kano), safe_mean(topsis)]
    labels_fuzzy = ["Fuzzy TOPSIS", "Fuzzy QFD", "Fuzzy Delphi"]
    labels_crisp = ["MoSCoW", "Kano", "TOPSIS"]

    # Визуализация
    plt.figure(figsize=(12, 6))

    # График для нечетких методов
    plt.subplot(1, 2, 1)
    bars = plt.bar(labels_fuzzy, fuzzy_means, color=['blue', 'green', 'red'])
    plt.title("Средние значения нечетких методов")
    plt.ylabel("Среднее значение")
    for bar in bars:  # Добавление подписей значений
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{bar.get_height():.2f}",
                 ha='center', va='bottom', fontsize=10)

    # График для четких методов
    plt.subplot(1, 2, 2)
    bars = plt.bar(labels_crisp, crisp_means, color=['purple', 'orange', 'gray'])
    plt.title("Средние значения четких методов")
    plt.ylabel("Среднее значение")
    for bar in bars:  # Добавление подписей значений
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{bar.get_height():.2f}",
                 ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()
