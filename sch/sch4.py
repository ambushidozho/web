import numpy as np 
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.family': "Times New Roman"}) 
plt.rcParams.update({'font.size': 16}) 
import os 
import sys 
dir_ = sys.path[0] 
res = open(os.path.join(dir_,f"result_4.txt"), 'w') #файл для записи 
N = 4 #количество знаков после запятой 
#постановка задачи 
Q = np.array([[22,6],[6,6]]) 
b = np.array([[-2*np.sqrt(10.0)],[6*np.sqrt(10)]]) 
c = -22 
c0 = 100 
Q_g = np.array([[2,0],[0,2]]) 
b_g = np.array([[0],[4]]) 
c_g = -21
n = 2 
i = n + 1 
x0 = np.array([[np.sqrt(10.0)],[0]]) 
epsilon = 10**(-3) #погрешность 
def X(x): 
    return np.array([[x[0]],[x[1]]]) 

def f(x): 
    return (1/2*float(np.dot(np.dot(np.transpose(x),Q),x))+float(np.dot(np.transpose(b),x))+ c)
 
def g(x): 
    return (1/2*float(np.dot(np.dot(np.transpose(x),Q_g),x))+float(np.dot(np.transpose(b_g), x))+c_g)
 
def hessian(x,C):  
    diff_g = np.add(np.dot(Q_g,x),b_g) 
    H1_1 = (2*C)/(g(x)**2)-(2*C*(diff_g[0])**2)/(g(x)**3) 
    H1_2 = (-1)*(2*C*diff_g[0]*diff_g[1])/(g(x)**3) 
    H2_2 = (2*C)/(g(x)**2)-(2*C*(diff_g[1])**2)/(g(x)**3) 
    return np.add(np.array([[H1_1[0],H1_2[0]],[H1_2[0],H2_2[0]]]),Q) 
def grad_f(x,C): 
    return np.add(np.add(np.dot(Q,x),b),(C*np.add(np.dot(Q_g,x),b_g)/(g(x)**2))) 
def f_k(x_,C_): 
    return f(x_)-C_/g(x_) 
#константы и функции для построения графика 
left = -8
rigth = 8
bottom = -10
top = 6
x1, x2 = np.mgrid[left-0.5:rigth+0.5:0.01,bottom-0.5:top+0.5:0.01] 
zg = 11*x1**2+3*x2**2+6*x1*x2-2*np.sqrt(10)*(x1-3*x2)-22 
zg_g = (x1-0)**2+(x2+2)**2-5**2
zg_b = zg-(c0/(zg_g))
def graph(label,x,fx): #функция построения графика 
    fig, ax = plt.subplots() 
    ax.set_xlabel("x1") 
    ax.set_ylabel("x2") 
    fig.set_figwidth(10) 
    fig.set_figheight(10) 
    ax.contour(x1, x2, zg_b, colors = 'green',linewidths=1, linestyles = 'solid')     
    ax.contour(x1, x2, zg_g, levels = [0], colors = 'red',linewidths=1, linestyles = 'solid') 
    ax.contour(x1, x2, zg_b, levels = [f_k(x0,c0)],colors = 'blue',linewidths=0.5, linestyles = 'dashed') 
    #ax.contour(x1, x2, zg_b, levels = 100,colors = 'black',linewidths=1, linestyles = 'dashed') 
    #ax.contour(x1, x2, zg, levels = sorted(fx),colors = 'black',linewidths=0.8, linestyles = 'solid') 
    #ax.clabel(cs) 
    #ax.axis([-8, 10, -10, 8]) 
    ax.axis([left, rigth, bottom, top]) 
    xg = [] 
    yg = [] 
    for i in range(len(x)): 
        xg.append(float(x[i][0][0])) 
        yg.append(float(x[i][1][0])) 
    ax.plot(xg, yg, color = 'purple',lw=3) 
    #ax.plot(xg[-1], yg[-1],color = 'r', marker='o', markersize=3, markeredgecolor="black") 
    #plt.show() 
    plt.grid(linestyle = (0, (5, 10))) 
    plt.savefig(os.path.join(dir_,f"4_{label}.png"), format = 'png') 
