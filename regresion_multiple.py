# -*- coding: utf-8 -*-
"""
Created on Wed Jun 06 01:26:11 2018

@author: Alonso
"""
import pandas as pd
import scipy as sp
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import statsmodels.api as sm
import matplotlib.pyplot as plt
from IPython.html.widgets import interact
from IPython.html import widgets
import matplotlib 
import statsmodels.api as sm
import statsmodels.formula.api as smf
NBA = pd.read_csv("NBA.csv")
df = pd.DataFrame(NBA)
print(df)

"""model = smf.ols(formula="W ~ PTS + oppPTS", data=NBA).fit()
results=model.summary()
print(results)"""
print("-------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------")
print("")
print("")
print("")
#---------------------------------------------------------
y = NBA['W']
X = NBA[['PTS', 'oppPTS']]
z = NBA['PTS']
m=  NBA ['oppPTS']

X = sm.add_constant(X)
model1 = sm.OLS(y, X).fit()
results1=model1.summary(alpha=0.05)
print(results1)

print(model1.resid) # residuos
print("")
print(model1.outlier_test()) # prubea de outlier - Bonferroni
print("")
print(model1.tvalues) # estadisticos t
print("")
print(model1.params) # parametros modelo
print("")
print(model1.mse_resid) # cuadrado medio del error
print("")
print(model1.mse_model) # cuadrado medio del modelo
e=model1.resid
q=model1.outlier_test()
q=np.matrix(q)
s=q[:,0]
s=s.tolist()  # residuos estudentizados
print(s)
X=np.matrix(X)
plt.scatter(z,y, c="r", alpha=1.0,edgecolor='black',label="PTS")
plt.legend(loc=2)
plt.title("W vs PTS")
plt.show()

plt.scatter(m,y, c="b", alpha=1.0,edgecolor='black',label=" oppPTS")
plt.legend(loc=1)
plt.title("W vs oppPTS")
plt.show()


plt.scatter(range(len(y)),e, c="y", alpha=1.0,edgecolor='black',label=" residuos")
plt.legend(loc=1)
plt.title("residuos vs numero observacion")
plt.axhline(y=0.0, color='black', linestyle='-')
plt.show()

plt.scatter(range(len(y)),s, c="g", alpha=1.0,edgecolor='black',label=" residuos estudentizados")
plt.legend(loc=1)
plt.title("residuos estudentizados vs numero observacion")
plt.axhline(y=0.0, color='black', linestyle='-')
plt.axhline(y=-2.0, color='red', linestyle='-')
plt.axhline(y=2.0, color='red', linestyle='-')
plt.show()


xxx=np.linspace(-11,11,1000)
mu=0.0
sigma=np.sqrt(9.38155339629)
yyy=st.norm.pdf(xxx,0,np.sqrt(9.38155339629))

plt.plot(xxx,yyy,'r',label=("$\mu$={}, $\sigma$={}".format(mu, sigma)))
plt.hist(e, 30,color='g',histtype='bar',cumulative=False,edgecolor='black', linewidth=1.0,density=True,label="Residuos")
plt.ylabel('frequencia')
plt.xlabel('valores')
plt.title('Histograma - Residuos')
plt.grid(True)  
plt.legend(loc=1,fontsize = 'small')
plt.savefig('fotofoto', dpi=2000)
plt.show()
print(model1.mse_resid)
#   IC - RESUDIOS ESRTUDENTIZADOS (+/-)t sub (alfa/2,n-k-1)




