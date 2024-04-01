''' Пространственное распределение давления по зоне выстрела
из статьи  DOI:10.3390/ma14081878
'''
# 3-D версия
from math import *
import matplotlib.pyplot as plt
import numpy as np

# если нужна будет работа с экселем
from openpyxl import Workbook   

# Исходные данные
P_peak = 10  # pressure in GPa
R = 0.5   #spot radius in mm
HEL = 0.5 #до какого момента имеет смысл считать
SampleHeight = 0    #высота пятна

r = 10   #на сколько строим функцию, по идее должна зависеть от R

# функция распределения
def functionPress(x, y):
    return P_peak * exp(- ((x ** 2 + y ** 2) / (2 * R ** 2)))

y = np.arange(-r, r, 0.08)
x = np.arange(-r, r, 0.08)

X, Y, P = [], [], []
for x_iter in x:
    for y_iter in y:
        if functionPress(x_iter, y_iter) >= HEL:
            P.append(functionPress(x_iter, y_iter))
            X.append(x_iter)
            Y.append(y_iter)

Z = [SampleHeight for i in range(len(X))]   # вообще говоря это не обязательно

#*********** генерация текстового документа *********
file1 = open("D:\вуз\Нирс\питон\График давления для Ансис\PessureXYZ.txt", "w")

file1.write('x\ty\tz\tPressure\n')
for i in range(len(X)):
    file1.write(f'{X[i]}\t{Y[i]}\t{SampleHeight}\t{P[i]*1000}\n')   # давление из ГПа в МПа

file1.close()

#*********** график **********
fig = plt.figure()

# syntax for 3-D projection
ax = plt.axes(projection ='3d')

# plotting
ax.scatter(X, Y, P, color = 'green')
# ax.plot_surface(x_new, y_new2, P, alpha=0.5)

# зона выстрела
tetha = np.linspace(0, 2*np.pi, 100)
x = R * np.cos(tetha)
y = R * np.sin(tetha)
z = [functionPress(x[0], y[0]) for i in range(len(y))]

ax.plot3D(x, y, z, 'red', linewidth = 5) 


ax.set_title('Pressure function')
ax.set_xlabel('X, mm')
ax.set_ylabel('Y, mm')
ax.set_zlabel('Давление, ГПа')

plt.tight_layout()

plt.show()

