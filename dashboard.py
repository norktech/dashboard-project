import openpyxl
import matplotlib.pyplot as plt

wb = openpyxl.load_workbook("produtos.xlsx")
ws = wb.active

nomes = []
precos = []

for row in ws.iter_rows(min_row=2, values_only=True):
    nomes.append(row[0].split(":")[0][:20])
    precos.append(float(row[1].replace("£", "")))

plt.figure(figsize=(14, 6))
plt.barh(nomes, precos, color="steelblue")
plt.xlabel("Preço (£)")
plt.title("NorkTech — Preços de Livros")
plt.tight_layout()
plt.savefig("dashboard.png")
plt.show()
print("Dashboard salvo: dashboard.png")