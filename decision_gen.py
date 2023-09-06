import random

global generations
generations = [] #[time,score]

def gen():
    time = random.randint(1, 10)
    generations.append([time,None])
    return time

def fitnes(score): #score-> actual
    global generations
    generations[-1] = [generations[-1][0],score] #asignamos el score del individuo actual
    i = -1 if len(generations)<2 else -2 #elegimos su generacion anterior, si es la primera se escoge a si misma
    bef_score= generations[i][1] #obtenemos su generacion anteroir
    fit = score-bef_score
    generations[-1] = [generations[-1][0],fit] #cambiamos el score por el fitnes
    return fit  #comparamos la actual con la anterior

def new_gen(parent,this): #generacion anteroir, generacion actual
    global generations
    tolerances = [0.8, 0.3]
    if parent[1] > this[1] and parent[0]<this[0]:#verificamos si el padre tuvo un mayor score y menor tiempo
        time = parent[0] - random.choice(tolerances)
    else:
        time = (this[0]/random.randrange(1,3))/(parent[0]-random.random())
    generations.append([abs(time),None])
    return abs(time)

# player = gen()
# generacion = 0
# while True:
#     score = random.randint(10,30) if player < 20 else  random.randint(0,10)
#     print("-----nuevo----")
#     print(f"player_gen:{player}")
#     print(f"score:{score}")
#     fit = fitnes(score)
#     if fit < 10:
#         if len(generations) < 2: 
#             player = player
#             generations.append([player,score])
#             continue
#         else:    
#             print("generando nuevo individuo")
#             player = new_gen(generations[-2],generations[-1])
#             generacion +=1
            
#     if fit > 20 or generacion > 10: break
#     print("-------New------")
#     print(f"generacion: {generacion}")
#     print(f"fitnes:{fit}  player:{player}")

# print(f"numero de generaciones: {generacion}")
# print(f"las generaciones son {generations}")