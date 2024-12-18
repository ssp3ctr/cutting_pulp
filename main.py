import pulp

# Входные данные
shapes = [(300, 400), (100, 100), (100, 100), (100, 100), (100, 100), (100, 100), (100, 100), (100, 100), (100, 100), (100, 100), (100, 100)]  # Прямоугольные фигуры (ширина, высота)
sheet_width = 1000  # Ширина листа
sheet_height = 2000  # Высота листа
n_sheets = 25  # Максимальное количество листов

# Модель
model = pulp.LpProblem("CuttingOptimization", pulp.LpMinimize)

# Переменные для координат каждой фигуры на каждом листе
x_vars = pulp.LpVariable.dicts("x", (range(len(shapes)), range(n_sheets)), 0, sheet_width, cat="Continuous")
y_vars = pulp.LpVariable.dicts("y", (range(len(shapes)), range(n_sheets)), 0, sheet_height, cat="Continuous")

sheet_used = pulp.LpVariable.dicts("SheetUsed", range(n_sheets), 0, 1, cat="Binary")

# Целевая функция - минимизация количества используемых листов
model += pulp.lpSum(sheet_used)

# Ограничения на каждую фигуру - она должна быть размещена на одном из листов
for i, shape in enumerate(shapes):
    model += pulp.lpSum([sheet_used[k] for k in range(n_sheets)]) == 1

# Ограничения на размещение фигур в пределах листов
for i, (w, h) in enumerate(shapes):
    for k in range(n_sheets):
        # Ограничение по ширине и высоте для каждой фигуры
        model += x_vars[i][k] + w <= sheet_width
        model += y_vars[i][k] + h <= sheet_height

# Ограничения на то, что фигуры не должны перекрываться
for i, (w1, h1) in enumerate(shapes):
    for j, (w2, h2) in enumerate(shapes):
        if i != j:
            for k in range(n_sheets):
                model += (x_vars[i][k] + w1 <= x_vars[j][k]) | (x_vars[j][k] + w2 <= x_vars[i][k]) | \
                         (y_vars[i][k] + h1 <= y_vars[j][k]) | (y_vars[j][k] + h2 <= y_vars[i][k])

# Решаем задачу
model.solve()

# Вывод решения
for i, shape in enumerate(shapes):
    for k in range(n_sheets):
        if pulp.value(x_vars[i][k]) is not None:
            print(f"Фигура {i} размещена на листе {k} в координатах ({pulp.value(x_vars[i][k])}, {pulp.value(y_vars[i][k])})")
