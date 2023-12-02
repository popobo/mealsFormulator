import parse_foods_excel as pf
import parse_order_excel as po
import random
import copy

foodItems = pf.read_food_items_from_excel("采购单.xlsx", "食材明细")
orderItems = po.parse_order_excel("采购单.xlsx", "报餐情况")

# 统计肉类数量
totalMeatQty = 0.0
totalVegetableQty = 0.0

meatItems = []
vegetableItems = []

kindOfMeat = 0
kindOfVegetable = 0

peopleCount = 0

averageMeatQty = 0.0
averageVegetableQty = 0.0

for f in foodItems:
    if f.category == pf.Category.MEAT:
        totalMeatQty = totalMeatQty + f.quantity
        meatItems.append(f)
    if f.category == pf.Category.VEGETABLE:
        totalVegetableQty = totalVegetableQty + f.quantity
        vegetableItems.append(f)

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
print("人均肉量：", averageMeatQty)
print("人均菜量：", averageVegetableQty)

def is_float_zero(num):
    return abs(num) < 1e-6  # 使用一个非常小的阈值来判断是否接近于0

# 去掉数量为0的食材
def filterFoodItems():
    global kindOfMeat
    global kindOfVegetable
    for i in meatItems:
        if is_float_zero(i.quantity):
            print("remove: ", i.name)
            meatItems.remove(i)
    for i in vegetableItems:
        if is_float_zero(i.quantity):
            print("remove: ", i.name)
            vegetableItems.remove(i)
    kindOfMeat = len(meatItems)
    kindOfVegetable = len(vegetableItems)
    

# 生成今日菜单
def getTodayFood(count, items, avr) -> list[pf.FoodItem]:
    # 今天要有几种食材，随机
    kinds = len(items)
    todayKinds= random.randint(1, kinds)
    # 每种食材的数量
    averageQtyToday = (count * avr) / todayKinds
    # 选出几种食材
    todayItems = []
    tempItems = items[:]
    for i in range(0, todayKinds):
        item = tempItems[random.randint(0, len(tempItems) - 1)]
        # 已选中删除掉，防止再次选中
        tempItems.remove(item)
        foodItem = copy.copy(item)
        # 减去对应的数量
        if averageQtyToday > item.quantity:
            foodItem.quantity = item.quantity
            item.quantity = 0
        else:
            foodItem.quantity = item.quantity
            item.quantity = item.quantity - averageQtyToday
        foodItem.totalPrice = foodItem.quantity * foodItem.price
        todayItems.append(foodItem)
    return todayItems
    

totalCost = 0.0
for o in orderItems:
    print(o.date)
    todayCount = o.breakfast + o.lunch + o.dinner
    
    todayMeat = getTodayFood(todayCount, meatItems, averageMeatQty)
    todayVegetable = getTodayFood(todayCount, vegetableItems, averageVegetableQty)
    
    todayFoods = todayMeat + todayVegetable
    foodString = ""
    foodCost  = 0.0
    for food in todayFoods:
        foodString = foodString + food.name + '、'
        foodCost = foodCost + food.totalPrice
    
    totalCost = totalCost + foodCost
    print(o.date, " | ", foodString, " | ", foodCost)
    
    
    filterFoodItems()

print("totalCost: ", totalCost)
    
pass