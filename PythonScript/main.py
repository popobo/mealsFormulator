import parse_foods_excel as pf
import parse_order_excel as po
import parse_config_excel as pc
import write_result_excel as wre
import random
import copy
import math
from fractions import Fraction
from typing import List

foodItems = pf.read_food_items_from_excel("采购单.xlsx", "食材明细")
orderItems = po.parse_order_excel("采购单.xlsx", "报餐情况")
meatConfig = pc.read_config_from_excel("采购单.xlsx", "参数设置", 0)
vegetableConfig = pc.read_config_from_excel("采购单.xlsx", "参数设置", 1)
otherConfig = pc.read_config_from_excel("采购单.xlsx", "参数设置", 2)

totalMeatQty = Fraction()
totalVegetableQty = Fraction()
totalOtherQty = Fraction()

meatItems = []
vegetableItems = []
otherItems = []
seasoningItems = []

kindOfMeat = 0
kindOfVegetable = 0
kindOfOther = 0

peopleCount = 0

averageMeatQty = Fraction()
averageVegetableQty = Fraction()
averageOtherQty = Fraction()

# 去掉数量为0的食材
def filterFoodItems():
    global kindOfMeat
    global kindOfVegetable
    global kindOfOther
    for i in meatItems:
        if i.quantity == 0:
            meatItems.remove(i)
    for i in vegetableItems:
        if i.quantity == 0:
            vegetableItems.remove(i)
    for i in otherItems:
        if i.quantity == 0:
            otherItems.remove(i)
    kindOfMeat = len(meatItems)
    kindOfVegetable = len(vegetableItems)
    kindOfOther = len(otherItems)

def getTodayMealKinds(count, config):
    if count < 3:
        return config.initialValue
    return (int)(config.initialValue + config.mealsKindsStep * math.ceil((count - 3) / config.peopleCountStep))

# 生成今日菜单
def getTodayFood(todayKinds, count, items, avr) -> List[pf.FoodItem]:
    if len(items) == 0:
        return []
    # 每种食材的数量
    averageQtyToday = (count * avr) / todayKinds
    # 选出几种食材
    todayItems = []
    tempItems = items[:]
    for i in range(0, todayKinds):
        if len(tempItems) == 0:
            break
        item = tempItems[random.randint(0, len(tempItems) - 1)]
        # 已选中删除掉，防止再次选中
        tempItems.remove(item)
        foodItem = copy.copy(item)
        # 减去对应的数量
        if averageQtyToday > item.quantity:
            foodItem.quantity = item.quantity
            item.quantity = 0
        else:
            foodItem.quantity = averageQtyToday
            item.quantity = item.quantity - averageQtyToday
        foodItem.totalPrice = foodItem.quantity * foodItem.price
        item.totalPrice = item.quantity * item.price
        todayItems.append(foodItem)
    return todayItems

for f in foodItems:
    if f.category == pf.Category.MEAT:
        totalMeatQty = totalMeatQty + f.quantity
        meatItems.append(f)
    if f.category == pf.Category.VEGETABLE:
        totalVegetableQty = totalVegetableQty + f.quantity
        vegetableItems.append(f)
    if f.category == pf.Category.OTHER:
        totalOtherQty = totalOtherQty + f.quantity
        otherItems.append(f)

# 肉的种类个数
kindOfMeat = len(meatItems)

# 蔬菜种类个数
kindOfVegetable = len(vegetableItems)
        
# 计算人次
for o in orderItems:
    peopleCount = peopleCount + o.breakfast + o.lunch + o.dinner

print("肉类总量：", totalMeatQty)
print("蔬菜总量：", totalVegetableQty)
print("总人次：", peopleCount)

# 计算这个月的人均肉量和菜量
averageMeatQty = totalMeatQty / peopleCount
averageVegetableQty = totalVegetableQty / peopleCount
averageOtherQty = totalOtherQty / peopleCount
print("人均肉量：", averageMeatQty)
print("人均菜量：", averageVegetableQty)
print("人均其他食材量：", averageOtherQty)

result = []
totalCost = 0.0
randomDayBuySeasoning = random.randint(0, len(orderItems) - 1)
for i, o in enumerate(orderItems):
    todayFoods = []
    if i == len(orderItems) - 1:
        todayFoods = meatItems + vegetableItems + otherItems
    else:
        todayCount = o.breakfast + o.lunch + o.dinner
        todayKinds = getTodayMealKinds(todayCount)
        
        kinds = todayKinds / 3
        meatKinds = kinds
        if todayKinds % 3 != 0:            
            meatKinds = meatKinds + 1
        todayMeat = getTodayFood(meatKinds, todayCount, meatItems, averageMeatQty)
        todayVegetable = getTodayFood(kinds, todayCount, vegetableItems, averageVegetableQty)
        todayOther = getTodayFood(kinds, todayCount, otherItems, averageOtherQty)
        todayFoods = todayMeat + todayVegetable + todayOther

    foodString = ""
    foodCost  = Fraction()
    for food in todayFoods:
        foodString = foodString + food.name + '、'
        foodCost = foodCost + food.totalPrice
    
    totalCost = totalCost + foodCost
    
    result.append(wre.Result(o.date, foodString, float(foodCost)))
    print(o.date, " | ", foodString, " | ", float(foodCost))
    
    filterFoodItems()
    
wre.write_result("采购单.xlsx", "result", result)

print("totalCost: ", totalCost)
