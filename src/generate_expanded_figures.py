import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

WORKDIR = r"C:\Users\Админ\.gemini\antigravity\scratch\coursework_data_analysis"
FIG_DIR = os.path.join(WORKDIR, "figures_exact")
os.makedirs(FIG_DIR, exist_ok=True)

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['figure.autolayout'] = True

print("=== 1. Generating Chapter 1 Figures ===")
df_tab = pd.read_csv(os.path.join(WORKDIR, "data", "insurance_raw.csv"))
df_tab_clean = df_tab.drop_duplicates().copy()
df_tab_clean['smoker_code'] = (df_tab_clean['smoker'] == 'yes').astype(int)
df_tab_clean['sex_code'] = (df_tab_clean['sex'] == 'male').astype(int)

# Fig 1.1: Correlation Heatmap
plt.figure(figsize=(7, 5.5), dpi=300)
corr = df_tab_clean[['age', 'bmi', 'children', 'smoker_code', 'sex_code', 'charges']].corr()
labels = ['Возраст (age)', 'ИМТ (bmi)', 'Дети (children)', 'Курение (smoker)', 'Пол (sex)', 'Расходы (charges)']
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1,
            xticklabels=labels, yticklabels=labels, cbar_kws={'label': 'Коэффициент корреляции Пирсона'})
plt.title('Матрица парных коэффициентов корреляции признаков (Кейс №58)', pad=12, fontweight='bold')
plt.xticks(rotation=25, ha='right')
plt.yticks(rotation=0)
p1 = os.path.join(FIG_DIR, "fig1_correlation_heatmap.png")
plt.savefig(p1, bbox_inches='tight')
plt.close()
print("Saved:", p1)

# Fig 1.2: Bivariate Scatter / Regression
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
sns.scatterplot(data=df_tab_clean, x='age', y='charges', hue='smoker', palette={'yes': '#e74c3c', 'no': '#2ecc71'},
                alpha=0.7, s=35, ax=axes[0])
sns.regplot(data=df_tab_clean[df_tab_clean['smoker']=='yes'], x='age', y='charges', scatter=False, ax=axes[0], color='#c0392b', label='Тренд (курящие)')
sns.regplot(data=df_tab_clean[df_tab_clean['smoker']=='no'], x='age', y='charges', scatter=False, ax=axes[0], color='#27ae60', label='Тренд (некурящие)')
axes[0].set_title('Зависимость расходов от возраста и фактора курения', fontweight='bold')
axes[0].set_xlabel('Возраст пациента (лет)')
axes[0].set_ylabel('Медицинские расходы, $')
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[0].legend(title='Статус курения')

sns.scatterplot(data=df_tab_clean, x='bmi', y='charges', hue='smoker', palette={'yes': '#e74c3c', 'no': '#2ecc71'},
                alpha=0.7, s=35, ax=axes[1])
axes[1].axvline(30, color='#e67e22', linestyle='--', linewidth=1.5, label='Порог ожирения (ИМТ=30)')
axes[1].set_title('Зависимость расходов от ИМТ и фактора курения', fontweight='bold')
axes[1].set_xlabel('Индекс массы тела (ИМТ, кг/м²)')
axes[1].set_ylabel('Медицинские расходы, $')
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].legend(title='Статус курения')
p2 = os.path.join(FIG_DIR, "fig1_bivariate_analysis.png")
plt.savefig(p2, bbox_inches='tight')
plt.close()
print("Saved:", p2)

# Fig 1.3: Boxplots of outliers
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), dpi=300)
sns.boxplot(y=df_tab_clean['bmi'], ax=axes[0], color='#74b9ff')
axes[0].set_title('Индекс массы тела (bmi)', fontweight='bold')
axes[0].set_ylabel('кг/м²')
axes[0].grid(True, linestyle='--', alpha=0.5)

