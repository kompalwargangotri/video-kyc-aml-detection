import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create output directory if it doesn't exist
os.makedirs("research_graphs", exist_ok=True)

# Set the style for academic papers
plt.style.use('seaborn-v0_8-paper')
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'securefin.db')

# Fallback path if generated from backend folder
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'database', 'securefin.db')

conn = sqlite3.connect(DB_PATH)

# Graph 1 & 2: AML Live Data

try:
    aml_df = pd.read_sql_query('SELECT amount, risk_score, status FROM aml_decisions', conn)
except Exception as e:
    print(f"No aml decisions found: {e}")
    aml_df = pd.DataFrame()

if not aml_df.empty:
    plt.figure(figsize=(8, 6))

    # Capitalize just in case status strings are capitalized
    aml_df['status'] = aml_df['status'].str.upper()

    palette = {}
    if 'ALLOW' in aml_df['status'].values: palette['ALLOW'] = 'green'
    if 'REVIEW' in aml_df['status'].values: palette['REVIEW'] = 'orange'
    if 'BLOCK' in aml_df['status'].values: palette['BLOCK'] = 'red'

    sns.scatterplot(data=aml_df, x='amount', y='risk_score', hue='status',
                    palette=palette, alpha=0.8, s=80, edgecolors='black')
    plt.axhline(y=40, color='gray', linestyle='--', label='Review Threshold')
    plt.axhline(y=80, color='darkred', linestyle='--', label='Block Threshold')
    plt.title('AML Live Decisions: Amount vs. Risk Score', fontweight='bold')
    plt.xlabel('Transaction Amount')
    plt.ylabel('Risk Score')
    plt.legend(title='Decision Status')
    plt.tight_layout()
    plt.savefig('research_graphs/aml_scatter.png', dpi=300)
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.histplot(data=aml_df, x='risk_score', bins=10, kde=True, color='royalblue')
    plt.axvline(x=40, color='orange', linestyle='--', linewidth=2, label='Review (40+)')
    plt.axvline(x=80, color='red', linestyle='--', linewidth=2, label='Block (80+)')
    plt.title('Live AML Risk Score Distribution', fontweight='bold')
    plt.xlabel('Risk Score')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig('research_graphs/aml_distribution.png', dpi=300)
    plt.close()

# Graph 3: KYC Liveness Confidence comparison

try:
    kyc_df = pd.read_sql_query('SELECT confidence, status FROM kyc_requests', conn)
except Exception as e:
    print(f"No kyc requests found: {e}")
    kyc_df = pd.DataFrame()

if not kyc_df.empty:
    plt.figure(figsize=(8, 5))

    kyc_df['status'] = kyc_df['status'].str.upper()
    palette = {}
    if 'VERIFIED' in kyc_df['status'].values: palette['VERIFIED'] = 'green'
    if 'FAILED' in kyc_df['status'].values: palette['FAILED'] = 'red'

    sns.boxplot(data=kyc_df, x='status', y='confidence', palette=palette)
    plt.title('KYC Confidence vs Verification Status', fontweight='bold')
    plt.ylabel('Confidence (%)')
    plt.xlabel('Status')
    plt.tight_layout()
    plt.savefig('research_graphs/kyc_confidence.png', dpi=300)
    plt.close()

conn.close()
print("Live database graphs updated successfully.")
