import numpy as np 
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.family': "Times New Roman"}) 
plt.rcParams.update({'font.size': 16}) 
import os 
import sys 
dir_ = sys.path[0] 
res = open(os.path.join(dir_,f"result_2.txt"), 'w') #файл для записи
N = 4 #количество знаков после запятой 
#постановка задачи 
Q = np.array([[22,6],[6,6]]) 
b = np.array([[-2*np.sqrt(10.0)],[6*np.sqrt(10)]]) 
c = -22 
n = 2 
x0 = np.array([[np.sqrt(10.0)],[0]]) 
epsilon = 10**(-3) #погрешность 

def X(x): 
    return np.array([[x[0]],[x[1]]]) 

def f(x): 
    return (1/2*float(np.dot(np.dot(np.transpose(x),Q),x))+float(np.dot(np.transpose(b),x))+ c) 

#константы и функции для построения графика 
left = -5
rigth = 10
bottom = -15
top = 5
x1, x2 = np.mgrid[left-0.5:rigth+0.5:0.01,bottom-0.5:top+0.5:0.01] 
zg = 11*x1**2+3*x2**2+6*x1*x2-2*np.sqrt(10)*(x1-3*x2)-22 

def graph(label,x,fx,t): #функция построения графика 
    fig, ax = plt.subplots() 
    ax.set_xlabel("x1") 
    ax.set_ylabel("x2") 
    fig.set_figwidth(10) 
    fig.set_figheight(10) 
    fx_ = [] 

    for k in range(len(x)): 
        for j in range(len(x[k])): 
            try: 
                fx_.append(fx[k][j]) 
            except: 
                pass 
    fx_ = list(set(fx_)) 
    ax.contour(x1, x2, zg, colors = 'red',linewidths=1, linestyles = 'solid') 
    ax.contour(x1, x2, zg, levels = sorted(fx_),colors = 'green',linewidths=1, linestyles = 'solid') 
    ax.axis([left, rigth, bottom, top]) 
    xg = [] 
    yg = [] 
    xg2 = [] 
    yg2 = [] 
    for k in range(len(x)): 
        for j in range(len(x[k])): 
            if t == 2: 
                if j == 0: 
                    xg2.append(float(x[k][j][0][0])) 
                    yg2.append(float(x[k][j][1][0])) 
            xg.append(float(x[k][j][0][0])) 
            yg.append(float(x[k][j][1][0])) 
    #for i in range(1,8): 
# ax.arrow(xg[i-1],yg[i-1],(xg[i]-xg[i-1])/2,(yg[i]-yg[i-1])/2, 
#length_includes_head=True, color='r',  head_width = 0.08) 
    #ax.plot(xg, yg,color = 'r', marker='o', markersize=3, markeredgecolor="black") 
    ax.plot(xg, yg, color = 'black',lw=3) 
    #if t == 2: 
# ax.plot(xg2, yg2,color = 'r', linestyle = '--', linewidth=0.5) 
    #plt.show() 
    plt.grid(linestyle = (0, (5, 10))) 
    plt.savefig(os.path.join(dir_,f"2_{label}.png"), format = 'png') 
label = 'Циклический покоординатный спуск'
print(label) 
res.write(label + '\n') 
k = 0 
j = 0 
e = [np.array([[1],[0]]),np.array([[0],[1]])] 
x = [] 
W = []  
p = [] 
alpha = [] 
fx = [] 
flag = True 
while flag: 
    for j in range(n+1): 
        if j == 0: 
            if k == 0: 
                x.append([x0]) 
            else: 
                x.append([x[k-1][n]]) 
            W.append([]) 
            p.append([]) 
            alpha.append([]) 
            fx.append([]) 
        else: 
            x[k].append(np.add(x[k][j-1],np.dot(alpha[k][j-1],p[k][j-1])))       
        fx[k].append(f(x[k][j])) 
        if j == n: 
            if k != 0: 
                if np.linalg.norm(np.subtract(x[k][j],x[k-1][j])) < epsilon: 
                    flag = False 
                else: 
                    k+=1 
            else: 
                k+=1 
        else: 
            W[k].append(np.negative(np.add(np.dot(Q,x[k][j]),b))) #антиградиент            
            p[k].append(e[j])    #направление спуска 
            alpha[k].append((np.vdot(W[k][j],p[k][j]))/(np.vdot(np.dot(Q,p[k][j]) ,p[k][j])))  
for k in range(len(x)): 
    for j in range(len(x[k])): 
        norm = '-' 
        if k != 0: 
            if j == n: 
                norm = np.round(np.linalg.norm(np.subtract(x[k][j],x[k][0])),N)        
        if j == n: 
             alpha_ = '-' 
        else: 
            alpha_ = np.round(alpha[k][j],N) 
        t = f'{k+1:7}\t{j+1:7}\t[{np.round(x[k][j][0][0],N):7},{np.round(x[k][j][1][0],N):7}] \t{np.round(fx[k][j],N):7}\t{alpha_:7}\t{norm:7}' 
        print(t) 
        res.write(t + '\n') 