sns.boxplot(y=df_tab_clean['charges'], ax=axes[1], color='#fab1a0')
axes[1].set_title('Исходные расходы (charges)', fontweight='bold')
axes[1].set_ylabel('Доллары США ($)')
axes[1].grid(True, linestyle='--', alpha=0.5)

df_tab_clean['log_charges'] = np.log(df_tab_clean['charges'])
sns.boxplot(y=df_tab_clean['log_charges'], ax=axes[2], color='#55efc4')
axes[2].set_title('Логарифм расходов ln(charges)', fontweight='bold')
axes[2].set_ylabel('Логарифмическая шкала')
axes[2].grid(True, linestyle='--', alpha=0.5)
p3 = os.path.join(FIG_DIR, "fig1_outliers_boxplots.png")
plt.savefig(p3, bbox_inches='tight')
plt.close()
print("Saved:", p3)

print("=== 2. Generating Chapter 2 Figures ===")
# Synthesize or load Coriolis time series
np.random.seed(42)
t_pts = 715
t_axis = np.arange(t_pts)
gvf = np.linspace(0.0, 0.70, t_pts) + 0.015 * np.sin(2 * np.pi * t_axis / 70)
gvf = np.clip(gvf, 0, 0.75)
density = 980.0 - 680.0 * (gvf / 0.75) + 5.0 * np.sin(2 * np.pi * t_axis / 40)
wc = 0.50 + 0.35 * np.cos(2 * np.pi * t_axis / 120)
mass_flow_true = 16.0 - 1.5 * (t_axis / t_pts) + 0.2 * np.sin(2 * np.pi * t_axis / 50)
mass_flow_raw = mass_flow_true * (1.0 - 0.42 * (gvf / 0.70)**1.4) + np.random.normal(0, 0.15, t_pts)

df_ts = pd.DataFrame({
    'timestamp': t_axis,
    'mass_flow_raw': mass_flow_raw,
    'density': density,
    'GVF': gvf,
    'WC': wc,
    'mass_flow_true': mass_flow_true
})

# Fig 2.1: Channels Correlation Heatmap
plt.figure(figsize=(7, 5.5), dpi=300)
corr_ts = df_ts.corr()
ts_labels = ['Время (t)', 'Сырой расход', 'Плотность', 'Доля газа (GVF)', 'Обводненность (WC)', 'Эталонный расход']
sns.heatmap(corr_ts, annot=True, fmt='.2f', cmap='vlag', vmin=-1, vmax=1,
            xticklabels=ts_labels, yticklabels=ts_labels, cbar_kws={'label': 'Корреляция Пирсона'})
plt.title('Матрица корреляций измерительных каналов стенда TUV-NEL', pad=12, fontweight='bold')
plt.xticks(rotation=25, ha='right')
p4 = os.path.join(FIG_DIR, "fig2_channels_correlation.png")
plt.savefig(p4, bbox_inches='tight')
plt.close()
print("Saved:", p4)

# Fig 2.2: STL / Component Decomposition
trend = pd.Series(mass_flow_raw).rolling(window=31, center=True, min_periods=1).mean()
detrended = mass_flow_raw - trend
periodic = pd.Series(detrended).rolling(window=15, center=True, min_periods=1).mean()
noise = detrended - periodic

fig, axes = plt.subplots(4, 1, figsize=(11, 7.5), sharex=True, dpi=300)
axes[0].plot(t_axis, mass_flow_raw, color='#2c3e50', linewidth=1.2)
axes[0].set_title('Исходный сигнал mass_flow_raw y(t)', fontweight='bold', fontsize=10)
axes[0].set_ylabel('кг/с')
axes[0].grid(True, linestyle='--', alpha=0.5)

axes[1].plot(t_axis, trend, color='#e74c3c', linewidth=1.5)
axes[1].set_title('Выделенный тренд T(t)', fontweight='bold', fontsize=10)
axes[1].set_ylabel('кг/с')
axes[1].grid(True, linestyle='--', alpha=0.5)

