import numpy as np 
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.family': "Times New Roman"})
plt.rcParams.update({'font.size': 16}) 
import os 
import sys 
dir_ = sys.path[0] 
res = open(os.path.join(dir_,f"result_3.txt"), 'w') #файл для записи 
N = 4 #количество знаков после запятой 
#постановка задачи 
Q = np.array([[22,6],[6,6]]) 
b = np.array([[-2*np.sqrt(10.0)],[6*np.sqrt(10)]]) 
c = -22 
n = 2  
i = n+1 

x0 = np.array([[np.sqrt(10.0)],[0]]) 
epsilon = 10**(-3) #погрешность 
def X(x): 
    return np.array([[x[0]],[x[1]]]) 
def f(x): 
    return (1/2*float(np.dot(np.dot(np.transpose(x),Q),x))+float(np.dot(np.transpose(b),x))+ c) 
#константы и функции для построения графика 
left = -2
rigth = 5
bottom = -5
top = 2
x1, x2 = np.mgrid[left-0.5:rigth+0.5:0.01,bottom-0.5:top+0.5:0.01] 
zg = 11*x1**2+3*x2**2+6*x1*x2-2*np.sqrt(10)*(x1-3*x2)-22 
flag = False

def graph(label,x,fx): #функция построения графика 
    fig, ax = plt.subplots() 
    ax.set_xlabel("x1") 
    ax.set_ylabel("x2") 
    fig.set_figwidth(10) 
    fig.set_figheight(10) 
    ax.contour(x1, x2, zg, colors = 'yellow',linewidths=1, linestyles = 'solid')
    if(flag):
       bottom = -6
    ax.axis([left, rigth, -6, top])
    ax.axis([left, rigth, bottom, top])
    xg = [] 
    yg = [] 
    xg_m = [] 
    yg_m = [] 
    ax.plot(x0[0], x0[1], color = 'blue', marker='o', markersize=4, markeredgecolor="black") 
    for k in range(len(x)): 
        xg_m.append(float(x_m[k][0][0])) 
        yg_m.append(float(x_m[k][1][0]))  
        # if k == 0:
        #     ax.plot(x0[0], x0[1], float(x_m[k][0][0]), float(x_m[k][1][0]), color = 'red',lw=15) 
        # else:
        #     ax.plot(float(x_m[k - 1][0][0]), float(x_m[k - 1][1][0]), float(x_m[k][0][0]), float(x_m[k][1][0]), color = 'red',lw=3) 
        ax.plot(float(x_m[k][0][0]), float(x_m[k][1][0]), color = 'blue', marker='o', markersize=4, markeredgecolor="black")
        for j in range(i): 
            xg.append(float(x[k][j][0][0]))
            yg.append(float(x[k][j][1][0]))
        xg.append(float(x[k][0][0][0])) 
        yg.append(float(x[k][0][1][0]))
    ax.plot(xg_m, yg_m, color = 'red',lw=0.5)
    ax.plot(xg, yg, color = 'purple',lw=1)  
    plt.grid(linestyle = (0, (5, 10))) 
    plt.savefig(os.path.join(dir_,f"3_{label}.png"), format = 'png') 
def write(k,x,fx,s): #запись данных в файл 
    for j in range(i): 
        if j == 0: 
            t = f'{k+1:7}\t{j+1:7}\t[{np.round(x[k][j][0][0],4):7},{np.round(x[k][j][1][0],4):7}] \t{np.round(fx[k][j],4):7}\t{np.round(s,4):7}' 
        else: 
            t = f'{"":7}\t{j+1:7}\t[{np.round(x[k][j][0][0],4):7},{np.round(x[k][j][1][0],4):7}] \t{np.round(fx[k][j],4):7}\t{"":7}' 
        print(t) 
        res.write(t + '\n')

def x_c(x): 
    x_c = X([0,0]) 
    for x_ in x[:-1]:         
        x_c = x_c + x_    
    x_c /= n 
    return x_c 

