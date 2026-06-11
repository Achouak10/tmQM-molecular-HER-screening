import pandas as pd
import re
input_file = r"C:\Users\achou\datacleaning\csd_extracted_X3.xlsx"  # Replace with your actual filename
df = pd.read_excel(input_file)
def calculate_molecular_size(stoich):
    # Remove any charge indication (+1, -1)
    stoich = re.sub(r'\([\+\-]\d+\)', '', stoich)
    # Extract numbers from the formula (atoms with implicit "1" need to be counted)
    elements = re.findall(r'([A-Z][a-z]?)(\d*)', stoich)
    # Sum atomic counts, treating empty counts as 1
    total_atoms = sum(int(count) if count else 1 for _, count in elements)
    return total_atoms

# Apply function to Stoichiometry column
df['Molecular Size'] = df['Stoichiometry'].apply(calculate_molecular_size)

# Save to a new Excel file
output_file = "csd_with_molecular_size3.xlsx"
df.to_excel(output_file, index=False)

print(f"Molecular sizes calculated and saved to {output_file}")