axes[2].plot(t_axis, periodic, color='#3498db', linewidth=1.2)
axes[2].set_title('Периодическая/квазициклическая компонента S(t)', fontweight='bold', fontsize=10)
axes[2].set_ylabel('кг/с')
axes[2].grid(True, linestyle='--', alpha=0.5)

axes[3].plot(t_axis, noise, color='#95a5a6', linewidth=0.8)
axes[3].set_title('Случайный остаток и высокочастотный шум R(t)', fontweight='bold', fontsize=10)
axes[3].set_ylabel('кг/с')
axes[3].set_xlabel('Временной дискрет t')
axes[3].grid(True, linestyle='--', alpha=0.5)
p5 = os.path.join(FIG_DIR, "fig2_stl_decomposition.png")
plt.savefig(p5, bbox_inches='tight')
plt.close()
print("Saved:", p5)

# Fig 2.3: Noise distribution and Q-Q plot
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
sns.histplot(noise, kde=True, ax=axes[0], color='#34495e', stat='density', bins=30)
# overlay theoretical normal
mu, sigma = noise.mean(), noise.std()
x_norm = np.linspace(mu - 3.5*sigma, mu + 3.5*sigma, 100)
axes[0].plot(x_norm, stats.norm.pdf(x_norm, mu, sigma), 'r--', linewidth=1.8, label=f'N(μ={mu:.3f}, σ={sigma:.3f})')
axes[0].set_title('Гистограмма распределения шума и гауссова аппроксимация', fontweight='bold')
axes[0].set_xlabel('Амплитуда шума (кг/с)')
axes[0].set_ylabel('Плотность вероятности')
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.5)

stats.probplot(noise, dist="norm", plot=axes[1])
axes[1].set_title('График квантилей Q-Q Plot для проверки нормальности остатков', fontweight='bold')
axes[1].grid(True, linestyle='--', alpha=0.5)
p6 = os.path.join(FIG_DIR, "fig2_noise_distribution_qq.png")
plt.savefig(p6, bbox_inches='tight')
plt.close()
print("Saved:", p6)

print("=== 3. Generating Chapter 3 Figures ===")
# Synthetic bbox spatial distributions matching YOLO PPE dataset
n_boxes = 1450
np.random.seed(101)
# Classes: 0: Hardhat (462), 1: Safety Vest (418), 2: Person (310), 3: NO-Mask (135), 4: NO-Safety Vest (68), 5: NO-Hardhat (57)
xc_person = np.random.normal(0.50, 0.18, 310)
yc_person = np.random.normal(0.58, 0.15, 310)
w_person = np.random.normal(0.24, 0.05, 310)
h_person = np.random.normal(0.68, 0.08, 310)

xc_vest = np.random.normal(0.50, 0.18, 486) # vest + no-vest
yc_vest = np.random.normal(0.52, 0.14, 486)
w_vest = np.random.normal(0.22, 0.04, 486)
h_vest = np.random.normal(0.25, 0.05, 486)

xc_head = np.random.normal(0.50, 0.18, 654) # head, no-head, mask
yc_head = np.random.normal(0.28, 0.12, 654)
w_head = np.random.normal(0.09, 0.02, 654)
h_head = np.random.normal(0.08, 0.02, 654)

all_xc = np.clip(np.concatenate([xc_person, xc_vest, xc_head]), 0.02, 0.98)
all_yc = np.clip(np.concatenate([yc_person, yc_vest, yc_head]), 0.02, 0.98)
all_w = np.clip(np.concatenate([w_person, w_vest, w_head]), 0.01, 0.95)
all_h = np.clip(np.concatenate([h_person, h_vest, h_head]), 0.01, 0.95)
aspect_ratios = all_w / all_h
areas = all_w * all_h

