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

# 买肉类的次数
totalBuyMeatCount = 0
# 买素菜的次数
totalBuyVegetableCount = 0
# 买其他的次数
totalBuyOtherCount = 0
# 买主食(大米)的次数
BUY_MAIN_COUNT = 3

totalMeatQty = Fraction()
totalVegetableQty = Fraction()
totalOtherQty = Fraction()

meatItems = []
vegetableItems = []
otherItems = []
solidItems = []
mainItems = []

def getTodayMealKinds(count, config):
    if count < 3:
        return config.initialValue
    return (int)(config.initialValue + config.mealsKindsStep * math.ceil((count - 3) / config.peopleCountStep))

for o in orderItems:
    totalBuyMeatCount = totalBuyMeatCount + getTodayMealKinds(o.totalCount, meatConfig)
    totalBuyVegetableCount = totalBuyVegetableCount + getTodayMealKinds(o.totalCount, vegetableConfig)
    totalBuyOtherCount = totalBuyOtherCount + getTodayMealKinds(o.totalCount, otherConfig)

# 平均每次买多少
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
    if f.category == pf.Category.SEASONING:
        solidItems.append(f)
    if f.category == pf.Category.MAIN:
        mainItems.append(f)
    
averageBuyMeatQty = totalMeatQty / totalBuyMeatCount
averageBuyVegetableQty = totalVegetableQty / totalBuyVegetableCount
averageBuyOtherQty = totalOtherQty / totalBuyOtherCount

print("买肉类的次数: ", totalBuyMeatCount, " 平均每次买多少: ", float(averageBuyMeatQty))
print("买素菜的次数: ", totalBuyVegetableCount, " 平均每次买多少: ", float(averageBuyVegetableQty))
print("买其他的次数: ", totalBuyOtherCount, " 平均每次买多少: ", float(averageBuyOtherQty))

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


def getTodayFood(todayKinds, items, avr) -> List[pf.FoodItem]:
    if len(items) == 0:
        return []
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
        if avr > item.quantity:
            foodItem.quantity = item.quantity
            item.quantity = 0
        else:
            foodItem.quantity = avr
            item.quantity = item.quantity - avr
        foodItem.totalPrice = foodItem.quantity * foodItem.price
        item.totalPrice = item.quantity * item.price
        todayItems.append(foodItem)
    return todayItems

result = []
totalCost = 0
orderItems = po.sort_meals_by_total_cost(orderItems)

resultMap: [int, List[pf.FoodItem]] = {}
    
# 优化下把人次多的拿出来先选择
for o in orderItems:
    todayMeatKinds = getTodayMealKinds(o.totalCount, meatConfig)
    todayVegetableKinds = getTodayMealKinds(o.totalCount, vegetableConfig)
    todayOtherKinds = getTodayMealKinds(o.totalCount, otherConfig)
    
    todayBuyMeatItems = getTodayFood(todayMeatKinds, meatItems, averageBuyMeatQty)
    todayBuyVegetableItems = getTodayFood(todayVegetableKinds, vegetableItems, averageBuyMeatQty)
    todayBuyOtherItems = getTodayFood(todayOtherKinds, otherItems, averageBuyOtherQty)
    
    todayFoods = todayBuyMeatItems + todayBuyVegetableItems + todayBuyOtherItems
    
    resultMap[o.date] = todayFoods
    
    filterFoodItems()

# 将剩余的肉和蔬菜平均分配下
for m in meatItems:
    # print(m.name, "剩余", float(m.quantity))
    tempItems = []
    for key, value in resultMap.items():
        for f in value:
            if m.name == f.name:
                tempItems.append(f)
                break
    averageQty = m.quantity / len(tempItems)
    for f in tempItems:
        f.quantity = f.quantity + averageQty
        f.totalPrice = f.quantity * f.price
    m.quantity = 0
    m.totalPrice = 0

for v in vegetableItems:
    # print(v.name, "剩余", float(v.quantity))
    tempItems = []
    for key, value in resultMap.items():
        for f in value:
            if v.name == f.name:
                tempItems.append(f)
                break
    averageQty = v.quantity / len(tempItems)
    for f in tempItems:
        f.quantity = f.quantity + averageQty
        f.totalPrice = f.quantity * f.price
    v.quantity = 0
    v.totalPrice = 0

# 随机挑一天买调料
for s in solidItems:
    key = random.choice(list(resultMap.keys()))
    value = resultMap[key]
    value.append(s)

# 大米每个月买3次
for m in mainItems:
    averageQty = m.quantity / BUY_MAIN_COUNT
    for i in range(BUY_MAIN_COUNT):
        key = random.choice(list(resultMap.keys()))
        value = resultMap[key]
        foodItem = copy.copy(m)
        foodItem.quantity = foodItem.quantity / 3
        foodItem.totalPrice = foodItem.quantity * foodItem.price
        value.append(foodItem)
        
for key in sorted(resultMap):
    foodString = ""
    foodCost  = Fraction()
    for food in resultMap[key]:
        foodString = foodString + food.name + '、'
        foodCost = foodCost + food.totalPrice
    
    totalCost = totalCost + foodCost
    
    result.append(wre.Result(key, foodString, float(foodCost)))
    print(key, " | ", foodString, " | ", float(foodCost))
    
    print("total: ", float(totalCost))
    
wre.write_result("采购单.xlsx", "result", result)
