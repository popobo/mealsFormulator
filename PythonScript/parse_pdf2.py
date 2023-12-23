import pdfplumber
import parse_foods_excel as pf
from fractions import Fraction
from openpyxl import Workbook

NAME_INDEX = 0
KIND_INDEX = 1
UNIT_INDEX = 2
QUANTITY_INDEX =3
PRICE_INDEX = 4

MEAT_FOOD = ["肉及肉制品", "海水产品", "淡水产品", "畜禽产品"]
VEGETABLE_FOOD = ["食用菌", "蔬菜", "油料", "豆制品", "其他食品", "薯豆加工品", "蔬菜加工品", "方便食品"]
SEASONING = ["调味品", "植物油", "乳制品"]
MAIN_FOOD = ["谷物加工品"]
TOTAL_FOOD = MEAT_FOOD + VEGETABLE_FOOD + SEASONING + MAIN_FOOD

headers = ["菜名",  "种类", "单位", "数量", "单价"]

def getFoodListFromPdf(pdfPath: str):
    wb = Workbook()
    ws = wb.active
    pdf = pdfplumber.open("采购发票.pdf")
    foodList = []
    for page in pdf.pages:
        tables = page.extract_table()
        rows = tables[1][0].split("\n")

        row_index = 1
        for r in rows:
            newRowList = r.split(" ")
            tempList = newRowList[NAME_INDEX].split('*')
            del newRowList[NAME_INDEX]
            for e in tempList:
                if e != '':
                    newRowList.insert(NAME_INDEX, e)
            print(newRowList)
            if len(newRowList) > QUANTITY_INDEX:
                if newRowList[KIND_INDEX] in TOTAL_FOOD:
                    
                    category = pf.Category.MEAT
                    if newRowList[KIND_INDEX] in MEAT_FOOD:
                        category = pf.Category.MEAT
                    if newRowList[KIND_INDEX] in VEGETABLE_FOOD:
                        category = pf.Category.VEGETABLE
                    if newRowList[KIND_INDEX] in MAIN_FOOD:
                        category = pf.Category.MAIN
                    if newRowList[KIND_INDEX] in SEASONING:
                        category = pf.Category.SEASONING
                    
                    for i, value in enumerate(newRowList):
                        if i == KIND_INDEX:
                            value = category.value
                        if i > PRICE_INDEX:
                            break
                        ws.cell(row=row_index, column=i + 1, value=value)
                    
                    row_index = row_index + 1
                    food = pf.FoodItem(name=newRowList[NAME_INDEX], unit=pf.Unit.from_string(newRowList[UNIT_INDEX]), price=Fraction(newRowList[PRICE_INDEX]), category=category, quantity=Fraction(newRowList[QUANTITY_INDEX]))
                    foodList.append(food)
    wb.save("data.xlsx")
    return foodList


if __name__ == "__main__":
    getFoodListFromPdf("")