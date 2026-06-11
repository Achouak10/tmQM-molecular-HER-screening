import pandas as pd
# Load the uploaded Excel file that already contains the transition metal frequency summary
freq_df = pd.read_excel("Transition_Metal_Frequency_Summary.xlsx")

# Plot the data
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(freq_df['Transition Metal'], freq_df['Frequency'], color='steelblue')
#plt.title("Figure 12. Frequency of Transition Metals in Final HER Candidate Set")
plt.xlabel("Transition Metal")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.tight_layout()
#plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.show()
