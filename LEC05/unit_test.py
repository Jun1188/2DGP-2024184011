import math    
x = 400
y = 300
r = 100
degree = 0
delta = 10
while degree < 360:
    degree += delta
    radian = math.radians(degree)
    x = 400 + r * math.cos(radian)
    y = 300 + r * math.sin(radian)
    print(f"{x}, {y}")