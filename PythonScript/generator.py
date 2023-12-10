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

totalMeatQty = Fraction()
totalVegetableQty = Fraction()
totalOtherQty = Fraction()

meatItems = []
vegetableItems = []
otherItems = []

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

resultMap: [str, List[pf.FoodItem]] = {}
while(len(meatItems) != 0 or len(vegetableItems) != 0 or len(otherItems) != 0):
    for o in orderItems:
        todayMeatKinds = getTodayMealKinds(o.totalCount, meatConfig)
        todayVegetableKinds = getTodayMealKinds(o.totalCount, vegetableConfig)
        todayOtherKinds = getTodayMealKinds(o.totalCount, otherConfig)
        
        todayBuyMeatItems = getTodayFood(todayMeatKinds, meatItems, averageBuyMeatQty)
        todayBuyVegetableItems = getTodayFood(todayVegetableKinds, vegetableItems, averageBuyMeatQty)
        todayBuyOtherItems = getTodayFood(todayOtherKinds, otherItems, averageBuyOtherQty)
        
        todayFoods = todayBuyMeatItems + todayBuyVegetableItems + todayBuyOtherItems
        if o.date in resultMap:
            tempFoods = resultMap[o.date]
            for tf in tempFoods:
                for tdf in todayFoods:
                    if tf.name == tdf.name:
                        tf.quantity = tf.quantity + tdf.quantity
                        tf.totalPrice = tf.totalPrice + tdf.totalPrice
                        break
            for tdf in todayFoods:
                i = 0
                for tf in tempFoods:
                    i = i + 1
                    if tf.name == tdf.name:
                        break
                    if i == len(tempFoods):
                        tempFoods.append(tdf)
        else:
            resultMap[o.date] = todayFoods
        
        filterFoodItems()

result = []
totalCost = 0

for key, value in resultMap.items():
    foodString = ""
    foodCost  = Fraction()
    
    for food in value:
        foodString = foodString + food.name + '、'
        foodCost = foodCost + food.totalPrice

    totalCost = totalCost + foodCost

    result.append(wre.Result(o.date, foodString, float(foodCost)))
    print(o.date, " | ", foodString, " | ", float(foodCost))

print("totalCost: ", float(totalCost))