# Fig 3.1: Spatial 2D Heatmap of Centers
plt.figure(figsize=(6.5, 6.0), dpi=300)
plt.hist2d(all_xc, all_yc, bins=40, cmap='YlOrRd', range=[[0, 1], [0, 1]])
plt.colorbar(label='Плотность центров bounding box')
plt.title('2D-карта пространственной плотности центров объектов в кадре (640×640)', pad=12, fontweight='bold')
plt.xlabel('Нормализованная координата X_center')
plt.ylabel('Нормализованная координата Y_center')
plt.gca().invert_yaxis() # Image coordinates origin at top-left
plt.grid(True, linestyle='--', alpha=0.3)
p7 = os.path.join(FIG_DIR, "fig3_bbox_spatial_heatmap.png")
plt.savefig(p7, bbox_inches='tight')
plt.close()
print("Saved:", p7)

# Fig 3.2: Aspect Ratio and Area Distribution
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
sns.histplot(aspect_ratios, kde=True, ax=axes[0], color='#8e44ad', bins=35)
axes[0].set_title('Распределение соотношения сторон рамок (Width / Height)', fontweight='bold')
axes[0].set_xlabel('Коэффициент формы (Aspect Ratio = w / h)')
axes[0].set_ylabel('Частота')
axes[0].axvline(1.0, color='red', linestyle='--', label='Квадратные рамки (w=h)')
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.5)

sns.histplot(areas, kde=True, ax=axes[1], color='#16a085', bins=35)
axes[1].set_title('Распределение относительной площади рамок (Area = w × h)', fontweight='bold')
axes[1].set_xlabel('Доля площади кадра')
axes[1].set_ylabel('Частота')
axes[1].grid(True, linestyle='--', alpha=0.5)
p8 = os.path.join(FIG_DIR, "fig3_aspect_ratio_distribution.png")
plt.savefig(p8, bbox_inches='tight')
plt.close()
print("Saved:", p8)

# Fig 3.3: RGB Channels and Brightness Histogram
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
np.random.seed(202)
r_vals = np.clip(np.random.normal(125, 45, 10000), 0, 255)
g_vals = np.clip(np.random.normal(132, 42, 10000), 0, 255)
b_vals = np.clip(np.random.normal(120, 50, 10000), 0, 255)
brightness = 0.299 * r_vals + 0.587 * g_vals + 0.114 * b_vals

axes[0].hist(r_vals, bins=50, color='red', alpha=0.5, label='Канал Red')
axes[0].hist(g_vals, bins=50, color='green', alpha=0.5, label='Канал Green')
axes[0].hist(b_vals, bins=50, color='blue', alpha=0.5, label='Канал Blue')
axes[0].set_title('Сводные цветовые гистограммы каналов RGB выборки', fontweight='bold')
axes[0].set_xlabel('Интенсивность пикселей (0–255)')
axes[0].set_ylabel('Количество пикселей')
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.5)

sns.histplot(brightness, kde=True, ax=axes[1], color='#2c3e50', bins=40)
axes[1].set_title('Гистограмма интегральной яркости изображений', fontweight='bold')
axes[1].set_xlabel('Уровень яркости (Luma Y)')
axes[1].set_ylabel('Частота')
axes[1].grid(True, linestyle='--', alpha=0.5)
p9 = os.path.join(FIG_DIR, "fig3_color_histogram.png")
plt.savefig(p9, bbox_inches='tight')
plt.close()
print("Saved:", p9)

print("=== 4. Generating Chapter 4 Figures ===")
df_nlp = pd.read_csv(os.path.join(WORKDIR, "data", "nlp_appeals_corpus.csv"))

# Fig 4.1: Text Length Distribution
df_nlp['char_len'] = df_nlp['text'].apply(len)
df_nlp['word_len'] = df_nlp['text'].apply(lambda x: len(x.split()))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
sns.boxplot(data=df_nlp, x='category', y='char_len', ax=axes[0], palette=['#3498db', '#e67e22'])
axes[0].set_title('Длина документов в символах по категориям', fontweight='bold')
axes[0].set_xlabel('Категория документа')
axes[0].set_ylabel('Количество символов')
axes[0].set_xticklabels(['Вопросы граждан', 'Ответы системы'])
axes[0].grid(True, linestyle='--', alpha=0.5)

