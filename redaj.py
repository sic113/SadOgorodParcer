import openpyxl

workbook = openpyxl.load_workbook("vers02.xlsx")

workbook.active=0
worksheet=workbook.active

i = 0
for cell in worksheet['C']:
    i += 1

    try:
        cell.value = (cell.value).replace("вес", "")
        cell.value = (cell.value).strip()

        a = str(cell)
        a = a.replace(">", "")
        a = a.split(".")
        b = a[1]
        print(b)
        worksheet[f'{b}'] = cell.value
        workbook.save('vers02.xlsx')
    except AttributeError:
        print("пустая ячейка")
        worksheet[f'{b}'] = cell.value
        workbook.save('vers02.xlsx')