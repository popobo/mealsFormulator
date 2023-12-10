import openpyxl
from typing import List

# 创建一个类来存储报餐情况
class Meal:
    def __init__(self, date, breakfast, lunch, dinner, totalCost):
        self.date = date
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        self.totalCount = breakfast + lunch + dinner
        self.totalCost = totalCost
        
    def print(self):
        print("breakfast", self.breakfast)
        print("lunch", self.lunch)
        print("dinner", self.dinner)
        print("totalCost", self.totalCost)

def is_number(variable):
    return isinstance(variable, (int, float, complex))

# def read_food_items_from_excel(file_path: str, sheet_name: str) -> List[FoodItem]:
def  parse_order_excel(file_path: str, sheet_name: str) -> List[Meal]:
    # 打开 Excel 文件
    workbook = openpyxl.load_workbook(file_path)

    # 选择报餐情况的工作表
    sheet = workbook[sheet_name]
    
    # 解析每一行的报餐情况并存储在相应的类中
    meals = []
    
    parseFlag = False
    for row in sheet.iter_rows(min_row=4, values_only=True):
        date = row[0]
        if is_number(date):
            parseFlag = True
        else:
            parseFlag = False
        if not parseFlag:
            continue
        breakfast = row[1]
        lunch = row[2]
        dinner = row[3]
        totalCost = (breakfast + lunch + dinner) * 10
        meal = Meal(date, breakfast, lunch, dinner, totalCost)
        meals.append(meal)

    # 关闭 Excel 文件
    workbook.close()
    
    return meals
    
if __name__ == "__main__":
    parse_order_excel("采购单.xlsx", "报餐人数")