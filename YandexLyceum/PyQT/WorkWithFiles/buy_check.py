total = 0.0

with open("prices.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 3:
            _, quantity, price = parts
            total += int(quantity) * float(price)

print(f"{total:.2f}")
