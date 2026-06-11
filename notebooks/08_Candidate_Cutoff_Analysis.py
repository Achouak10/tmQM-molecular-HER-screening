import pandas as pd
import re
from collections import Counter

# === Step 1: Load the files ===
# Replace with your actual file paths
cutoff_df = pd.read_excel("tmQM after cut-off.xlsx")  # Filtered 111 candidates
tmqm_df = pd.read_excel("tmQM_y.xlsx")               # Original full dataset

# Ensure Sr. No. columns are integer for accurate merging
cutoff_df['Sr. No.'] = cutoff_df['Sr. No.'].astype(int)
tmqm_df['Sr. No.'] = tmqm_df['Sr. No.'].astype(int)

# Merge to add CSD_code and Stoichiometry
merged_df = pd.merge(
    cutoff_df,
    tmqm_df[['Sr. No.', 'CSD_code', 'Stoichiometry']],
    on='Sr. No.',
    how='left'
)

# === Step 2: Define transition metals and analyze stoichiometry ===
transition_metals = [
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
    "La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Ac", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn"
]

def extract_transition_metals(stoich, metals):
    found = []
    for metal in metals:
        if metal in stoich:
            found.append(metal)
    return found

# Apply function
merged_df['Transition_Metals'] = merged_df['Stoichiometry'].astype(str).apply(
    lambda x: extract_transition_metals(x, transition_metals)
)

# Count frequency
metal_counter = Counter()
for metals in merged_df['Transition_Metals']:
    metal_counter.update(metals)

# Convert to DataFrame for summary
metal_summary_df = pd.DataFrame(metal_counter.items(), columns=['Transition Metal', 'Frequency'])
metal_summary_df = metal_summary_df.sort_values(by='Frequency', ascending=False)

# === Save both results ===
merged_df.to_excel("Filtered_HER_Candidates_with_CSD.xlsx", index=False)
metal_summary_df.to_excel("Transition_Metal_Frequency_Summary.xlsx", index=False)

# Optional: Display
print("Top Transition Metals:")
print(metal_summary_df.head())

