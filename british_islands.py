import numpy as np
import matplotlib.pyplot as plt

data = np.load('gb-alt.npy')

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.flatten()

sea_levels = [0, 25, 50, 200]
titles = ['Поточна карта (рівень моря = 0 м)', 
          'Підвищення рівня моря на 25 м',
          'Підвищення рівня моря на 50 м',
          'Підвищення рівня моря на 200 м']

original_area = np.sum(data > 0)

for i, (level, title) in enumerate(zip(sea_levels, titles)):
    if level == 0:
        land_mask = data > 0
    else:
        land_mask = data > level
    
    land_percentage = (np.sum(land_mask) / original_area) * 100
    
    im = axes[i].imshow(land_mask, cmap='Blues', interpolation='nearest')
    axes[i].set_title(f'{title}\nЗалишок суші: {land_percentage:.2f}%', fontsize=12)
    axes[i].set_xlabel('Довгота', fontsize=10)
    axes[i].set_ylabel('Широта', fontsize=10)
    
    axes[i].axhline(y=data.shape[0]//2, color='red', linewidth=0.5, alpha=0.5)
    axes[i].axvline(x=data.shape[1]//2, color='red', linewidth=0.5, alpha=0.5)

plt.tight_layout()
plt.savefig('british_isles_sea_level.png', dpi=150)
plt.show()

print("=" * 70)
print("АНАЛІЗ ПІДВИЩЕННЯ РІВНЯ МОРЯ")
print("=" * 70)

total_cells = data.size
land_cells = np.sum(data > 0)
print(f"\nЗагальна кількість комірок: {total_cells:,}")
print(f"Поточна площа суші: {land_cells:,} комірок")

for level in [25, 50, 200]:
    remaining_land = np.sum(data > level)
    percentage = (remaining_land / land_cells) * 100
    print(f"\nПідвищення рівня моря на {level} м:")
    print(f"  Залишок суші: {remaining_land:,} комірок")
    print(f"  Відносно поточної площі: {percentage:.2f}%")

elevation_stats = {
    'min': np.min(data),
    'max': np.max(data),
    'mean': np.mean(data[data > 0]),
    'median': np.median(data[data > 0])
}

print("\n" + "=" * 70)
print("СТАТИСТИКА ВИСОТ")
print("=" * 70)
print(f"Мінімальна висота: {elevation_stats['min']:.1f} м")
print(f"Максимальна висота: {elevation_stats['max']:.1f} м")
print(f"Середня висота суші: {elevation_stats['mean']:.1f} м")
print(f"Медіанна висота: {elevation_stats['median']:.1f} м")