def stop(x): 
    s = 0 
    for j in range(i): 
        s+= ((f(x[j])-f(x_c(x)))**2)     
    return (1/(n+1)*s)**(0.5) 
l = 2 
label = f'Регулярный симплекс (l = {l})' 
print(label) 
res.write(label + '\n') 
k = 0 
delta = 0.5 
x = [] 
fx = [] 
x_m = [] 
x.append([]) 
fx.append([]) 
x_m.append(x0) 
h = (l**2-(l/2)**2)**(0.5) 
x[k].append(X([-l/2+x0[0][0],x0[1][0]-h/3])) 
x[k].append(X([l/2+x0[0][0],x0[1][0]-h/3])) 
x[k].append(X([x0[0][0],x0[1][0]+2*h/3]))
x[k] = sorted(x[k],key=f) 
for j in range(i): 
    fx[k].append(f(x[k][j])) 
write(k,x,fx,stop(x[k])) 
while stop(x[k]) > epsilon: 
    x_n = 2*x_c(x[k]) - x[k][-1] 
    x_m.append(2*x_c(x[k]) - x_m[k])     
    x.append([]) 
    for j in range(0,i-1): 
        x[k+1].append(x[k][j]) 
    x[k+1].append(x_n) 
    if f(x_n) >= fx[k][-1]: 
        for j in range(1,i): 
            x[k+1][j] = (x[k+1][0]+delta*(x[k+1][j]-x[k+1][0])) #редукция       
        x_m[k+1] = (x[k+1][0]+delta*(x_m[k+1] -x[k+1][0])) 
    k+= 1 
    x[k] = sorted(x[k],key=f) 
    fx.append([]) 
    for j in range(i): 
        fx[k].append(f(x[k][j])) 
    write(k,x,fx,stop(x[k])) 
print(len(x),x[k][0],f(x[k][0])) 
flag = True
graph(label,x,fx) 
label = f'Нелдера-Мида (l = {l})' 
print(label) 
res.write(label + '\n') 
k = 0 
delta = 0.5 
alpha = 1 
betta = 2 
gamma = 0.5 
x = [] 
fx = [] 
x_m = [] 
z = []   
x.append([]) 
fx.append([]) 
x_m.append(x0) 
z.append([]) 
h = (l**2-(l/2)**2)**(0.5) 
x[k].append(X([-l/2+x0[0][0],x0[1][0]-h/3])) 
x[k].append(X([l/2+x0[0][0],x0[1][0]-h/3])) 
x[k].append(X([x0[0][0],x0[1][0]+2*h/3])) 
x[k] = sorted(x[k],key=f) 
for j in range(i): 
    fx[k].append(f(x[k][j])) 
write(k,x,fx,stop(x[k])) 
while stop(x[k]) > epsilon: 
    x_c_ = x_c(x[k]) 
    z[k].append(x_c_+alpha*(x_c_-x[k][-1])) #отражение 
    z[k].append(x_c_+betta*(z[k][0]-x_c_)) #растяжение 
    z[k].append(x_c_+gamma*(z[k][0]-x_c_)) #сжатие + 
    z[k].append(x_c_+gamma*(x[k][-1]-x_c_)) #сжатие - 
    z[k] = sorted(z[k],key=f) 
    x.append([]) 
    z.append([]) 
    fx.append([]) 
    if f(z[k][0]) < f(x[k][-1]): 
        x[k+1] = x[k][:-1] 
        x[k+1].append(z[k][0]) 
    else: 
        for j in range(1,i): 
            x[k+1][j].append(x[k][0]+delta*(x[k][j]-x[k][0])) #редукция     
    k+= 1 
    x[k] = sorted(x[k],key=f) 
    x_m_ = X([0,0]) 
    for j in range(i): x_m_ = x_m_+ x[k][j] 
    x_m.append(x_m_/3) 
    for j in range(i): 
        fx[k].append(f(x[k][j])) 
    write(k,x,fx,stop(x[k])) 
print(len(x),x[k][0],f(x[k][0])) 
graph(label,x,fx) 
res.close() 
input('Готово') 