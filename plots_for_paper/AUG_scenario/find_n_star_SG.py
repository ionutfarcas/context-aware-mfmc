import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize

from matplotlib.pyplot import *


if __name__ == '__main__':

	w1     	= 410.9941333333333

	#### SG lo-fi model ####
	data 		= np.load('results/SG_lo_fi_model_rate_params.npz')
	acc_p_SG 	= data['acc_params']
	cost_p_SG 	= data['cost_params']

	print(acc_p_SG)

	c1_SG 		= acc_p_SG[0]
	alpha_SG 	= acc_p_SG[1]
	c2_SG 		= cost_p_SG[0]
	beta_SG 	= cost_p_SG[1]

	acc_rate_SG 	= lambda n: c1_SG * n ** (-alpha_SG)
	cost_rate_SG 	= lambda n: c2_SG * n ** beta_SG

	d_acc_rate_SG 	= lambda n: -alpha_SG * c1_SG * n ** (-alpha_SG - 1)
	d_cost_rate_SG 	= lambda n: beta_SG * c2_SG * n ** (beta_SG  - 1)  


	obj_SG 		= lambda n, p: ( acc_rate_SG(n) + cost_rate_SG(n) )/ (p - n)
	obj_SG_grad = lambda n, p: (d_acc_rate_SG(n) + d_cost_rate_SG(n) ) / (p - n) + \
								( acc_rate_SG(n) + cost_rate_SG(n)  ) / (p - n)**2

	#############


	budget = np.array([1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
	# budget = np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])


	budget 		= np.floor(budget/w1)
	n_star_SG 	= np.zeros_like(budget, dtype=int)
	x0 			= np.array([1.])

	for i, p in enumerate(budget):

		## SG part ##
		#############

		obj_SG_f 		= lambda n: 1e2*p*obj_SG(n, p)
		obj_SG_f_grad 	= lambda n: 1e2*p*obj_SG_grad(n, p)

		bounds 	= Bounds([1], [p - 1])
		res 	= minimize(obj_SG_f, x0, method='trust-constr', jac=obj_SG_f_grad, options={'maxiter': 10000, 'gtol':1e-15}, bounds=bounds)

		if p - np.ceil(res.x[0]) > 1:		
			n_star_SG[i] = np.ceil(res.x[0])
		else:
			print(i)

		nn = np.linspace(1, 1000 - 1, 100)

		fig = figure()
		ax 	= fig.add_subplot(111)

		ax.semilogy(nn, obj_SG_f(nn), 'r-')
		ax.semilogy(n_star_SG[i], obj_SG_f(n_star_SG[i]), linestyle=None, marker='o')

	
		# show()

	print(n_star_SG)

	print(cost_rate_SG(n_star_SG[3]))

	np.save('results/SG_n_star.npy', n_star_SG)