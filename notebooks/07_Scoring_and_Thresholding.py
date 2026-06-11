import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load filtered data
df = pd.read_excel("Promising_Materials_Selected.xlsx")

# Copy to avoid modifying original
df_scored = df.copy()

# Features to score
features = ['HL_Gap', 'Dipole_M', 'Molecular Size', 'MND', 'q']

# Standardize features
scaler = StandardScaler()
scaled = scaler.fit_transform(df_scored[features])
scaled_df = pd.DataFrame(scaled, columns=features)

# Invert HL_Gap (low is better)
scaled_df['HL_Gap'] = -scaled_df['HL_Gap']

# Penalize q (neutrality preferred)
scaled_df['q'] = -scaled_df['q'].abs()

# Compute composite score
scaled_df['Score'] = scaled_df.mean(axis=1)

# Merge scores back
df_scored['Score'] = scaled_df['Score']

# Sort by score
df_scored_sorted = df_scored.sort_values(by='Score', ascending=False)

# Export to Excel
df_scored_sorted.to_excel("Ranked_Materials.xlsx", index=False)
print("Saved to Ranked_Materials.xlsx")

import matplotlib.pyplot as plt

# Plot histogram of scores
plt.figure(figsize=(8, 5))
plt.hist(df_scored_sorted['Score'], bins=100, color='skyblue', edgecolor='black')
plt.axvline(x=0, color='gray', linestyle='--', label='Mean/Median')
plt.axvline(x=1, color='red', linestyle='--', label='Top performer threshold')
plt.axvline(x=0.5, color='orange', linestyle='--', label='Good candidate threshold')

plt.title('Distribution of Composite Scores')
plt.xlabel('Score')
plt.ylabel('Number of Materials')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Filter and export materials with Score > 0.5 (good candidate threshold)
top_candidates = df_scored_sorted[df_scored_sorted['Score'] > 0.5]

# Save to Excel
top_output_path = "C:/Users/achou/K-means/Top_Candidates_Score_Above_0.5.xlsx"
top_candidates.to_excel(top_output_path, index=False)

top_output_path
