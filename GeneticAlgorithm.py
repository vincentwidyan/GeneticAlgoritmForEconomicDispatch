#Genetic Algorithm for Economic Dispatch in Power System

from random import *
import random
import numpy as np
from operator import add
from functools import reduce
import time
start = time.time()
print('\n')
print('*************************************************************')
print('Metode Genetic Algorithm Berbasis Lamda Search untuk Penyelesaian Economic Dispatch')
print('--------- dengan Piecewise Function Characteristic ----------')
print('\n')
print('Vincentius Wahyu W')
print('16/399923/TK/44937')
print('\n')

# Insialisasi Fungsi
print("1. Initialisasi Power Unit Parameter")
p = np.array([[100, 200, 300, 400], [150, 275, 390, 450], [130, 260, 430,500],[170,300,450,600]], dtype=np.float64)
print ("Power each Unit : ", p)
#p = Daya (MW), tiap row menyatakan tiap pembangkit. Tiap Kolom menyatakan tiap breakpoint

ihr = np.array([[7000, 8200, 8900, 11000], [7500, 7700, 8100, 8500],[7300,8300,9000,10000],[7100,8300,8800,10300]], dtype=np.float64)
print("IHR :", ihr)
demand = 1200 #Daya yang ingin dibangkitkan
costUnit = np.array([1.6, 2.1, 1.8, 2.2], dtype=np.float64) #Cost Pembangkitan,
print("Cost Unit : ", costUnit)
tol = 0.01 #Toleransi angka
print("Tolerance value :", tol)
print('\n')

bp = len(ihr[0, :]) #Banyaknya titik segmen grafik piecewise
nGen = len(ihr[:, 0]) #Banyaknya pemabangkit
#print(nGen)


print("2. Initialisasi Genetic Algorithm Parameter")
count=100 #Banyaknya populasi, Sebaiknya di atas 10
retain=0.4 #Nilai probabilitas individu di seleksi dalam populasi
random_select=0.7 #Nilai probabilitas individu yang terbuang di masukan kembali ke populasi --> Genetic Diversity
mutate=0.4 #Nilai probabilitas terjadi mutasi pada individu
print("Poulation number ;", count, " | Retain number : ", retain, " | Random Select Percentage : ", random_select, " | Mutation rate : ", mutate)
print('\n')

lamda = np.zeros(shape=(nGen, bp))
slope = np.zeros(shape=(nGen, bp))
const = np.zeros(shape=(nGen, bp))
temp_slope = np.zeros(shape=(nGen, bp))
temp_constant = np.zeros(shape=(nGen, bp))
one_slope = np.zeros(shape=(1, nGen))
Pow_max= np.zeros(shape=(nGen, 1))
Pow_min= np.zeros(shape=(nGen, 1))
Pow= np.zeros(shape=(count, nGen))

#Menghitung Nilai Slope, Constant dari Fungsi Piecewise tiap Segmen
for j in range(nGen):
    for i in range(bp):
        lamda[j, i] = (ihr[j, i] * costUnit[j]) / 1000

for j in range(nGen):
    for i in range(bp - 1):
        slope[j, i + 1] = (lamda[j, i + 1] - lamda[j, i]) / (p[j, i + 1] - p[j, i])
        const[j, i + 1] = lamda[j, i] - (slope[j, i+1] * p[j, i])

#Menghitung Nilai Maksimum dan Minimum Load tiap Pembangkit
for i in range (nGen):
    Pow_max[i,0]=np.amax(p[i,:])
for i in range(nGen):
    Pow_min[i, 0] = np.amin(p[i, :])
max_lam = np.amax(lamda)
min_lam = np.amin(lamda)

#Exit Jika Permintaan Daya di luar Range
if demand < sum(Pow_min):
    print("Daya Pemabangkitan  kurang dari Technical Minimum Load")
    exit()
elif demand > sum(Pow_max):
    print("Daya Pemabangkitan  lebih dari Technical Maximum Load")
    exit()

