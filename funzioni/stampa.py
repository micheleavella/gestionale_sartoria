from openpyxl import load_workbook


def stampa(cliente, data, quantità, capo, commento):
    workbook = load_workbook(filename="dati/template.xlsx")
    sheet = workbook.active

    sheet["A4"].value = cliente.upper()
    sheet["A5"].value = data.strftime("%d/%m/%Y")

    for i in range(len(capo)):
        sheet["A" + str(7 + i)].value = quantità[i]
        sheet["B" + str(7 + i)].value = capo[i]
        sheet["C" + str(7 + i)].value = commento[i]

    workbook.save("dati/out.xlsx")