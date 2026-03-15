import pandas as pd
import numpy as np


def calculate_dqi(df):
    # 1. Частка не-NaN
    null_score = 1 - df.isnull().mean().mean()

    # 2. Частка не-дублікатів
    dup_score = 1 - df.duplicated().sum() / len(df)

    # 3. Частка коректних значень
    # Припустимо, некоректні — це від'ємні значення
    correct_score = (df['price'] >= 0).mean() if 'price' in df.columns else 1

    # 4. Частка значень без викидів (за методом IQR)
    if 'price' in df.columns:
        Q1 = df['price'].quantile(0.25)
        Q3 = df['price'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df['price'] < (Q1 - 1.5 * IQR)) | (df['price'] > (Q3 + 1.5 * IQR))).sum()
        outlier_score = 1 - outliers / len(df)
    else:
        outlier_score = 1

    dqi = np.mean([null_score, dup_score, correct_score, outlier_score])

    return {
        "DQI": dqi,
        "Null Score": null_score,
        "Duplicate Score": dup_score,
        "Correctness Score": correct_score,
        "Outlier Score": outlier_score
    }


# --- Приклад роботи ---

# 1. Дані "ДО" (з помилками)
data = {
    'id': [1, 2, 2, 4, 5, 6],
    'price': [100, -50, 100, 200, 10000, None]  # -50 (некоректне), 10000 (викид), None (NaN)
}
df_before = pd.DataFrame(data)

# 2. Пайплайн очищення
df_after = df_before.copy()
df_after = df_after.drop_duplicates()
df_after['price'] = df_after['price'].apply(lambda x: x if x is None or x >= 0 else np.nan)  # прибираємо від'ємні
df_after['price'] = df_after['price'].fillna(df_after['price'].median())  # заповнюємо NaN

# Прибираємо викиди
Q1, Q3 = df_after['price'].quantile([0.25, 0.75])
IQR = Q3 - Q1
df_after = df_after[~((df_after['price'] < (Q1 - 1.5 * IQR)) | (df_after['price'] > (Q3 + 1.5 * IQR)))]

# 3. Розрахунок результатів
results_before = calculate_dqi(df_before)
results_after = calculate_dqi(df_after)

print(f"DQI До: {results_before['DQI']:.2f}")
print(f"DQI Після: {results_after['DQI']:.2f}")
