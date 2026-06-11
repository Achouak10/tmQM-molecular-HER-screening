import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 1. Load the dataset (Handling the comma separator)
# Ensure the file is in your directory
df = pd.read_csv('tmQM_y.csv', sep=',', on_bad_lines='skip')

# 2. Select numerical descriptors
# We exclude non-numeric columns like 'CSD_code'
features = [
    'Electronic_E', 'Dispersion_E', 'Dipole_M', 
    'Metal_q', 'HL_Gap (eV)', 'HOMO_Energy', 
    'LUMO_Energy', 'Polarizability'
]

# Drop rows with missing values to ensure clean analysis
X = df[features].apply(pd.to_numeric, errors='coerce').dropna()

# 3. Standardize the Data (Crucial step)
# This ensures that variables with large units (like Energy) don't dominate variables with small units (like Charge).
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Run PCA
pca = PCA()
pca_data = pca.fit_transform(X_scaled)

# 5. Calculate Explained Variance
explained_variance = np.cumsum(pca.explained_variance_ratio_)

# 6. Analyze Loadings (Which features drive each PC?)
loadings = pd.DataFrame(
    pca.components_.T, 
    columns=[f'PC{i+1}' for i in range(len(features))], 
    index=features
)

print("--- Cumulative Variance Explained ---")
print(explained_variance)

print("\n--- Top Contributors (Loadings) ---")
print(loadings.abs().idxmax())  # Returns the feature with the highest impact on each PC

# Optional: Plot the Scree Plot
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='--')
plt.axhline(y=0.90, color='r', linestyle='-', label='90% Variance Threshold')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA Variance Analysis for tmQM Descriptors')
plt.legend()
plt.grid(True)
plt.savefig('pca_variance_plot.png')