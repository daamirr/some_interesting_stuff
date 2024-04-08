''' Пространственное распределение давления по зоне выстрела
из статьи  DOI:10.3390/ma14081878
'''
# 3-D версия
from math import *
import numpy as np
import matplotlib.pyplot as plt

# Исходные данные
Power = 4   # Энергия, Джоули
tay = 60   # длительность импульса, ns


gamma = 5/3     # адиабатическая что-то там
alpha = 0.25    # подгоночный коэффициент, связанная с долей ионизации

# табличные данные, для титана Ti6Al4V брал от сюда doi: 10.1063/1.1303508
p_w, p_tit = 1, 4.42  #density of water and titan, gram/cm^3 
D_w, D_tit = 1.483, 4.987 # 1.465, 4.987 - or speed of sound (https://www.matweb.com/search/datasheet_print.aspx?matguid=b350a789eda946c6b86a3e4d3c577b39)| 5.2 - speed of shockwave in water and in titan, km/s

# shock impedance
Z1 = p_w * D_w * 1e5
Z2 = p_tit * D_tit * 1e5
Z = 2 * Z2 * Z1 / (Z1 + Z2)

R = 0.7   #spot radius in mm
Intensity0 = Power / (tay * np.pi * (2*R/10) ** 2 / 4) # GW/cm^2
P_peak = 0.01 * ((alpha * Z * Intensity0) / (2 * alpha + 3)) ** 0.5 


# P_peak = 2.932  # pressure in GPa
# R = 0.7   #spot radius in mm
HEL = 0 #P_peak * 0.1 #до какого момента имеет смысл считать
SampleHeight = 5    #высота пятна

r = 10   #на сколько строим функцию, по идее должна зависеть от R
delta = 0  #смещение
number_type = 0     #

s = R / 2 / (2 * log(2)) ** 0.5 # в данном случае R это полуширина

# функция распределения по Гауссу
def gausFunctionPress(x, y):
    # return P_peak * exp(- (((x + delta) ** 2 + (y + delta) ** 2) / (2 * R ** 2)))
    return 1 / (s * (2 * pi) ** 0.5) * exp(- (((x + delta) ** 2 + (y + delta) ** 2) / (2 * s ** 2)))

def gausPressure(r):
    return P_peak * np.exp(- (r ** 2 / (2 * s ** 2)))

# def interval(a, b, precision):
#     radius = [a]
#     i = 0
#     while radius[i] <= b and i <= 100:
#         r1 = radius[i]
#         r2 = s * (2 * log(P_peak / abs(gausPressure(r1)-precision))) ** 0.5
#         radius.append(r2)
#         print(r2)
#         # time.insert(1, (t2 * -1) + tay)     # вставляем в начало перед точкой (0,0)
#         # P.insert(1, gausPressure(t2))
#         i += 1
#     return radius

# radius = [0]
# i = 0
# precision = 0.1
# while radius[i] <= 4 and i <= 100:
#     r1 = radius[i]
#     r2 = s * (2 * log(P_peak / abs(gausPressure(r1)-precision))) ** 0.5
#     radius.append(r2)
#     print(r2)
#     # time.insert(1, (t2 * -1) + tay)     # вставляем в начало перед точкой (0,0)
#     # P.insert(1, gausPressure(t2))
#     i += 1

# deltaPres = 0.1
# i = 0
# iterTime = [0]
# time = [0]
# P = [0]
# while iterTime[i] <= R:
#     t1 = iterTime[i]
#     t2 = s * (2 * abs(log(1 / (s * (2 * pi) ** 0.5) / abs(gausFunctionPress(t1, 0)-deltaPres)))) ** 0.5
#     print("t = ", t2)
#     iterTime.append(t2)
#     print(gausFunctionPress(t1, 0) - gausFunctionPress(t2, 0))
#     # time.insert(1, (t2 * -1) + tay)     # вставляем в начало перед точкой (0,0)
#     # P.insert(1, gausPressure(t2))
#     i += 1

# if (x**2 + y**2)
# x = y = interval(-r, r, 0.1)  #0.01
# x = y = iterTime
 #0.01
# x1 = np.arange(-r, -R, 0.15)
# x2 = np.arange(-R, R, 0.05)
# x3 = np.arange(R, r, 0.15)
# # b = [a[i] for i in range(len(a))] + [c[j] for j in range(len(c))]

