#meter mano

from itertools import combinations #para seleccionar parejas de padres
import numpy as np
import pandas as pd
import random

#https://www.slideshare.net/AhmedGadFCIT/genetic-algorithm-ga-optimization-stepbystep-example
#https://www.linkedin.com/pulse/genetic-algorithm-implementation-python-ahmed-gad/

#Crear una nueva poblacion
class population(): #no se si sea buena idea, pero hay que intentarlo
	def __init__(self,pop_size,n_of_genes):
		self.n_of_genes = n_of_genes
		#self.pop = np.random.uniform(low=-1.0,high=1.0, size=(pop_size,n_of_genes))
		self.pop = np.random.standard_normal(size=(pop_size,n_of_genes))/2
		self.fitness = np.zeros((pop_size,1))
		self.selected = []

	def select_mating_pool(self,n_of_parents):
		#Se debe haber rellenado el atributo self.fitness antes
		if sum(self.fitness)==0:
			print('---Error---')
			print('El fitness de cada individuo en la poblacion es 0. Talvez no has rellenado este atributo')

		df = pd.DataFrame(self.pop) #se crea el dataframe con los genes
		df.insert(loc=self.n_of_genes,column='Fitness',value=self.fitness)#agrego una columna con el finess de cada gen 
		df = df.sort_values(by='Fitness',ascending = False) #ordeno los valores segun su fitness
		self.selected = df.iloc[0:n_of_parents,:self.n_of_genes].values #extraigo los primeros 'N' genes

	def nueva_gen(self,n_de_hijos):
		n_of_parents=len(self.selected)
		comb=list(combinations(range(n_of_parents), 2))

		#Eligo 3 combinaciones de padres ---> Cada combinacion de padres da 1 hijo --> 3 hijos

		if n_de_hijos>len(comb):
			print('---Error---')
			print('Solo pueden haber {} combinaciones de padres distintos'.format(len(comb)))
			print('y tu estas pidiendo {} hijos. Aumenta el numero de padres'.format(n_de_hijos))
		else:
			#love tiene los indices, que me señalan una combinacion de padres
			love = random.sample(comb,k=n_de_hijos)

			hijos=[]
			for pair in love:
				if self.n_of_genes!=1:
					locus = np.random.randint(low=1,high=self.n_of_genes)
				else:
					locus = 1
				half_1 = self.selected[pair[0]][0:locus]
				half_2 = self.selected[pair[1]][locus:]
				hijos.append(np.concatenate((half_1,half_2)))
			hijos_mutados = self.mutate(hijos)
			nueva_gen = np.concatenate((self.selected,hijos_mutados)) #Mantener padres vivos. Agregar hijos mutados

			return nueva_gen

	def mutate(self,hijos):
		prob_mutar = 0.3 # ESTA PROBABILIDAD SE PUEDE CAMBIAR

		for id_h,hijo in enumerate(hijos):
			for id_g,gen in enumerate(hijo):
				if np.random.uniform()<prob_mutar:
					#print('hubo una mutacion en el {} hijo, su {} gen.'.format(id_h,id_g),end=' ')
					#Que tipo de mutacion va a ser
					azar = np.random.uniform() #numero aleatorio entre 0 y 1
					ruido = np.around( np.random.standard_normal(1) ,2)

					if azar<0.2:
						hijos[id_h][id_g]=-gen
					elif azar<0.6:
						#dividir por 2
						hijos[id_h][id_g]=gen/2 + ruido
					else:
						#multiplicar por 2
						hijos[id_h][id_g]=gen*2 + ruido
		return hijos
