
# Problema del vendedor viajero-TSP. Implementación en Python 3.5 usando solver CPLEX. 
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

def TSP(N):
	wb = Workbook()
	ws = wb.active
	book = xlrd.open_workbook('C.xlsx')            #LECTURA DE PARÁMETROS.
	sheet = book.sheet_by_name("C")
	c=[[int(sheet.cell_value(r,c)) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	c=np.matrix(c)  
	print("")
	print("MATRIZ DE DISTANCIAS")
	print("")        
	print(c)    
	print("")
	print("")
	print("") 

	Model=cplex.Cplex()

	x_vars=np.array([["x("+str(i)+","+str(j)+")" for j in range(N)] for i in range(N)])
	x_varnames = x_vars.flatten()
	x_vartypes='B'*N*N
	x_varlb = [0.0]*len(x_varnames)
	x_varub = [1.0]*len(x_varnames)
	x_varobj = []
	for i in range(N):
		for j in range(N):
			x_varobj.append(float(c[i,j]))


	Model.variables.add(obj = x_varobj, lb = x_varlb, ub = x_varub, types = x_vartypes, names = x_varnames)

	u_vars=np.array(["u("+str(i)+")" for i in range(0,N)])
	u_varnames=u_vars.flatten()
	u_vartypes='I'*N
	u_varlb=[1.0]*N
	u_varub=[float(N)-1.0]*N
	u_varobj=[0.0]*N

	Model.variables.add(obj = u_varobj, lb = u_varlb, ub = u_varub, types = u_vartypes, names = u_varnames)
	Model.objective.set_sense(Model.objective.sense.minimize)
	# suma(J,x[i,j])==1.0, forall i in N
	for i in range(N):
		row1=[]
		val1=[]
		for j in range(N):
			row1.append(x_vars[i,j])
			val1.append(1.0)

		Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row1, val= val1)], senses = 'E', rhs = [1.0])

	# suma(i,x[i,j])==1.0, forall j in N
	for j in range(N):
		row2=[]
		val2=[]
		for i in range(N):
			row2.append(x_vars[i,j])
			val2.append(1.0)

		Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row2, val= val2)], senses = 'E', rhs = [1.0])
	
	#u[i]-u[j]-(N-1)x[i,ji]<=N-2 , forall i in N, forall j in N, con i!=j.
	for i in range(1,N):
		for j in range(1,N):
			if i!=j:
				row3=[]
				val3=[]
				row3.append(u_vars[i])
				val3.append(1.0)
				row3.append(u_vars[j])
				val3.append(-1.0)
				row3.append(x_vars[i,j])
				val3.append(float(N)-1.0)
				Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row3, val= val3)], senses = 'L', rhs = [float(N)-2.0])

	
	solution=Model.solve()
	Model.write('modelo.lp')
	#Model.parameters.mip.pool.relgap.set(0.6)
	
	pool_solution=Model.populate_solution_pool()
	#print(pool_solution)

	def show_solution():
		print("\nVARLOS FUNCION OBJETIVO - DISTANCIA MINIMIA = {}".format(Model.solution.get_objective_value()))
		V=[i for i in range(N)]
		E=[]
		E1=[(i,j) for i in range(N) for j in range(N) if i!=j]
		for i in range(0,N):
			for j in range(0,N):
				if(Model.solution.get_values("x("+str(i)+","+str(j)+")")!=0.0):
					print("x("+str(i)+","+str(j)+")"+" = "+str(Model.solution.get_values("x("+str(i)+","+str(j)+")")))
					E.append((i,j))
		print("")

		for i in range(0,N):
			if(Model.solution.get_values("u("+str(i)+")")!=0.0):
				print("u("+str(i)+")"+" = "+str(Model.solution.get_values("u("+str(i)+")")))
		print("")

		G=nx.DiGraph()
		G.add_edges_from(E)
		G.add_nodes_from(V)

		
		pos=nx.spring_layout(G,k=0.3)

		print(Model.solution.get_values("x("+str(1)+","+str(0)+")")) #OBTENER VALOR DE UNA VARIABLE.
		print("ESTATUS_DE_LA_SOLUCION_ENCONTRADA:", Model.solution.get_status_string())
		print("SOLUCION_PRIMAL_OPTIMA?:", Model.solution.is_primal_feasible())
		#print(Model.variables.get_cols())
		
		nx.draw_networkx_nodes(G, pos)
		nx.draw_networkx_labels(G, pos)
		nx.draw_networkx_edges(G, pos, edgelist=E1, edge_color='blue', width=0.3 ,arrows=True) # highlight elist
		nx.draw_networkx_edges(G, pos, edge_color='black', width=1.8,arrows=True) # show all edges, thin lines
		

# turn off axis markings
		plt.axis('off')
		plt.savefig('grafo_tsp.png',dpi=20)
		plt.show()
	
	show_solution()

	



TSP(10)
