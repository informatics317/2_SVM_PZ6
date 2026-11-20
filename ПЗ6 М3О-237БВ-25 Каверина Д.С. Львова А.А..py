# Задание 1. Поиск палиндрома
def min_deletions_wagner_fischer(s):
    r = s[::-1]
    n = len(s)
    d = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
        d[0][i] = i
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i - 1] == r[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1]) + 1
    return d[n][n] // 2

def restore_palindrome(s):
    n = len(s)
    if n == 0:
        return ""
    p = [[0] * n for _ in range(n)]
    for i in range(n):
        p[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                p[i][j] = p[i + 1][j - 1] + 2
            else:
                p[i][j] = max(p[i + 1][j], p[i][j - 1])
    left, right = 0, n - 1
    first_half, second_half = [], []
    while left <= right:
        if s[left] == s[right]:
            first_half.append(s[left])
            if left != right:
                second_half.append(s[right])
            left += 1
            right -= 1
        elif p[left + 1][right] >= p[left][right - 1]:
            left += 1
        else:
            right -= 1
    return "".join(first_half + second_half[::-1])

def find_deleted(s, result):
    deleted = []
    k = 0
    for i in range(len(s)):
        if k < len(result) and s[i] == result[k]:
            k = k + 1
        else:
            deleted.append((s[i], i + 1))
    return deleted

def is_palindrome(t):
    return t == t[::-1]

s = "ROPEQOR"

print("Задание 1. Поиск палиндрома")
count = min_deletions_wagner_fischer(s)
result = restore_palindrome(s)
print("Исходная строка:", s)
print("Полученный палиндром:", result)
print("Это палиндром:", is_palindrome(result))
print("Количество удалений:", count)
print("Удалённые символы (символ, позиция):", find_deleted(s, result))
print("Проверка: n - длина палиндрома =", len(s) - len(result), ", K =", count)

print()


# Задание 2. Лабиринт
def solve_maze(field):
    n = len(field)
    dp = [[None] * n for _ in range(n)]
    parent = [[None] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if field[i][j] == "#":
                continue

            if i == 0 and j == 0:
                dp[i][j] = field[i][j]
                continue

            candidates = []
            if i > 0 and dp[i - 1][j] is not None:
                candidates.append((dp[i - 1][j], (i - 1, j)))
            if j > 0 and dp[i][j - 1] is not None:
                candidates.append((dp[i][j - 1], (i, j - 1)))

            if not candidates:
                continue

            best_value, best_cell = max(
                candidates, key=lambda item: item[0]
            )
            dp[i][j] = best_value + field[i][j]
            parent[i][j] = best_cell

    if dp[n - 1][n - 1] is None:
        return None, [], dp

    path = []
    i, j = n - 1, n - 1
    while True:
        path.append((i + 1, j + 1))
        if i == 0 and j == 0:
            break
        i, j = parent[i][j]

    path.reverse()
    return dp[n - 1][n - 1], path, dp

def path_to_moves(path):
    moves = ""
    for k in range(1, len(path)):
        if path[k][1] > path[k - 1][1]:
            moves = moves + "R"
        else:
            moves = moves + "D"
    return moves

field = [
    [2, 1, 0, 5, 1],
    [0, "#", 4, "#", 2],
    [3, 2, 7, 1, 0],
    ["#", 1, "#", 3, 4],
    [1, 0, 2, 1, 5]
]

print("Задание 2. Лабиринт")
maximum, path, dp = solve_maze(field)
print("Таблица динамического программирования:")
for row in dp:
    print(row)

if maximum is None:
    print("Маршрут до выхода отсутствует.")
else:
    print("Максимум драгоценностей:", maximum)
    print("Оптимальный маршрут:")
    for cell in path:
        print(cell)

print("Маршрут в виде ходов:", path_to_moves(path))

print()

# Дополнение к заданию
# Поиск всех решений
def build_p(s):
    n = len(s)
    p = [[0] * n for _ in range(n)]
    for i in range(n):
        p[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                p[i][j] = p[i + 1][j - 1] + 2
            else:
                p[i][j] = max(p[i + 1][j], p[i][j - 1])
    return p

def all_palindromes(s, p, left, right):
    if left > right:
        return [""]
    if left == right:
        return [s[left]]
    result = []
    if s[left] == s[right]:
        inner = all_palindromes(s, p, left + 1, right - 1)
        for x in inner:
            result.append(s[left] + x + s[right])
    else:
        if p[left + 1][right] >= p[left][right - 1]:
            for x in all_palindromes(s, p, left + 1, right):
                if x not in result:
                    result.append(x)
        if p[left][right - 1] >= p[left + 1][right]:
            for x in all_palindromes(s, p, left, right - 1):
                if x not in result:
                    result.append(x)
    return result

def all_paths(field, dp, i, j):
    if i == 0 and j == 0:
        return [[(1, 1)]]
    result = []
    if i > 0 and dp[i - 1][j] is not None:
        if dp[i - 1][j] + field[i][j] == dp[i][j]:
            for path in all_paths(field, dp, i - 1, j):
                result.append(path + [(i + 1, j + 1)])
    if j > 0 and dp[i][j - 1] is not None:
        if dp[i][j - 1] + field[i][j] == dp[i][j]:
            for path in all_paths(field, dp, i, j - 1):
                result.append(path + [(i + 1, j + 1)])
    return result

print("Дополнение к заданию")
p = build_p(s)
pals = all_palindromes(s, p, 0, len(s) - 1)
print("Все палиндромы максимальной длины:", pals)
print("Их количество:", len(pals))

maximum, path, dp = solve_maze(field)
n = len(field)
paths = all_paths(field, dp, n - 1, n - 1)
print("Максимум драгоценностей:", maximum)
print("Количество оптимальных маршрутов:", len(paths))
for one in paths:
    print(path_to_moves(one), one)

