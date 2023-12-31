import enum
from typing import List
import pandas as pd
from fractions import Fraction

class Unit(enum.Enum):
    JIN = "斤"
    BOTTLE = "瓶"
    PACKAGE = "包"
    PIECE = "块"
    BOX = "箱"
    BUCKET = "桶"
    
    @staticmethod
    def from_string(label):
        for member in Unit:
            if member.value == label:
                return member
        # 如果没有找到匹配的枚举成员，可以抛出一个异常或返回None
        raise ValueError(f"'{label}' is not a valid value for {Unit.__name__}.")

class Category(enum.Enum):
    MEAT = "荤"
    VEGETABLE = "素"
    OTHER = "其他"
    SEASONING = "调"
    MAIN = "主"

class FoodItem:
    def __init__(self, name: str, unit: Unit, quantity: Fraction, price: Fraction, category: Category):
        self.name = name
        self.unit = unit
        self.quantity = quantity
        self.price = price
        self.category = category
        self.totalPrice = quantity * price
        self.averageQty = Fraction()
    
    def print(self):
        print("name:", self.name)
        print("unit:", self.unit)
        print("quantity:", self.quantity)
        print("price:", self.price)
        print("category:", self.category)

def read_food_items_from_excel(file_path: str, sheet_name: str) -> List[FoodItem]:
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    food_items = []
    for _, row in df.iterrows():
        name = row['菜名']
        unit = Unit(row['单位'])
        quantity = row['数量']
        price = row['单价']
        category = Category(row['种类'])

        food_item = FoodItem(name, unit, Fraction(quantity), Fraction(price), category)
        food_items.append(food_item)

    return food_items

if __name__ == "__main__":
    foodItems = read_food_items_from_excel("采购单.xlsx", "食材明细")
    for i in foodItems:
        i.print()