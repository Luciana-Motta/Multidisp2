from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
import modelo 
import ajuste


##problema a ser minimzado
print("Começando minimização")
#res = minimize(resid, [(1)for i in range(n)], method='Powell', bounds=[(0,0.01),(0.01,3),(0.01,3),(0.005,1),(0.1,10),(0.001,0.3),(0.001,0.5)],
               #options={'gtol': 1e-3, 'disp': True})

#parametros a serem ajustados
lamb = 5.0 #mobilidade total*
krg = 1.0 #permeabilidade efetiva (gás)
krw = 0.75 #permeabilidade efetiva (água)
Swc = 0.99 #Saturação da água*
Sgr = 0.000 #Saturação do gás*

res = minimize(ajuste.resid, [lamb, krg, krw, Swc, Sgr], method='Powell', bounds=[(3,6),(0,2),(0.0,1),(0, 1),(0, 1)])


##melhor conjunto de paramêtros encontado
res.P

print(res.P)
#plota resultados
frames = 14
intervalo=7/14

L = 1
dl = 0.01
t = 10
dt = 0.01
Sw0 = 0
times_of_interest = []  # Adjust this list with the specific times you want

#modelagem da água
fw = 0.99
m = modelo.Solve2d(fw, L, dl, t, dt, Sw0, times_of_interest,res.P)
Dados = ajuste.getValidation(int(L/dl),frames,intervalo,0)

#apresenta a melhor solução
ts=[0,1,2,3,4,5,6]
for t1 in ts:
  plt.plot(m[t1], label="Model t="+str(t1), color=(0,0,0))
  plt.plot(Dados[t1],"--", label="Validation t="+str(t1), color=(0,0,0.5))
  plt.xlim(0,20)
  plt.xlabel("x")
  plt.ylabel("saturação")
  plt.show()
  plt.legend(loc="best")


err=[(np.mean(((m[t]-Dados[t])**2)**(0.5))) for t1 in ts]

plt.plot(ts,err,label="error")
plt.xlabel("tempo (t)")
plt.ylabel("erro")
plt.legend(loc="best")