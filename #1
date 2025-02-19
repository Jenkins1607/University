def jump(N,k, paths):

    paths[0] = 1 # 1 способ добраться до 0-й ступеньки 

    for i in range(1, N + 1):
        for j in range(1, k + 1):
            if (i - j) >= 0:
                paths[i] += paths[i - j]

    return paths[N]

def main():
    N = int(input("Введите кол-во ступеней: "))
    k = 2 #может перепрыгнуть не более двух ступенек (макс длина прыжка)

    paths = [0] * (N + 1) # массив количества способов добраться до i-й ступеньки 
    
    result = jump(N,k, paths)

    print(f"Ways count is: {result}")

main()