#Fungsi Utama
def evolve(pop,demand,retain,random_select,mutate):
    gradeda = [ (fitness(x,demand), x) for x in pop]


    def sortSecond(val):
        return val[0]
    gradeda.sort(key=sortSecond)
    graded = [x[1] for x in gradeda]


    #Individu Selection
    retain_lenght = int(len(graded)*retain)
    parents = graded[:retain_lenght]
    #print('Parent Terpilih :',parents)

    #Genetic Diversity : Mengambil lagi beberapa Individu untuk mencegah local optimum
    for individu in graded[retain_lenght:]:
        if random_select > random.random():
            parents.append(individu)
    #print('Parent setelah ditambah :', parents)

    #Individu Mutation : Mutasi nilai kromosom pada individu
    for individu in parents:
        if mutate > random.random():
            place_to_mutate = randint(0,len(individu)-1)
            individu[place_to_mutate] = random.uniform(min(individu), max(individu))

    #print('Parent hasil mutasi :', parents)

    #CrossOver : Menyilangkan antar individu menjadi individu baru utk mencukupi kembali populasi
    parents_lenght = len(parents)
    desired_lenght = len(temp_lamda) - parents_lenght
    #print('des',desired_lenght)
    children = []
    while len(children) < desired_lenght:
        malenumber = randint(0,parents_lenght-1)
        femalenumber = randint(0, parents_lenght -1)
        if malenumber != femalenumber:
            male = parents[malenumber]
            female = parents[femalenumber]
            half = round(len(male)/2)
            child = male[:half] + female[half:]
            children.append(child)
    parents.extend(children)
    #print('Parent populasi utuh', parents)
    return parents

#############################################################
#Membentuk fungsi individu
def individual(lenght,min,max):
    return [random.uniform(min,max) for x in range(lenght)]#

#Membentuk Populasi : kumpulan individu
def population(count, lenght, min, max):
    return [individual(lenght,min,max) for x in range (count)]

#Rating tiap individu
def fitness(one_slope,demand):
    for i in range(nGen):
        if one_slope[i] <= lamda[i, 0]:
            temp_slope[0,i] = slope[i, 0]
            temp_constant[0,i] = const[i, 0]
        for k in range(bp - 1):
            if (one_slope[i] > lamda[i, k]) & (one_slope[i] <= lamda[i, k + 1]):
                temp_slope[0,i] = slope[i, k + 1]
                temp_constant[0,i] = const[i, k + 1]
        if one_slope[i] > lamda[i, bp - 1]:
            temp_slope[0,i] = slope[i, bp - 1]
            temp_constant[0,i] = const[i, bp - 1]
    for i in range(nGen):
        if temp_slope[0, i] == 0:
            Pow[0, i] = Pow_min[i,0]
        elif (one_slope[i] - temp_constant[0, i]) / temp_slope[0, i] >= Pow_max[i, 0]:
            Pow[0, i] = Pow_max[i, 0]
        else:
            Pow[0, i] = (one_slope[i] - temp_constant[0, i]) / temp_slope[0, i]
    sum=np.sum(Pow)
    return abs(demand-sum)

#Rating/nilai sebuah populasi
def grade(pop, demand):
        summed=reduce(add, (fitness(x, demand) for x in pop),0)
        #print(summed)
        return summed/(len(pop)*1.0)


# Mian Function creating population

temp_lamda=population(count,nGen,min_lam,max_lam) #Membentuk populasi
fitness_history=[grade(temp_lamda, demand)] #nilai awal populasi
Generation=0
#print(fitness_history)


# Looping until fitness function below tolerance

while 1:
    temp_lamda= evolve(temp_lamda, demand, retain, random_select, mutate)

    Generation+=1

    fitness_history.append(fitness(temp_lamda[0], demand))
    if fitness(temp_lamda[0],demand) <=tol:
        break
    if Generation >=500:
        print('Iterasi terhenti di generasi ke-',Generation)
        break



# Find Value

print('Generasi ke :', Generation)
for i in range (nGen):
    print('Nilai lamda Unit ',i+1,' :', temp_lamda[0][i])

fitness(temp_lamda[0],demand)
for i in range (nGen):
    print('Daya Pembangkit Unit' ,i+1,':', Pow[0][i])

print('Daya Pembangkit :', sum(Pow[0]))
end = time.time()
print('Waktu Eksekusi', end - start)