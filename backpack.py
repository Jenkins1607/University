def GoPack(items, dp, W):
    for row, value in enumerate(items.values()):
        price = value['price']
        cells = value['cells']

        for limit_cells in range(1, W + 1):
            col = limit_cells - 1 # для корректной итерации по dp

            if row == 0:
                dp[row][col] = 0 if cells > limit_cells else price
            else:
                prev_price = dp[row - 1][col]
                if cells > limit_cells:
                    dp[row][col] = prev_price # предыдущее значение
                else:
                    used = 0 if col-cells < 0 else dp[row - 1][col-cells]

                    res = max(prev_price, price + used)
                    dp[row][col] = res
        
    return dp[N-1][W-1]

def main():
    N = int(input("Введите кол-во предметов: "))
    W = int(input("Введите вместимость рюкзака: ")) 

    # Создание пула предметов с инфой о них
    items = {}
    for row in range(N):
        key = chr(97 + row)  # генерируем ключи 'a', 'b', 'c', ...
        price = int(input(f"Введите цену {row + 1}-го предмета: "))
        cells = int(input(f"Введите объем {row + 1}-го предмета: "))
                                                                    
        items[key] = {'price': price, 'cells': cells}

    # инициализация таблицы для решения задачи
    dp = [[0 for _ in range(W)] for _ in range(N)]

    res = GoPack(items, dp, W)

    print(f"Оптимальная сумма: {res}")

main()
