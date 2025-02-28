def way_to_max(N, paths, costs, money_pull):
    money_pull[0] = 0  # на нулевом шаге прибыль 0$
    money_pull[1] = costs[1] # на первом шаге прибыль 1$

    for i in range(2, N + 1):
        if money_pull[i-1] > money_pull[i-2]:
            money_pull[i] = money_pull[i-1] + costs[i] # ++ прибыль
            paths[i] = i - 1 # добавляем индекс в массив путей
        else: 
            money_pull[i] = money_pull[i - 2] + costs[i]
            paths[i] = i - 2 # добавляем индекс в массив путей
    
    return paths, money_pull


def main():
    N = int(input("Введите кол-во ступеней: "))

    money_pull = [0] * ( N + 1) # массив полученной прибыли

    paths = [0] * (N + 1) # массив индексов пути

    costs = [0] * (N + 1) 
    for i in range(1, N + 1):
        costs[i] = int(input(f"Введите прибыль для {i}-й ступени: "))

    res = way_to_max(N, paths, costs, money_pull)

    print(f"Массив путей и приыбыли соответственно: {res}")

main()

# записывать путь по которому он допрыгал но i-ой ступени с макс прибылью
# в массиве должны быть выборы max(f(n-1), f(n-2))
# сделать массив приыбли paths(n)
# с(n) - прибыль за n шагов
