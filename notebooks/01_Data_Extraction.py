import docx
from docx import Document
import pandas as pd
input_file = r"C:\Users\achou\Downloads\tmQM_X1.docx"
doc = Document(input_file)
csd_lines = [para.text.strip() for para in doc.paragraphs if para.text.strip().startswith("CSD")]
df = pd.DataFrame(csd_lines, columns=["CSD Data"])
output_file = "csd_extracted_lines.xlsx"
df.to_excel(output_file, index=False)
print(f"Extracted {len(csd_lines)} lines starting with 'CSD'. Saved to {output_file}")
