
#include "Widget.h"
#include "./ui_Widget.h"
#include <QDebug>
#include <QIntValidator>
#include <QMap>
#include <QRandomGenerator>

static const QMap<int, QString> COL_MAP = {{0, "菜名"},
                                           {1, "价格"},
                                           {2, "数量"}}

Widget::Widget(QWidget * parent)
    : QWidget(parent),
                                ui(new Ui::Widget) {
    ui->setupUi(this);
    ui->foodsTable->setShowGrid(true); // 设置显示格子线
    ui->foodsTable->setSelectionBehavior(
        QAbstractItemView::SelectRows); // 整行选中的方式

    ui->foodsTable->horizontalHeader()->setStyleSheet(
        "QHeaderView::section{background:lightblue;}"); // skyblue设置表头背景色
    ui->foodsTable->setStyleSheet(
        "selection-background-color:lightblue;"); // 设置选中背景色

    ui->foodsTable->setRowCount(30);   // 设置行数
    ui->foodsTable->setColumnCount(2); // 设置列数

    ui->totalLayout->setStretchFactor(ui->foodsTable, 2);
    ui->totalLayout->setStretchFactor(ui->resultEdit, 1);

    QStringList header;
    header << "菜式"
           << "价格";
    ui->foodsTable->setHorizontalHeaderLabels(header);

    // Set random Chinese food names and prices
    QStringList chineseFoods;
    chineseFoods << "宫保鸡丁"
                 << "鱼香肉丝"
                 << "麻婆豆腐"
                 << "回锅肉"
                 << "糖醋排骨"
                 << "酸辣汤"
                 << "麻辣香锅"
                 << "水煮鱼"
                 << "红烧肉"
                 << "蚂蚁上树"
                 << "鱼香茄子"
                 << "干煸豆角"
                 << "宫保虾丁"
                 << "蒜蓉西兰花"
                 << "剁椒鱼头"
                 << "东坡肉"
                 << "麻辣烫"
                 << "糖醋鲤鱼"
                 << "麻辣小龙虾"
                 << "酸菜鱼";

    for (int row = 0; row < 20; ++row) {
        QString food = chineseFoods.at(
            QRandomGenerator::global()->bounded(chineseFoods.size()));
        QString price = QString::number(QRandomGenerator::global()->bounded(
            10, 100)); // Random price between 10 and 99
        QTableWidgetItem *foodItem = new QTableWidgetItem(food);
        QTableWidgetItem *priceItem = new QTableWidgetItem(price);
        ui->foodsTable->setItem(row, 0, foodItem);
        ui->foodsTable->setItem(row, 1, priceItem);
    }

    connect(ui->confiremButton, &QPushButton::clicked, this,
            &Widget::onConfirmButtonClicked);
}

QMap<QString, int> generateMenu(const QMap<QString, int> &mealsMap,
                                int budget) {
    QMap<QString, int> menu;                      // 存储点菜结果
    int totalCost = 0;                            // 当前点菜总价格
    QMap<QString, int> remainingMeals = mealsMap; // 创建剩余菜单的副本

    // 从mealsMap中随机点菜，直到总价格超过预算或所有菜品都点过了
    auto meals = remainingMeals.keys();
    while (totalCost < budget && !remainingMeals.isEmpty()) {
        meals = remainingMeals.keys();
        QString randomMeal = meals.at(
            QRandomGenerator::global()->bounded(remainingMeals.size()));
        int mealPrice = remainingMeals.value(randomMeal);

        // 检查点菜是否超过预算
        if (totalCost + mealPrice <= budget) {
            menu.insert(randomMeal, mealPrice);
            totalCost += mealPrice;
        }

        remainingMeals.remove(randomMeal); // 从剩余菜单中移除已点的菜品
    }

    return menu;
}

void Widget::onConfirmButtonClicked() {
    QMap<QString, int> mealsMap;

    for (int row = 0; row < ui->foodsTable->rowCount(); ++row) {
        QTableWidgetItem *foodItem = ui->foodsTable->item(row, 0); // 0 是食材列
        QTableWidgetItem *priceItem =
            ui->foodsTable->item(row, 1); // 1 是价格列

        // 检查每个单元格是否为空，如果为空则跳过
        if (!foodItem || !priceItem) {
            continue;
        }

        auto priceStr = priceItem->text();

        bool ok = false;
        auto price = priceStr.toInt(&ok);
        if (!ok) {
            ui->resultEdit->setText(
                QString("第 %1 行的价格有问题（不是数字）").arg(row));
            return;
        }

        mealsMap.insert(foodItem->text(), price);
    }

    auto budget = ui->numOfPeoSpin->value() * ui->moEachPeoSpin->value();

    auto result = generateMenu(mealsMap, budget);
    QMap<QString, int>::const_iterator it;
    QString resultStr;
    for (it = result.constBegin(); it != result.constEnd(); ++it) {
        resultStr += it.key() + ":" + QString::number(it.value()) + "\n";
    }
    ui->resultEdit->setText(resultStr);
}

Widget::~Widget() { delete ui; }
