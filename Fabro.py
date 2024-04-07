#Fabro
import numpy as np
import matplotlib.pyplot as plt
import math

# задающие параметры:
    # геометрия
diametr = 0.14   # диаметр пятна, cm

    # параметры лазера
Power = 4   # Энергия, Джоули
tay = 60    # длительность импульса, ns
Intensity0 = Power / (tay * np.pi * diametr ** 2 / 4) # GW/cm^2

gamma = 5/3     # адиабатическая что-то там
alpha = 0.25    # подгоночный коэффициент, связанная с долей ионизации

# табличные данные, для титана Ti6Al4V брал от сюда doi: 10.1063/1.1303508
p_w, p_tit = 1, 4.42  #density of water and titan, gram/cm^3 
D_w, D_tit = 1.483, 4.987 # 1.465, 4.987 - or speed of sound (https://www.matweb.com/search/datasheet_print.aspx?matguid=b350a789eda946c6b86a3e4d3c577b39)| 5.2 - speed of shockwave in water and in titan, km/s

# или расчетный метод
E = 114*1e9
PoissonsRatio = 0.33
D_tit_calc = (E / (3 * (1 - 2 * PoissonsRatio) * p_tit / 1000) ) ** 0.5
# print(D_tit_calc)


# shock impedance
Z1 = p_w * D_w * 1e5
Z2 = p_tit * D_tit * 1e5
Z = 2 * Z2 * Z1 / (Z1 + Z2)

# P_peak максимальное значение давления
P_tay = 0.01 * ((alpha * Z * Intensity0) / (2 * alpha + 3)) ** 0.5   #in GPa
# P_tay = 0.01 * (alpha / (2 * alpha + 3)) ** 0.5 * Z ** 0.5 * Intensity0 ** 0.5

P = [0]

# это похоже на какой-то рандом, задание функции до адиабатического охлаждения

# step1 = 2
# step2 = 50
# t1 = np.arange(0, 3*tay, step1)
# t2 = np.arange(3*tay-0.9*step1, 1000, step2)
# time = [t1[i] for i in range(len(t1))] + [t2[i] for i in range(len(t2))]



# def fabPressure(function):
#     for i in range(n):
#         t1 = time[i]
#         # abs(deltaPres - function(t1))
#         t2 = s * (2 * math.log(P_tay / (function(t1)-deltaPres))) ** 0.5
#         time.append(t2)
#         P.append(function(tay - t2))

#         print(P[i] - P[i+1])




# time = np.arange(0, 1000, 5)



def gausPressure(r):
    # s = tay / (2 * pow(2 * math.log(2), 0.5))    
    # R = tay * 0.1
    # return P_tay * np.exp(- (r ** 2 / (2 * R ** 2)))
    #return 1 / (2 * np.pi) ** 0.5 * np.exp (-0.5 * (r) ** 2 )
    #return ((1 / (s * pow(2 * 3.14, 0.5))) * math.exp(-1 * math.pow((r - tay), 2) / (2 * math.pow(s, 2))))
    return P_tay * np.exp(- (r ** 2 / (2 * s ** 2)))

# def fabroPressure():
#     for i in range(1, len(time)):
#         if time[i] < tay:
#             Pressure = gausPressure(tay - time[i])
#             P.append(Pressure)
#         else:   
#             # adiabatic release (Laplace’s law)
#             Pressure = P_tay * (tay / ((gamma + 1) * (time[i] - tay) + tay)) ** (gamma / (gamma + 1))
#             P.append(Pressure)

def adiabaticPressure(t):
    return P_tay * (tay / ((gamma + 1) * (t - tay) + tay)) ** (gamma / (gamma + 1))



deltaPres = 0.1 #точность в GPa
# аргумент time будет строиться постепенно 
time = [0]
P = [0]
n = 25 # кол-во точек
s = tay / (2 * pow(2 * math.log(2), 0.5))

iter = [0]
i = 0
while iter[i] <= tay:
    t1 = iter[i]
    # abs(deltaPres - function(t1))
    # t2 = tay - s * (2 * math.log(P_tay / abs(gausPressure(tay + t1)-deltaPres))) ** 0.5
    t2 = s * (2 * math.log(P_tay / abs(gausPressure(t1)-deltaPres))) ** 0.5
    print(t2)
    iter.append(t2)
    time.insert(1, (t2 * -1) + tay)
    #time.append(# + 60)

    P.insert(1, gausPressure(t2))
    i += 1

time.pop(1)
P.pop(1)
time.append(tay)
P.append(P_tay)
print(time)
# iter = time[-1]
 #len(time) - 1
while time[i] <= 1000 and i <= 100:
    t1 = time[i]
    t2 = tay + (tay * (((-deltaPres + adiabaticPressure(t1)) / P_tay) ** -((gamma + 1) / gamma)) - tay) / (gamma + 1)
    print(time[i])
    time.append(t2)
    P.append(adiabaticPressure(t2))
    i += 1


# print(iter)
time.pop(-1)
P.pop(-1)
time.append(1000)
P.append(adiabaticPressure(1000))
print(len(time))
# print(P)


#*********** график **********
plt.plot(time, P, color = 'green') 
plt.grid()
plt.title('')
plt.show()


# for i in range(len(time)):
    



# fabroPressure()



# #*********** генерация текстовых документов *********
file1 = open("D:\вуз\Гагаринские чтения\режимы обработки\по времени\FabroScale.txt", "w")
file2 = open("D:\вуз\Гагаринские чтения\режимы обработки\по времени\FabroTime.txt", "w")

file2.write('time, ns\n') #\tscalePressure\n')

for i in range(len(time)):
    file1.write(f'{P[i]/P_tay}\n')   
    file2.write(f'{time[i] * 1e-9}\n')   # время из ns в s

file1.close()
file2.close()
