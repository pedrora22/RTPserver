import random

LOSS_RATE = 0.1  # 10%

if random.random() < LOSS_RATE:
    print("Pacote perdido")
    continue
