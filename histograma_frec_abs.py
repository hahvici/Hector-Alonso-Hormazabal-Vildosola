# -*- coding: utf-8 -*-
"""
Created on Fri May 25 23:46:38 2018

@author: Alonso
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
mu, sigma = 0, 1.0 # media y desvio estandar
datos = np.random.normal(mu, sigma, 10000) #creando muestra de datos
x=np.linspace(-4,4,num=1000)
y=st.norm.pdf(x,0,1)

plt.plot(x,y,'r')
# histograma de distribución normal.
plt.hist(datos, 30,color='b',histtype='bar',cumulative=False,edgecolor='black', linewidth=0.7,density=True,label="Datos")
plt.plot(x,y,'r-',label=("$\\mu$={}, $\\sigma^2$={}".format(mu, sigma)))
plt.ylim(0,1)
plt.ylabel('frequencia')
plt.xlabel('valores')
plt.title('Histograma - Variable aleatoria normal')
plt.legend(loc="upper right") 
plt.grid(True)  
plt.show()

# Datos empiricos vs distribución teórica supuesta.

