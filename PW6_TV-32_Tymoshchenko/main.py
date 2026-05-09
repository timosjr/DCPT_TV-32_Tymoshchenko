import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

folder_path = 'csv_files'
files = glob.glob(os.path.join(folder_path, '*.csv'))

comparison_data = []

if not files:
    print("Файли не знайдено.")
else:
    for file_path in files:
        file_name = os.path.basename(file_path)

        try:
            df = pd.read_csv(file_path, skipinitialspace=True)
            time_col = 'Time (s)'
            abs_col = 'Absolute field (µT)'

            if time_col in df.columns and abs_col in df.columns:
                min_val = df[abs_col].min()
                mean_val = df[abs_col].mean()
                max_val = df[abs_col].max()

                # 1. Побудова індивідуального графіка (для кожного файлу)
                plt.figure(figsize=(8, 4))
                plt.plot(df[time_col], df[abs_col], color='steelblue', alpha=0.8)
                plt.axhline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
                plt.title(f"Детальний графік: {file_name}")
                plt.xlabel("Час (с)")
                plt.ylabel("Поле (µT)")
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.show()

                # 2. Збір даних для порівняння
                if "годинник" not in file_name.lower():
                    comparison_data.append({
                        'назва': file_name.replace('.csv', ''),
                        'min': min_val,
                        'mean': mean_val,
                        'max': max_val
                    })
            else:
                print(f"У файлі {file_name} відсутні потрібні колонки.")
        except Exception as e:
            print(f"Помилка у файлі {file_name}: {e}")

    # 3. Побудова порівняльного графіка
    if comparison_data:
        comp_df = pd.DataFrame(comparison_data)

        x = range(len(comp_df))
        width = 0.25

        fig, ax = plt.subplots(figsize=(12, 7))

        ax.bar([i - width for i in x], comp_df['min'], width, label='Мінімум', color='#7fb3d5')
        ax.bar(x, comp_df['mean'], width, label='Середнє', color='#2980b9')
        ax.bar([i + width for i in x], comp_df['max'], width, label='Максимум', color='#1a5276')

        ax.set_title('Порівняння рівнів магнітного поля побутових пристроїв', fontsize=14)
        ax.set_ylabel('Магнітна індукція (µT)')
        ax.set_xticks(x)
        ax.set_xticklabels(comp_df['назва'], rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.show()
    else:
        print("Немає даних для порівняння (всі файли містили 'годинник' або були некоректні).")