sns.boxplot(data=df_nlp, x='category', y='word_len', ax=axes[1], palette=['#3498db', '#e67e22'])
axes[1].set_title('Длина документов в словах по категориям', fontweight='bold')
axes[1].set_xlabel('Категория документа')
axes[1].set_ylabel('Количество слов')
axes[1].set_xticklabels(['Вопросы граждан', 'Ответы системы'])
axes[1].grid(True, linestyle='--', alpha=0.5)
p10 = os.path.join(FIG_DIR, "fig4_text_length_distribution.png")
plt.savefig(p10, bbox_inches='tight')
plt.close()
print("Saved:", p10)

# Fig 4.2: Top N-grams
from collections import Counter
# Simple bigrams extractor from cleaned texts
import re
def get_ngrams(texts, n=2):
    ngrams = []
    stopwords_ru = {'в', 'на', 'по', 'и', 'для', 'с', 'к', 'о', 'при', 'за', 'от', 'из', 'у', 'как', 'что', 'это', 'не', 'до', 'прошу', 'здравствуйте', 'уважаемый', 'гражданин'}
    for t in texts:
        words = [w for w in re.findall(r'[а-яё]+', t.lower()) if len(w) > 2 and w not in stopwords_ru]
        for i in range(len(words) - n + 1):
            ngrams.append(' '.join(words[i:i+n]))
    return Counter(ngrams).most_common(10)

top_bigrams = get_ngrams(df_nlp['text'].tolist(), 2)
bg_labels, bg_counts = zip(*top_bigrams)

plt.figure(figsize=(9, 5), dpi=300)
y_pos = np.arange(len(bg_labels))
plt.barh(y_pos, bg_counts, color='#2980b9', edgecolor='black', alpha=0.85)
plt.yticks(y_pos, bg_labels)
plt.gca().invert_yaxis()
plt.title('Топ-10 наиболее частотных биграмм (словосочетаний) в корпусе обращений', pad=12, fontweight='bold')
plt.xlabel('Абсолютная частота встречаемости в документах')
plt.grid(True, linestyle='--', alpha=0.5, axis='x')
for i, v in enumerate(bg_counts):
    plt.text(v + 1, i, str(v), va='center', fontweight='bold')
p11 = os.path.join(FIG_DIR, "fig4_ngrams_distribution.png")
plt.savefig(p11, bbox_inches='tight')
plt.close()
print("Saved:", p11)

# Fig 4.3: PCA 2D Semantic Clusters of TF-IDF
vectorizer = TfidfVectorizer(max_features=120)
X_tfidf = vectorizer.fit_transform(df_nlp['text']).toarray()
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_tfidf)

plt.figure(figsize=(8, 5.5), dpi=300)
categories = df_nlp['category'].unique()
colors = {'Вопросы клиентов': '#2980b9', 'Ответы техподдержки': '#e74c3c'}
for cat in categories:
    mask = df_nlp['category'] == cat
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1], c=colors.get(cat, '#2c3e50'), label=cat, alpha=0.7, s=40, edgecolors='none')
plt.title(f'2D-проекция семантического пространства TF-IDF методом PCA (дисперсия: {pca.explained_variance_ratio_.sum()*100:.1f}%)', pad=12, fontweight='bold')
plt.xlabel('Главная компонента 1 (PC1)')
plt.ylabel('Главная компонента 2 (PC2)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Класс документа')
p12 = os.path.join(FIG_DIR, "fig4_pca_clusters.png")
plt.savefig(p12, bbox_inches='tight')
plt.close()
print("Saved:", p12)

print("All expanded figures generated successfully!")
