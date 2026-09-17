import sys
import os

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# 1. Load Data
print("="*60)
print("[1/5] Loading CTU-13 dataset (Attack & Normal traffic)...")
t0 = time.time()
df_att = pd.read_csv('CTU13_Attack_Traffic.csv')
df_norm = pd.read_csv('CTU13_Normal_Traffic.csv')
print(f" - Attack Flows (Botnet): {len(df_att):,}")
print(f" - Normal Flows: {len(df_norm):,}")

df = pd.concat([df_att, df_norm], ignore_index=True)
if 'Unnamed: 0' in df.columns:
    df.drop(columns=['Unnamed: 0'], inplace=True)

# Shuffle
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
print(f" - Total NetFlows: {len(df):,}")

# 2. Preprocess
print("\n[2/5] Preprocessing & Splitting Train/Test (80% / 20%)...")
X = df.drop(columns=['Label'])
y = df['Label']
feature_names = list(X.columns)

# Clean inf and nan
X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f" - Train set: {len(X_train):,} flows")
print(f" - Test set: {len(X_test):,} flows")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Train Models
print("\n[3/5] Training Machine Learning Models...")
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=15, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
}

results = {}
preds = {}
probs = {}
fitted_models = {}

for name, model in models.items():
    t_start = time.time()
    if name == 'Logistic Regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
    
    train_time = time.time() - t_start
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    results[name] = {
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1-Score': f1,
        'ROC-AUC': auc,
        'Train Time (s)': train_time
    }
    preds[name] = y_pred
    probs[name] = y_prob
    fitted_models[name] = model
    print(f" -> {name:20s} | Acc: {acc*100:.2f}% | F1: {f1:.4f} | Recall: {rec:.4f} | Time: {train_time:.2f}s")

# 4. Save Models
os.makedirs('saved_models', exist_ok=True)
os.makedirs('output_charts', exist_ok=True)
joblib.dump(fitted_models['Random Forest'], 'saved_models/random_forest_botnet.pkl')
joblib.dump(scaler, 'saved_models/scaler.pkl')
joblib.dump(feature_names, 'saved_models/feature_names.pkl')
print("\n[4/5] Saved best model (Random Forest) to saved_models/")

# 5. Plotting Evaluation Figures
print("\n[5/5] Exporting evaluation charts (PNG)...")

# Chart 1: Metrics comparison
metrics_df = pd.DataFrame(results).T[['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']]
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
metrics_df.plot(kind='bar', ax=ax, width=0.75, colormap='viridis')
plt.title('Comparison of ML Models for Botnet Detection (CTU-13 Dataset)', fontsize=13, fontweight='bold', pad=15)
plt.ylabel('Score (0.0 - 1.0)', fontsize=11)
plt.xlabel('Algorithms', fontsize=11)
plt.xticks(rotation=0, fontsize=10, fontweight='bold')
plt.ylim(0.85, 1.01)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig('output_charts/1_metrics_comparison.png')
plt.close()
print(" -> Exported: output_charts/1_metrics_comparison.png")

# Chart 2: Confusion Matrix for Random Forest
cm = confusion_matrix(y_test, preds['Random Forest'])
fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
cax = ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.85)
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(x=j, y=i, s=f"{cm[i, j]:,}", va='center', ha='center', size='large', weight='bold',
                color='white' if cm[i, j] > cm.max()/2 else 'black')

plt.title('Confusion Matrix - Random Forest', fontsize=12, fontweight='bold', pad=20)
fig.colorbar(cax)
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Normal (0)', 'Botnet (1)'], fontsize=10)
ax.set_yticklabels(['Normal (0)', 'Botnet (1)'], fontsize=10)
plt.xlabel('Predicted Label', fontsize=11, labelpad=10)
plt.ylabel('True Label', fontsize=11, labelpad=10)
plt.tight_layout()
plt.savefig('output_charts/2_confusion_matrix_rf.png')
plt.close()
print(" -> Exported: output_charts/2_confusion_matrix_rf.png")

# Chart 3: ROC Curve comparison
fig, ax = plt.subplots(figsize=(7.5, 6), dpi=300)
for name in models.keys():
    fpr, tpr, _ = roc_curve(y_test, probs[name])
    auc_val = results[name]['ROC-AUC']
    ax.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.4f})", linewidth=2)

ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random Guess (AUC = 0.5000)')
plt.title('ROC Curves (Receiver Operating Characteristic)', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('False Positive Rate', fontsize=11)
plt.ylabel('True Positive Rate', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', fontsize=10)
plt.tight_layout()
plt.savefig('output_charts/3_roc_curves.png')
plt.close()
print(" -> Exported: output_charts/3_roc_curves.png")

# Chart 4: Top 15 Feature Importances (Random Forest)
rf_model = fitted_models['Random Forest']
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1][:15]
top_features = [feature_names[i] for i in indices]
top_importances = importances[indices]

fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
y_pos = np.arange(len(top_features))
ax.barh(y_pos, top_importances[::-1], align='center', color='#1f77b4', edgecolor='#0f3a5a')
ax.set_yticks(y_pos)
ax.set_yticklabels(top_features[::-1], fontsize=10)
ax.set_xlabel('Feature Importance Score', fontsize=11)
plt.title('Top 15 Network Features for Botnet Detection', fontsize=12, fontweight='bold', pad=15)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('output_charts/4_feature_importance_rf.png')
plt.close()
print(" -> Exported: output_charts/4_feature_importance_rf.png")

# Output text summary
res_df = pd.DataFrame(results).T
print("\n" + "="*60)
print("EVALUATION SUMMARY TABLE (For Report & Slides):")
print("="*60)
print(res_df.to_string())
print("="*60)
print(f"Finished in: {time.time()-t0:.2f} seconds.")
