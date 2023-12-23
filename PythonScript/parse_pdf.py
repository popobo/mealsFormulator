import tabula
from fractions import Fraction
import parse_foods_excel as pf

NAME_INDEX = 0
KIND_INDEX = 1
UNIT_INDEX = 2
AMOUNT_INDEX =3
PRICE_INDEX = 4
QUANTITY_INDEX = 5

MEAT_FOOD = ["肉及肉制品", "海水产品", "淡水产品", "畜禽产品"]
VEGETABLE_FOOD = ["食用菌", "蔬菜", "油料", "豆制品", "其他食品", "薯豆加工品", "蔬菜加工品", "方便食品"]
SEASONING = ["调味品", "植物油", "乳制品"]
MAIN_FOOD = ["谷物加工品"]
TOTAL_FOOD = MEAT_FOOD + VEGETABLE_FOOD + SEASONING + MAIN_FOOD

def print_pdf_tables(file_path):
    # 读取PDF文件中的所有表格
    tables = tabula.read_pdf(file_path, pages='2', multiple_tables=True)
    
    # 遍历所有表格
    foodList = []
    for i, table in enumerate(tables):
        print(f"Table {i+1}:")
        # 遍历表格中的每一行
        for index, row in table.iterrows():
            rowStr = row.to_string(index=False)
            rowList = rowStr.split(' ')
            newRowList = []
            for e in rowList:
                if e != '':
                    newRowList.append(e)
            tempList = newRowList[NAME_INDEX].split('*')
            del newRowList[NAME_INDEX]
            for e in tempList:
                if e != '':
                    newRowList.insert(NAME_INDEX, e)
            print(newRowList)
            if len(newRowList) > QUANTITY_INDEX:
                if newRowList[KIND_INDEX] in TOTAL_FOOD:
                    price = newRowList[PRICE_INDEX][:-1]
                    price = Fraction(price)
                    category = pf.Category.MEAT
                    if newRowList[KIND_INDEX] in MEAT_FOOD:
                        category = pf.Category.MEAT
                    if newRowList[KIND_INDEX] in VEGETABLE_FOOD:
                        category = pf.Category.VEGETABLE
                    if newRowList[KIND_INDEX] in MAIN_FOOD:
                        category = pf.Category.MAIN
                    if newRowList[KIND_INDEX] in SEASONING:
                        category = pf.Category.SEASONING
                    if (newRowList[NAME_INDEX] == "芋头"):
                        pass
                    food = pf.FoodItem(name=newRowList[NAME_INDEX], unit=pf.Unit.from_string(newRowList[UNIT_INDEX]), price=price, category=category, quantity=Fraction(newRowList[QUANTITY_INDEX]))
                    foodList.append(food)
            # if newRowList[KIND_INDEX] in MAIN_FOOD:
            #     food = pf.FoodItem(name=newRowList[NAME_INDEX], unit=pf.Unit.__members__[newRowList[UNIT_INDEX]], price=)
    for f in foodList:
        f.print()
            

# 使用函数打印PDF文件中的表格行
pdf_path = '采购发票.pdf'  # 替换为你的PDF文件路径"
print_pdf_tables(pdf_path)