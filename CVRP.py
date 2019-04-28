# Capacited vehicule routing problem - Dado un grafo G(V,E) donde |V|=N, donde 0 se define como el depot central, se deben determinar K 
# circuitos simples los que deben ser recorridos por los K vehículos disponibles. En cada nodo V\{0} existe una demanda d[i] que debe 
# satisfecha por la flota homogenea de capacidad C. El objetivo es cumplir los requerimientos al mínimo costo de transporte\distancia.

# MTZ-SEC'S
# FORMULACIÓN DE TRES ÍNIDICES.
# LA SUMA DE LAS DEMANDAS DE CADA CIRUCUITO NO DEBE SUPERAR LA CAPACIDAD DE CADA VEHÍCULO.

import time
import numpy as np
import cplex
from cplex import Cplex
from cplex.exceptions import CplexError
import sys
import networkx as nx
import matplotlib.pyplot as plt
from openpyxl import Workbook
import xlrd
import random

def CVRP(N,K,cap):
	wb = Workbook()
	ws = wb.active
	book = xlrd.open_workbook('CVRP.xlsx')            #LECTURA DE PARÁMETROS.
	sheet = book.sheet_by_name("C")
	C=[[int(sheet.cell_value(r,c)) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	C=np.matrix(C)  
	print("")
	print("MATRIZ DE DISTANCIAS")
	print("")        
	print(C)    
	print("")
	print("")
	sheet = book.sheet_by_name("d")
	d=[[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	d=np.matrix(d)  
	print("")
	print("Demandas")
	print("")        
	print(d)    

	Model=cplex.Cplex()

	x_vars=np.array([[["x("+str(i)+","+str(j)+","+str(k)+")" for k in range(K)] for j in range(N)] for i in range(N)])
	x_varnames = x_vars.flatten()
	x_vartypes='B'*N*N*K
	x_varlb = [0.0]*N*N*K
	x_varub = [1.0]*N*N*K
	x_varobj = []
	for i in range(N):
		for j in range(N):
			for k in range(K):
				x_varobj.append(float(C[i,j]))



	Model.variables.add(obj = x_varobj, lb = x_varlb, ub = x_varub, types = x_vartypes, names = x_varnames)


	u_vars=np.array([["u("+str(i)+","+str(k)+")" for k in range(K)] for i in range(0,N)])
	u_varnames=u_vars.flatten()
	u_vartypes='C'*len(u_varnames)
	u_varlb=[0.0]*len(u_varnames)
	u_varub=[cplex.infinity]*len(u_varnames)
	u_varobj=[0.0]*len(u_varnames)

	Model.variables.add(obj = u_varobj, lb = u_varlb, ub = u_varub, types = u_vartypes, names = u_varnames)


	y_vars=np.array([["y("+str(i)+","+str(k)+")" for k in range(K)] for i in range(0,N)])
	y_varnames=y_vars.flatten()
	y_vartypes='B'*N*K
	y_varlb=[0.0]*N*K
	y_varub=[1.0]*N*K
	y_varobj=[0.0]*N*K

	Model.variables.add(obj = y_varobj, lb = y_varlb, ub = y_varub, types = y_vartypes, names = y_varnames)




	Model.objective.set_sense(Model.objective.sense.minimize)

	
	for k in range(K):
		row1=[]
		val1=[]
		for j in range(N):
			row1.append(x_vars[0,j,k])
			val1.append(1.0)
		Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row1, val= val1)], senses = 'E', rhs = [1.0])

	for k in range(K):
		row2=[]
		val2=[]
		for j in range(N):
			row2.append(x_vars[j,0,k])
			val2.append(1.0)
		Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row2, val= val2)], senses = 'E', rhs = [1.0])

	


	for i in range(1,N):
		row3=[]
		val3=[]
		for k in range(K):
			row3.append(y_vars[i,k])
			val3.append(1.0)

		Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row3, val= val3)], senses = 'E', rhs = [1.0])


	for i in range(1,N):
		for k in range(K):
			row4=[]
			val4=[]
			for j in range(N):
				row4.append(x_vars[j,i,k])
				val4.append(1.0)
			row4.append(y_vars[i,k])
			val4.append(-1.0)

			Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row4, val= val4)], senses = 'E', rhs = [0.0])



	for i in range(1,N):
		for k in range(K):
			row5=[]
			val5=[]
			for j in range(N):
				row5.append(x_vars[i,j,k])
				val5.append(1.0)
			row5.append(y_vars[i,k])
			val5.append(-1.0)

			Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row5, val= val5)], senses = 'E', rhs = [0.0])


	for i in range(1,N):
		for j in range(1,N):
			for k in range(K):
				if i!=j:
					row6=[]
					val6=[]
					row6.append(u_vars[i,k])
					val6.append(1.0)
					row6.append(u_vars[j,k])
					val6.append(-1.0)
					row6.append(x_vars[i,j,k])
					val6.append(float(cap))

					Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row6, val= val6)], senses = 'L', rhs = [float(cap-d[j])])


					

	for i in range(1,N):
		for k in range(K):
			row7=[]
			val7=[]
			row7.append(u_vars[i,k])
			val7.append(1.0)

			Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row7, val= val7)], senses = 'L', rhs = [float(cap)])


	for i in range(1,N):
		for k in range(K):
			row8=[]
			val8=[]
			row8.append(u_vars[i,k])
			val8.append(1.0)

			Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row8, val= val8)], senses = 'G', rhs = [float(d[i])])




	solution=Model.solve()
	Model.write('modelocvrp.lp')


	def show_solution():
		print("\nVARLOS FUNCION OBJETIVO - DISTANCIA MINIMIA = {}".format(Model.solution.get_objective_value()))
		for i in range(N):
			for j in range(N):
				for k in range(K):
					if(Model.solution.get_values("x("+str(i)+","+str(j)+","+str(k)+")")!=0.0):
						print("x("+str(i)+","+str(j)+","+str(k)+")"+" = "+str(Model.solution.get_values("x("+str(i)+","+str(j)+","+str(k)+")")))


		print("")

		for i in range(0,N):
			for k in range(K):
				if(Model.solution.get_values("u("+str(i)+","+str(k)+")")!=0.0):
					print("u("+str(i)+","+str(k)+")"+" = "+str(Model.solution.get_values("u("+str(i)+","+str(k)+")")))
		print("")

		for i in range(0,N):
			for k in range(K):
				if(Model.solution.get_values("y("+str(i)+","+str(k)+")")!=0.0):
					print("y("+str(i)+","+str(k)+")"+" = "+str(Model.solution.get_values("y("+str(i)+","+str(k)+")")))
		print("")


	def plot_solution():
		V=[i for i in range(N)]
		G=nx.DiGraph()
		G.add_nodes_from(V)
		E=[]
		pos=nx.spring_layout(G,k=0.3)
		color = list(np.random.choice(range(256), size=3))
		number_of_rutas = K
		color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_rutas)]
		for i in range(N):
			for j in range(N):
				for k in range(K):
					if(Model.solution.get_values("x("+str(i)+","+str(j)+","+str(k)+")")!=0.0):
						E.append((i,j))
						G.add_edges_from(E)
						nx.draw_networkx_edges(G, pos, edgelist=E, edge_color=color[k], width=1.8 ,arrows=True)
						E=[]
		nx.draw_networkx_nodes(G, pos,node_color='y')
		nx.draw_networkx_labels(G, pos)
		plt.axis('off')
		plt.savefig('grafo_cvrp.png',dpi=20)
		plt.show()

	
	show_solution()
	plot_solution()




CVRP(10,4,900)


