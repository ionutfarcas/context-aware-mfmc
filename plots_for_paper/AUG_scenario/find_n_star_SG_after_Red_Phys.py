import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize


if __name__ == '__main__':

	w1     	= 410.9941333333333
	w2 		= 34.903289782244556
	rho_12 	= 0.9990959539661993

	k1 = 1 - rho_12**2
	k2 = w2/w1

	data = np.load('results/SG_lo_fi_model_rate_params.npz')

	acc_rate_param 	= data['acc_params']
	cost_rate_param = data['cost_params']

	c1 		= acc_rate_param[0]
	alpha 	= acc_rate_param[1]
	c2 		= cost_rate_param[0]
	beta 	= cost_rate_param[1]

	# obj_SG 		= lambda n, p: ( k1*(1 - k2) + k2*c1*n**(-alpha) + c2*n**(beta) )/ (p - n)
	# obj_SG_grad = lambda n, p: (-k2*c1*n**(-alpha)*alpha/n + c2*n**beta*beta/n ) / (p - n) + ( k1*(1 - k2) + k2*c1*n**(-alpha) + c2*n**beta ) / (p - n)**2

	obj_SG 		= lambda n, p: ( k1 + k2*c1*n**(-alpha) + c2*n**(beta) )/ (p - n)
	obj_SG_grad = lambda n, p: (-k2*c1*n**(-alpha)*alpha/n + c2*n**beta*beta/n ) / (p - n) + ( k1 + k2*c1*n**(-alpha) + c2*n**beta ) / (p - n)**2


	budget = np.array([1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
	# budget = np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
	budget = np.floor(budget/w1)

	n_star_SG 	= np.zeros_like(budget, dtype=int)
	x0 			= np.array([1.])

	for i, p in enumerate(budget):

		obj_SG_f 		= lambda n: 1e2*p*obj_SG(n, p)
		obj_SG_f_grad 	= lambda n: 1e2*p*obj_SG_grad(n, p)


		bounds = Bounds([1], [p - 1])

		res = minimize(obj_SG_f, x0, method='trust-constr', jac=obj_SG_f_grad, options={'maxiter': 10000, 'gtol':1e-15}, bounds=bounds)

		if p - np.ceil(res.x[0]) > 1:		

			n_star_SG[i] = np.ceil(res.x[0])
		else:
			print(i)

	print(n_star_SG)

	print(c2*n_star_SG[3]**(beta))

	np.save('results/SG_after_Red_Phys_n_star.npy', n_star_SG)

	