def write(k,x,fx,C,s,*args): #запись данных в файл 
    if len(args) == 0: 
        t = f'{k:7}\t[{np.round(x[k][0][0],N):7},{np.round(x[k][1][0],N):7}]\t{np.round(fx[k] ,N):7}\t{np.round(C[k],N):7}\t{np.round(s,N):7}' 
    else: 
        t = f'{k:7}\t[{np.round(x[k][0][0],N):7},{np.round(x[k][1][0],N):7}]\t{np.round(fx[k] ,N):7}\t{np.round(C[k],N):7}\t{np.round(args[0],N):7}\t{np.round(s,N):7}' 
    print(t) 
    res.write(t + '\n') 
label = f'Метод барьерных функций, Метод Ньютона' 
print(label) 
res.write(label + '\n') 
k = 0 
C = [c0] 
x = [x0] 
fx = [f(x0)] 
k = 1 
C.append(C[k-1]*0.5) 
#fx.append(f(x[k])-C[k]/g(x[k])) 
x.append(np.subtract(x[k-1],np.dot(np.linalg.inv(hessian(x[k- 1],C[k])),(grad_f(x[k-1],C[k]))))) 
fx.append(f(x[k])) 
write(k,x,fx,C,np.linalg.norm(np.negative(grad_f(x[k],C[k])))) 
while np.linalg.norm(np.negative(grad_f(x[k],C[k]))) > epsilon: 
    k+=1 
    C.append(C[k-1]*0.5) 
    x.append(np.subtract(x[k-1],np.dot(np.linalg.inv(hessian(x[k- 1],C[k])),(grad_f(x[k-1],C[k]))))) 
    fx.append(f(x[k])) 
    write(k,x,fx,C,np.linalg.norm(np.negative(grad_f(x[k],C[k])))) 
graph(label,x,fx) 
label = f'Метод барьерных функций, Метод градиентного спуска с дроблением шага' 
print(label) 
res.write(label + '\n') 
k = 0 
omega = 0.8 
gamma = 0.5 
C = [c0] 
x = [x0] 
W = [0] 
kappa = [0,1] 
fx = [f(x0)] 
k = 1 
C.append(C[k-1]*0.9) #0.9 
W.append(np.negative(grad_f(x[k-1],C[k]))) 
x.append(np.add(x[k-1],np.dot(kappa[k],W[k]))) #рекурентное соотношение 
while (f_k(x[k-1],C[k]) - f_k(x[k],C[k]))  < (omega*kappa[k]*(np.linalg.norm(W[k]))**2): 
    kappa[k] *= gamma 
    x[k] = (np.add(x[k-1],np.dot(kappa[k],W[k]))) #рекурентное соотношение 
fx.append(f(x[k])) 
write(k,x,fx,C,np.linalg.norm(np.subtract(x[k],x[k-1])),kappa[k]) 
while np.linalg.norm(np.subtract(x[k],x[k-1])) > epsilon:      
    k+=1 
    C.append(C[k-1]*0.9) 
    kappa.append(kappa[k-1]) 
    W.append(np.negative(grad_f(x[k-1],C[k]))) 
    x.append(np.add(x[k-1],np.dot(kappa[k],W[k]))) #рекурентное соотношение 
    while (f_k(x[k-1],C[k]) - f_k(x[k],C[k])) < (omega*kappa[k]*(np.linalg.norm(W[k]))**2): 
        kappa[k] *= gamma 
        x[k] = (np.add(x[k-1],np.dot(kappa[k],W[k]))) #рекурентное соотношение     
    fx.append(f(x[k])) 
    write(k,x,fx,C,np.linalg.norm(np.subtract(x[k],x[k-1])),kappa[k]) 
graph(label,x,fx) 
label = 'Метод барьерных функций, Метод исчерпывающего спуска' 
print(label) 
res.write(label + '\n') 
k = 0 
x = [x0] 
W = [0] 
C = [c0] 
kappa = [0] 
fx = [f(x[0])] 
k = 1 
C.append(C[k-1]*0.9) 
W.append(np.negative(grad_f(x[k-1],C[k]))) #антиградиент 
while (np.linalg.norm(W[k]))>epsilon: #условие остановки 
    kappa.append((np.linalg.norm(W[k])**2)/(np.vdot(np.dot(Q,W[k]),W[k]))) 
# формула исчерпывающего спуска 
    x.append(np.add(x[k-1],np.dot(kappa[k],W[k]))) #рекурентное соотношение     
    fx.append(f(x[k])) #значение функции 
    k += 1 
    C.append(C[k-1]*0.9) 
    W.append(np.negative(grad_f(x[k-1],C[k]))) #антиградиент 
    write(k-1,x,fx,kappa,np.linalg.norm(W[k])) 
graph(label,x,fx) 
res.close() 
input('Готово') 