graph(label,x,fx,1)      
res.write('\n') 
label = 'Метод Хука-Джипса' 
print(label) 
res.write(label + '\n') 
k = 0 
j = 0 
e = [np.array([[1],[0]]),np.array([[0],[1]])]
x = [] 
W = []  
p = [] 
alpha = [] 
fx = [] 
flag = True 
while flag: 
    for j in range(n+1): 
        if j == 0: 
            if k == 0: 
                x.append([x0])                 
                fx.append([])           
            W.append([]) 
            p.append([]) 
            alpha.append([]) 
        else: 
            x[k].append(np.add(x[k][j-1],np.dot(alpha[k][j-1],p[k][j-1])))         
        fx[k].append(f(x[k][j])) 
        if j == n: 
            p[k].append(np.subtract(x[k][j],x[k][0])) 
            W[k].append(np.negative(np.add(np.dot(Q,x[k][0]),b))) 
            alpha[k].append((np.vdot(W[k][j],p[k][j]))/(np.vdot(np.dot(Q,p[k][j]) ,p[k][j])))  
            x.append([np.add(x[k][0],np.dot(alpha[k][j],p[k][j]))]) 
            k+=1 
            fx.append([f(x[k][0])]) 
            if k != 0: 
                if np.linalg.norm(np.subtract(x[k][0],x[k-1][0])) < epsilon: 
                    flag = False 
                    #write(x,fx,alpha) 
        else: 
            W[k].append(np.negative(np.add(np.dot(Q,x[k][j]),b))) #антиградиент            
            p[k].append(e[j])    #направление спуска 
            alpha[k].append((np.vdot(W[k][j],p[k][j]))/(np.vdot(np.dot(Q,p[k][j]) ,p[k][j])))  
for k in range(len(x)): 
    for j in range(len(x[k])): 
        norm = '-' 
        if k != 0: 
            if j == 0: 
                norm = np.round(np.linalg.norm(np.subtract(x[k][0],x[k-1][0])),N)        
        alpha_ = '-' 
        kappa_ = '-' 
        if j == n: 
            kappa_ = np.round(alpha[k][j],N) 
        elif k != len(x)-1: 
            alpha_ = np.round(alpha[k][j],N) 
        t = f'{k+1:7}\t{j+1:7}\t[{np.round(x[k][j][0][0],N):7},{np.round(x[k][j][1][0],N):7}] \t{np.round(fx[k][j],N):7}\t{alpha_:7}\t{norm:7}\t{kappa_:7}' 
        print(t) 
        res.write(t + '\n') 
graph(label,x,fx,2)    
res.write('\n')    
label = 'Метод Розенброка' 
print(label) 
res.write(label + '\n') 
k = 0 
j = 0 
e = [np.array([[1],[0]]),np.array([[0],[1]])] 
x = [] 
W = []  
p = [] 
alpha = [] 
fx = [] 
flag = True 
while flag: 
    for j in range(n+1): 
        if j == 0: 
            if k == 0: 
                x.append([x0]) 
            else: 
                x.append([x[k-1][n]]) 
            W.append([]) 
            p.append([]) 
            alpha.append([]) 
            fx.append([]) 
        else: 
            x[k].append(np.add(x[k][j-1],np.dot(alpha[k][j-1],p[k][j-1])))        
        fx[k].append(f(x[k][j])) 
        if j == n: 
            p_ = np.subtract(x[k][j],x[k][0]) 
            e[0] = p_ / np.linalg.norm(p_) 
            e[1] = np.array([-e[0][1], e[0][0]]) 
            if k != 0: 
                if np.linalg.norm(np.subtract(x[k][j],x[k-1][j])) < epsilon:                     flag = False 
                else: 
                    k+=1 
            else: 
                k+=1 
        else: 
            W[k].append(np.negative(np.add(np.dot(Q,x[k][j]),b))) #антиградиент            
            p[k].append(e[j])    #направление спуска 
            alpha[k].append((np.vdot(W[k][j],p[k][j]))/(np.vdot(np.dot(Q,p[k][j]) ,p[k][j])))  
for k in range(len(x)): 
    for j in range(len(x[k])): 
        norm = '-' 
        if k != 0: 
            if j == n: 
                norm = np.round(np.linalg.norm(np.subtract(x[k][j],x[k][0])),N)          
        if j == n: 
            alpha_ = '-' 
        else: 
            alpha_ = np.round(alpha[k][j],N) 
        t = f'{k+1:7}\t{j+1:7}\t[{np.round(x[k][j][0][0],N):7},{np.round(x[k][j][1][0],N):7}] \t{np.round(fx[k][j],N):7}\t{alpha_:7}\t{norm:7}' 
        print(t) 
        res.write(t + '\n') 
graph(label,x,fx,1)      
res.write('\n') 
res.close() 
input('Готово') 