import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import modelo


def pontos(pb_img,X, Y):
  w,h = pb_img.size
  dx=w/X
  dy=h/Y

  pontos = np.zeros((X,Y)) #ignora o ultimo ponto
  for i in range(X):
      for j in range(Y):
        x = i*(dx)
        y = j*(dy)
        pxl = pb_img.getpixel((x,y)) #pega os valores correspondentes as cores do pixel
        pontos[i,j] = int(pxl[0]) #como a imagem é em escala de cinza, basta pegar um dos valores

  return pontos

def getValidation(X, Y, frames,intervalo, v):

  pts = np.zeros((frames, X, Y))


  ts= [intervalo * i for i in range(0,frames)] #ts é um vetor que guarda o instante de tempo em que a concetração foi medida
  print(ts)
  R={}
  #pega cada imagem e salva os pontos de interesse
  for i in range(frames):
    busc_arq = "resultados " + str(v) + "/image"
    busc_arq += "{:03.0f}".format(i)
    busc_arq += ".jpg"
    img = Image.open(busc_arq)
    R[round(ts[i],4)]=((255-pontos(img,X,Y))/255) #calcula a consentração em cada posição no tempo ts[i]
    #rever

  max=0
  mask=R[0]
  for i in range(0,frames):
    R[round(ts[i],4)]=(R[round(ts[i],4)]-mask)
    m=np.max(R[round(ts[i],4)])
    if(max<m):
      max=m

  for i in range(0,frames):
    R[round(ts[i],4)]=(R[round(ts[i],4)])/max
    A=R[round(ts[i],4)]
    A[A<0]=0
    R[round(ts[i],4)]=A
    for j in range(X):
      for z in range(Y):
        if v == 0:
          R[round(ts[i],4)][j][z] = 0.99*R[round(ts[i],4)][j][z]
          if R[round(ts[i],4)][j][z] == 0:
            if j<=X-2 and z <= Y-2:
              R[round(ts[i],4)][j][z] = 0.99*(R[round(ts[i],4)][j+1][z] + R[round(ts[i],4)][j-1][z] + R[round(ts[i],4)][j][z-1] + R[round(ts[i],4)][j][z+1])/4

  return R

def resid(P):  #função objetivo a ser reduzida, x são os parametros a serem otimizados

  frames = 14
  intervalo=7/14
  L = 1
  dl = 0.01
  Dados = getValidation(int(L/dl),frames,intervalo,0)

  t = 10
  dt = 0.01
  Sw0 = 0
  times_of_interest = []  # Adjust this list with the specific times you want

  #modelagem da água
  fw = 0.99
  m= modelo.Solve2d(fw, L, dl, t, dt, Sw0, times_of_interest, P) #recebe os valores calculados pelo modelo
  err=np.zeros(frames)

  i=0
  print("Tentando ", P) #imprime os valores dos parametros que estão sendo otimizados
  #calcula o erro do modelo com os parametros testados
  for t,V in  Dados.items():

    t=round(t,4)
    try:
      of=25

      err[i]=np.mean(((m[t][:of]-V[:of])**2)**(0.5))
      i=i+1

    except:
      print(str(t) +"not defined by model")

  #plota a comparação do modelo com os dados
  ts=[0,1,2]
  i=0
  for t in ts:
    plt.plot(m[t][5:of], label="Model t="+str(t),color=(0*(i+2),0*(i+2),0.1*(i+2)))

    plt.plot(Dados[t][:of-5],"--", label="Validation t="+str(t),color=(0*(i+2),0*(i+2),0.1*(i+2)))
    i=i+1
    plt.legend(loc="best")
  plt.show()

  return np.mean(err) #retorna o erro médio