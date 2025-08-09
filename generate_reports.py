from reportlab.pdfgen import canvas
import pandas as pd
import os
import math  # for isnan check

# Ensure reports folder exists
if not os.path.exists('reports'):
    os.makedirs('reports')

# Load CSV
recipients = pd.read_csv('recipients.csv')

for _, row in recipients.iterrows():
    filename = row['report_file']
    name = row['name']

    # Skip if filename is missing or NaN
    if pd.isna(filename) or filename.strip() == '':
        print(f"⚠️ Skipping {name} because report_file is missing!")
        continue

    # Generate PDF
    c = canvas.Canvas(filename)
    c.drawString(100, 750, f"Hello {name},")
    c.drawString(100, 730, "Here is your personalized report.")
    c.drawString(100, 710, "This report is auto-generated using Python.")
    c.save()

    print(f"✅ Report generated: {filename}")
