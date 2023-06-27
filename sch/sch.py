import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.family': "Times New Roman"})
plt.rcParams.update({'font.size': 16}) 
import os 
import sys 
dir_ = sys.path[0] 
res = open(os.path.join(dir_,f"result.txt"), 'w') 
#постановка задачи 
Q = np.array([[22,6],[6,6]]) 
b = np.array([[-2*np.sqrt(10.0)],[6*np.sqrt(10)]]) 
c = -22 
x0 = np.array([[np.sqrt(10.0)],[0]]) 
epsilon = 10**(-3) #погрешность 

def X(x): 
    return np.array([[x[0]],[x[1]]]) 

def f(x): 
    return (1/2*float(np.dot(np.dot(np.transpose(x),Q),x))+float(np.dot(np.transpose(b),x))+ c) 

#константы и функции для построения графика 
left = -2
rigth = 6
bottom = -7.5
top = 2.5
x1, x2 = np.mgrid[left-0.5:rigth+0.5:0.01,bottom-0.5:top+0.5:0.01] 
zg = 11*x1**2+3*x2**2+6*x1*x2-2*np.sqrt(10)*(x1-3*x2)-22 

def graph(label,x,fx): #функция построения графика 
    fig, ax = plt.subplots() 
    ax.set_xlabel("x1") 
    ax.set_ylabel("x2") 
    fig.set_figwidth(10) 
    fig.set_figheight(10) 
    fx = list(set(fx)) 
    ax.contour(x1, x2, zg, colors = 'blue',linewidths=1, linestyles = 'solid')    
    ax.contour(x1, x2, zg, levels = sorted(fx),colors = 'coral',linewidths=1, linestyles = 'solid') 
    ax.axis([left, rigth, bottom, top]) 
    xg = [] 
    yg = [] 
    for i in range(len(x)): 
        xg.append(float(x[i][0][0])) 
        yg.append(float(x[i][1][0])) 
    ax.plot(xg, yg, color = 'purple',lw=3) 
    plt.grid(linestyle = (0, (5, 10))) 
    plt.show() 
    plt.savefig(os.path.join(dir_,f"1_{label}.png"), format = 'png') 


def write(k,x,fx,kappa,grad_norm): #запись данных в файл 
    n = 4 #знаков после запятой 
    t = f'{k:7}\t[{np.round(x[k][0][0],n):7},{np.round(x[k][1][0],n):7}]\t{np.round(fx[k] ,n):7}\t{np.round(kappa[k],n):7}\t{np.round(grad_norm,n):7}' 
    print(t) 
    res.write(t + '\n') 

label = 'Метод исчерпывающего спуска'
print(label) 
res.write(label + '\n') 
k = 0 
x = [x0] 
W = [0] 
kappa = [0] 
fx = [f(x[0])] 
k = 1 
W.append(np.negative(np.add(np.dot(Q,x[k-1]),b))) #антиградиент 
while (np.linalg.norm(W[k]))>epsilon: #условие остановки 
    kappa.append((np.linalg.norm(W[k])**2)/(np.vdot(np.dot(Q,W[k]),W[k]))) 
# формула исчерпывающего спуска 
    x.append(np.add(x[k-1],np.dot(kappa[k],W[k]))) #рекурентное соотношение    
    fx.append(f(x[k])) #значение функции 
    k += 1 
    W.append(np.negative(np.add(np.dot(Q,x[k-1]),b))) #антиградиент 
    write(k-1,x,fx,kappa,np.linalg.norm(W[k])) 
graph(label,x,fx) 
label = 'Метод Флетчера-Ривса' 
print(label) 
res.write(label + '\n') 
k = 0 
x = [x0] 
W = [0] 
kappa = [0] 
gamma = [0] 
p = [0] 
fx = [f(x[0])] 
k = 1 
W.append(np.negative(np.add(np.dot(Q,x[k-1]),b))) #антиградиент
while (np.linalg.norm(W[k]))>epsilon: #условие остановки 
    if k == 1: 
        p.append(W[k]) 
    else: 
        gamma.append((np.linalg.norm(W[k],2)**2)/(np.linalg.norm(W[k-1],2)**2))        
        p.append(np.add(np.dot(gamma[k-1],p[k-1]),W[k])) #вектор направления спуска 
    kappa.append((np.vdot(W[k],p[k]))/(np.vdot(np.dot(Q,p[k]),p[k]))) 
    x.append(np.add(x[k-1],np.dot(kappa[k],p[k]))) #рекурентное соотношение 
    fx.append(f(x[k])) #значение функции 
    k += 1 
    W.append(np.negative(np.add(np.dot(Q,x[k-1]),b))) #антиградиент 
    write(k-1,x,fx,kappa,np.linalg.norm(W[k])) 
graph(label,x,fx) 

label = 'Метод Двидона-Флетчера-Пауэлла' 
print(label) 
res.write(label + '\n') 
k = 0 
W = [0]  
kappa = [0] 
grad_norm = [0] 
x = [x0] 
fx = [f(x[0])] 
p = [0] 
A = [0] 
k += 1 
W.append(np.negative(np.add(np.dot(Q,x[k-1]),b))) #антиградиент 
while (np.linalg.norm(W[k]))>epsilon: #условие остановки 
    if k == 1: 
        p.append(W[k]) 
        A.append(np.eye(2)) 
    else: 
        delta_x = np.subtract(x[k-1],x[k-2]) 
        delta_W = np.subtract(W[k],W[k-1]) 
        delta_A = np.subtract(np.negative(np.divide( 
            np.dot(delta_x, np.transpose(delta_x)),
            np.vdot(delta_W,delta_x))),             
            np.divide( 
            np.dot(np.dot(np.dot(A[k- 1],delta_W),
                          np.transpose(delta_W)),np.transpose(A[k-1])), 
            np.vdot(np.dot(A[k-1],delta_W),delta_W))) 
        A.append(np.add(A[k-1],delta_A))  
        p.append(np.dot(A[k],W[k])) #вектор направления спуска 
    kappa.append((np.vdot(W[k],p[k]))/(np.vdot(np.dot(Q,p[k]),p[k]))) 
    x.append(np.add(x[k-1],np.dot(kappa[k],p[k]))) #рекурентное соотношение 
    grad_norm.append(np.linalg.norm(W[k]))  #норма градиента 
    fx.append(f(x[k])) #значение функции 
    k += 1 
    W.append(np.negative(np.add(np.dot(Q,x[k-1]),b))) #антиградиент 
    write(k-1,x,fx,kappa,np.linalg.norm(W[k])) 
graph(label,x,fx) 
res.close() 
input('Готово') 