import openpyxl
from openpyxl.styles import Font
import pandas as pd

def export_excel(results):
    df = pd.DataFrame(results)

    filename = "screening_results.xlsx"
    df.to_excel(filename, index=False)

    wb = openpyxl.load_workbook(filename)
    ws = wb.active

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(filename)
    return filename
