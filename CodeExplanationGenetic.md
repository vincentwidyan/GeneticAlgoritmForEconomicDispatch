# Code Explanation -- Genetic Algorithm 
Method using Genetic Algorithm with Lamda Search Based for Equation Economic Dispatch with Piecewise Function Characteristic

## Initialization Power Unit Parameter
Parameter for Power Unit such as Power output, IHR, Demand, Cost Unit, and Tolerance

    p = np.array([[100, 200, 300, 400], [150, 275, 390, 450], [130, 260, 430,500],[170,300,450,600]], dtype=np.float64)
    ihr = np.array([[7000, 8200, 8900, 11000], [7500, 7700, 8100, 8500],[7300,8300,9000,10000],[7100,8300,8800,10300]], dtype=np.float64)
    demand = 1200 #Daya yang ingin dibangkitkan
    costUnit = np.array([1.6, 2.1, 1.8, 2.2], dtype=np.float64) #Cost Pembangkitan,
    tol = 0.01 #Toleransi angka
    
    
## Initialization Genetic Parameter
Parameter for Genetic Algorithm such as Popluation number, Retain rate, Mutate rate, and random select

    count=100 #Banyaknya populasi, Sebaiknya di atas 10
    retain=0.4 #Nilai probabilitas individu di seleksi dalam populasi
    random_select=0.7 #Nilai probabilitas individu yang terbuang di masukan kembali ke populasi --> Genetic Diversity
    mutate=0.4 #Nilai probabilitas terjadi mutasi pada individu

## Evolve Function
Function for handling population after being created. There are many process here such as Retain, Random Select, and Mutate and Cross Over between invidual

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
    
## Individu and Population Function
Generating individu and population

    def individual(lenght,min,max):
        return [random.uniform(min,max) for x in range(lenght)]#

    def population(count, lenght, min, max):
        return [individual(lenght,min,max) for x in range (count)]
        
## Fitness and Grade Function
Calculate fitness of every individual then Grade them out of some population

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
            
            
 
 # Main Function -- Generating Population and Looping for best fitness

    temp_lamda=population(count,nGen,min_lam,max_lam) #Membentuk populasi
    fitness_history=[grade(temp_lamda, demand)] #nilai awal populasi
    Generation=0

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
