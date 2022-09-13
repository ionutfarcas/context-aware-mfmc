import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize

from matplotlib.pyplot import *


if __name__ == '__main__':

	w1     	= 410.9941333333333

	#### ML lo-fi model ####
	data 		= np.load('results/ML_lo_fi_model_rate_params.npz')
	acc_p_ML 	= data['acc_params']
	cost_p_ML 	= data['cost_params']

	c1_ML 		= acc_p_ML[0]
	alpha_ML 	= acc_p_ML[1]
	c2_ML 		= cost_p_ML[0]
	beta_ML 	= cost_p_ML[1]

	acc_rate_ML 	= lambda n: c1_ML * n ** (-alpha_ML)
	cost_rate_ML 	= lambda n: c2_ML * n ** beta_ML

	d_acc_rate_ML 	= lambda n: -alpha_ML * c1_ML * n ** (-alpha_ML - 1)
	d_cost_rate_ML 	= lambda n: beta_ML * c2_ML * n ** (beta_ML  - 1)  


	obj_ML 		= lambda n, p: ( acc_rate_ML(n) + cost_rate_ML(n) )/ (p - n)
	obj_ML_grad = lambda n, p: (d_acc_rate_ML(n) + d_cost_rate_ML(n) ) / (p - n) + \
								( acc_rate_ML(n) + cost_rate_ML(n)  ) / (p - n)**2

	#############


	budget = np.array([1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
	# budget = np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])


	budget 		= np.floor(budget/w1)
	n_star_ML 	= np.zeros_like(budget, dtype=int)
	x0 			= np.array([1.])

	for i, p in enumerate(budget):

		## ML part ##
		#############

		obj_ML_f 		= lambda n: 1e4*p*obj_ML(n, p)
		obj_ML_f_grad 	= lambda n: 1e4*p*obj_ML_grad(n, p)

		bounds 	= Bounds([1], [p - 1])
		res 	= minimize(obj_ML_f, x0, method='trust-constr', jac=obj_ML_f_grad, options={'maxiter': 10000, 'gtol':1e-10}, bounds=bounds)
		# res = minimize(obj_ML_f, x0, method='nelder-mead', jac=obj_ML_f_grad, options={'xatol': 1e-12, 'disp': True})

		if p - np.ceil(res.x[0]) > 1:		
			n_star_ML[i] = np.ceil(res.x[0])
		else:
			print(i)

		# nn = np.linspace(1, 1000 - 1, 100)

		# fig = figure()
		# ax 	= fig.add_subplot(111)

		# ax.semilogy(nn, obj_ML_f(nn), 'r-')
		# ax.semilogy(n_star_ML[i], obj_ML_f(n_star_ML[i]), linestyle=None, marker='o')

	
		# show()

	print(n_star_ML)

	print(cost_rate_ML(259))

	np.save('results/ML_n_star.npy', n_star_ML)