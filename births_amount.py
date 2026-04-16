import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

data = np.genfromtxt('births.csv', delimiter='\t', skip_header=1, dtype=float, encoding='utf-8')

births = {}
for row in data:
    month = int(row[0])
    day = int(row[1])
    count = int(row[2])
    
    if month >= 1 and month <= 12:
        if month == 2 and day == 29:
            continue
        if (month in [4, 6, 9, 11] and day > 30) or (month == 2 and day > 28):
            continue
        if day >= 1 and day <= 31:
            births[(month, day)] = count

daily_births = np.zeros((12, 31))
for (month, day), count in births.items():
    daily_births[month-1, day-1] = count

daily_births[daily_births == 0] = np.nan

total_births = np.nansum(daily_births)
probability = daily_births / total_births

fig, ax = plt.subplots(figsize=(14, 8))

cax = ax.imshow(probability, cmap='hot', aspect='auto', interpolation='nearest')
cbar = plt.colorbar(cax, ax=ax)
cbar.set_label('Вірогідність народження', fontsize=12)

months = ['Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер', 'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру']
days = np.arange(1, 32)

ax.set_xticks(np.arange(len(days)))
ax.set_yticks(np.arange(len(months)))
ax.set_xticklabels(days, fontsize=8, rotation=90)
ax.set_yticklabels(months, fontsize=10)
ax.set_xlabel('День місяця', fontsize=12)
ax.set_ylabel('Місяць', fontsize=12)
ax.set_title('Вірогідність дня народження у США 1969-1988', fontsize=14)

for month in range(12):
    for day in range(31):
        if not np.isnan(probability[month, day]):
            prob_value = probability[month, day]
            if prob_value > np.nanmax(probability) * 0.8:
                text_color = 'white'
            else:
                text_color = 'black'
            ax.text(day, month, f'{prob_value*100:.2f}%', 
                    ha='center', va='center', fontsize=6, color=text_color)

ax.axhline(y=1.5, color='white', linewidth=2, linestyle='-')
ax.axhline(y=3.5, color='white', linewidth=2, linestyle='-')
ax.axhline(y=5.5, color='white', linewidth=2, linestyle='-')
ax.axhline(y=7.5, color='white', linewidth=2, linestyle='-')
ax.axhline(y=8.5, color='white', linewidth=2, linestyle='-')
ax.axhline(y=10.5, color='white', linewidth=2, linestyle='-')

plt.tight_layout()
plt.savefig('birth_probability_heatmap.png', dpi=150)
plt.show()

print("=" * 70)
print("АНАЛІЗ ВІРОГІДНОСТЕЙ НАРОДЖЕННЯ")
print("=" * 70)

max_prob = np.nanmax(probability)
max_pos = np.where(probability == max_prob)
max_month = max_pos[0][0] + 1
max_day = max_pos[1][0] + 1
print(f"Найбільш ймовірний день народження: {max_day}.{max_month:02d} (вірогідність {max_prob*100:.4f}%)")

min_prob = np.nanmin(probability[~np.isnan(probability)])
min_pos = np.where(probability == min_prob)
min_month = min_pos[0][0] + 1
min_day = min_pos[1][0] + 1
print(f"Найменш ймовірний день народження: {min_day}.{min_month:02d} (вірогідність {min_prob*100:.4f}%)")

monthly_avg = np.nanmean(probability, axis=1) * 100
print(f"\nСередня вірогідність по місяцях:")
for i, avg in enumerate(monthly_avg):
    print(f"  {months[i]}: {avg:.4f}%")

holidays = {
    (1, 1): "Новий рік",
    (7, 4): "День незалежності",
    (12, 24): "Святвечір",
    (12, 25): "Різдво",
    (12, 31): "Переддень Нового року"
}

print(f"\nВірогідність у святкові дні:")
for (month, day), name in holidays.items():
    if month-1 < 12 and day-1 < 31 and not np.isnan(probability[month-1, day-1]):
        prob = probability[month-1, day-1] * 100
        print(f"  {name} ({day}.{month:02d}): {prob:.4f}%")
