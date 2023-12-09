import openpyxl
from typing import List

class Result:
    def __init__(self, date, foodString, cost) -> None:
        self.date = date
        self.foodString = foodString
        self.cost = cost
        
def write_result(filePath: str, sheetName: str, result: List[Result]):
    workbook = openpyxl.load_workbook(filePath)
    
    sheet = workbook.create_sheet(sheetName)
    
    # 写入标题行
    sheet.append(["Date", "Food String", "Cost"])

    # 遍历 Result 列表并写入每个 Result 的属性
    for res in result:
        sheet.append([res.date, res.foodString, res.cost])

    workbook.save(filePath)