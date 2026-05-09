import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

folder_path = 'csv_files'

extension = 'csv'
files = glob.glob(os.path.join(folder_path, f'*.{extension}'))

if not files:
    print(f"У папці '{folder_path}' не знайдено жодного CSV файлу.")
else:
    for file_path in files:
        try:
            file_name = os.path.basename(file_path)

            df = pd.read_csv(file_path, skipinitialspace=True)

            # Перевіряємо наявність необхідних колонок
            time_col = 'Time (s)'
            abs_col = 'Absolute field (µT)'

            if time_col in df.columns and abs_col in df.columns:

                mean_value = df[abs_col].mean()

                plt.figure(figsize=(10, 6))
                plt.plot(df[time_col], df[abs_col], label='Абсолютне поле', color='blue')

                # Додаємо лінію середнього значення
                plt.axhline(y=mean_value, color='red', linestyle='--',
                            label=f'Середнє: {mean_value:.2f} µT')

                # Налаштування тексту та підписів
                plt.title(f"Магнітне поле: {file_name}")
                plt.xlabel("Час (с)")
                plt.ylabel("Абсолютне значення (µT)")
                plt.legend()
                plt.grid(True, linestyle=':', alpha=0.7)

                # Відображаємо графік
                plt.show()

            else:
                print(f"Файл {file_name} не містить потрібних колонок ('{time_col}' або '{abs_col}').")

        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")
