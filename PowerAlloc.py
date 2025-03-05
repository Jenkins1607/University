def allocation(Y, N, F, H):
    
    # таблица для хранения максимального объема продукции 
    dp = [ [0 for _ in range(Y + 1)] for _ in range(N + 1)]
    
    for i in range(1, N + 1):
        for y in range(Y + 1):
            dp[i][y] = dp[i - 1][y]
            
            for x in range(y + 1):
                if H[i-1](x) < y:
                    dp[i][y] = max(dp[i][y], dp[i - 1][y - H[i - 1](x)] + F[i - 1](x))
    
    return dp

def main():
    while True:
        N = 4 # Число предприятий 
        Y = int(input("Введите кол-во единиц ресурса: ")) # Кол-во единиц некоторого ресурса

        F = [
        lambda x: x*15,
        lambda x: x*12,
        lambda x: x*14,
        lambda x: x*22
        ]

        H = [
        lambda x: x,
        lambda x: x*2,
        lambda x: x*4,
        lambda x: x*3
        ]


        res = allocation(Y, N, F, H)
        print("Результат-Матрица: ", end="\n")
        for row in res:
            for elem in row:
                print(str(elem).ljust(3), end=" ")
            print()

        print()

        print(f"Максимальный объем продукции: {res[N][Y]}")

main()
