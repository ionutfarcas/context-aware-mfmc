import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize

from matplotlib.pyplot import *


if __name__ == '__main__':

	w1     	= 0.1150

	#### RB lo-fi model ####
	acc_p_RB 	= np.array([0.164755097727376, 0.036466590444116, 1.885858754288085])
	cost_p_RB 	= [8.812465314363537e-05, 0.538023318720777]

	c1_RB 		= acc_p_RB[0]
	a_RB 		= acc_p_RB[1]
	alpha_RB 	= acc_p_RB[2]
	c2_RB 		= cost_p_RB[0]
	beta_RB 	= cost_p_RB[1]

	acc_rate_RB 	= lambda n: c1_RB * np.exp(-a_RB *n ** alpha_RB)
	cost_rate_RB 	= lambda n: c2_RB * n ** beta_RB

	d_acc_rate_RB 	= lambda n: -alpha_RB * a_RB * c1_RB * n ** (alpha_RB - 1) * np.exp(-a_RB * n ** alpha_RB)
	d_cost_rate_RB 	= lambda n: beta_RB * c2_RB * n ** (beta_RB  - 1)  


	obj_RB 		= lambda n, p: ( acc_rate_RB(n) + cost_rate_RB(n) )/ (p - n)
	obj_RB_grad = lambda n, p: (d_acc_rate_RB(n) + d_cost_rate_RB(n) ) / (p - n) + \
								( acc_rate_RB(n) + cost_rate_RB(n)  ) / (p - n)**2

	#############

	budget = np.array([1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2])


	budget 		= np.floor(budget/w1)
	n_star_RB 	= np.zeros_like(budget, dtype=int)
	n_star_SVR 	= np.zeros_like(budget, dtype=int)
	x0 			= np.array([1.])

	for i, p in enumerate(budget):

		## SG part ##
		#############

		obj_RB_f 		= lambda n: 1e3*p*obj_RB(n, p)
		obj_RB_f_grad 	= lambda n: 1e3*p*obj_RB_grad(n, p)

		bounds 	= Bounds([1], [p - 1])
		res 	= minimize(obj_RB_f, x0, method='trust-constr', jac=obj_RB_f_grad, options={'maxiter': 10000, 'gtol':1e-15}, bounds=bounds)

		if p - np.ceil(res.x[0]) > 1:		
			n_star_RB[i] = np.ceil(res.x[0])
		else:
			print(i)

	print(n_star_RB)
	