# x = [i for i in x1] + [i for i in x2] + [i for i in x3]
# y = x


y = np.arange(-r, r+0.05, 0.05).round(3)
x = y

print(x, y)

# angle = np.arange(0, 2 * np.pi, 0.1)

X1, Y1, P1 = [], [], []
X, Y, P = [], [], []

"""
while iter[i] <= tay:
    t1 = iter[i]
    t2 = s * (2 * math.log(P_tay / abs(gausPressure(t1)-deltaPres))) ** 0.5
    print(time[i])
    time.append(t2)
    P.append(adiabaticPressure(t2))
    i += 1
"""
# print(x, y)
for x_iter in x:
    for y_iter in y:
        if (x_iter ** 2 + y_iter ** 2) <= (2*R)**2: #gausFunctionPress(x_iter, y_iter) >= HEL:
            # P1.append(gausFunctionPress(x_iter, y_iter) * 2*R * P_peak)
            # X1.append(x_iter)
            # Y1.append(y_iter)
            P.append(gausFunctionPress(x_iter, y_iter) * 2*R * P_peak)
            X.append(x_iter)
            Y.append(y_iter)

        elif (x_iter ** 2 + y_iter ** 2) <= 4: #gausFunctionPress(x_iter, y_iter) >= HEL:
            P.append(gausFunctionPress(x_iter, y_iter) * 2*R * P_peak)
            X.append(x_iter)
            Y.append(y_iter)

print(max(P))
# print('Было:', '\n',X1, '\n', Y1, '\n')
# modifX = []
# modifY = []
# n = 2
# for j in range(len(X1)-1):
#     dobavkaX = (X1[j] - X1[j+1]) / n
#     dobavkaY = (Y1[j] - Y1[j+1]) / n
#     for i in range(n):
#         NewElem = X1[j] - i * dobavkaX
#         # # X1.insert(i+1, NewElem)
#         modifX.append(NewElem)
#         NewElem = Y1[j] - (i + 0) * dobavkaY
#         # Y1.insert(i+1, NewElem)
#         modifY.append(NewElem)

# modifX = modifY



# modifX.append(X1[-1])
# modifY.append(Y1[-1])
# print('Стало:', '\n', modifX, '\n', modifY, '\n')




# Pmod = []
# for y_iter in modifY:
#     for x_iter in modifX:
#         Pmod.append(gausFunctionPress(x_iter, y_iter) * 2*R * P_peak)

# a = 0
# P_mod2 = [a for i in range(len(modifX))]
# P_mod1 = [2 for i in range(len(X1))]

# print(len(P_mod2), len(modifX), len(modifY))


#*********** 3d график **********
fig = plt.figure()

# syntax for 3-D projection
ax = plt.axes(projection ='3d')

# plotting
ax.scatter(X, Y, P, color = 'green')
# ax.scatter(modifX, modifY, P1, color = 'green')
# ax.scatter(X1, Y1, P_mod1, color = 'blue')

# ax.scatter(modifX, modifY, P_mod2, color = 'red')

# ax.plot_surface(x_new, y_new2, P, alpha=0.5)

# зона выстрела
# tetha = np.linspace(0, 2*np.pi, 100)
# x = R * np.cos(tetha)
# y = R * np.sin(tetha)
# z = [gausFunctionPress(x[0], y[0]) for i in range(len(y))]

# ax.plot3D(x, y, z, 'red', linewidth = 5) 


ax.set_title('Pressure function')
ax.set_xlabel('X, mm')
ax.set_ylabel('Y, mm')
ax.set_zlabel('Давление, ГПа')

plt.tight_layout()

plt.show()

#*********** генерация текстового документа *********D:\вуз\Гагаринские чтения\режимы обработки
# file1 = open("PessureXYZ123.txt", "w")
file1 = open("D:\вуз\Гагаринские чтения\режимы обработки\PessureXYZ.txt", "w")

file1.write('x, mm\ty, mm\tz, mm\tPressure, MPa\n')
for i in range(len(X)):
    file1.write(f'{X[i]}\t{Y[i]}\t{SampleHeight}\t{P[i]*1000}\n')   # давление из ГПа в МПа

file1.close()
