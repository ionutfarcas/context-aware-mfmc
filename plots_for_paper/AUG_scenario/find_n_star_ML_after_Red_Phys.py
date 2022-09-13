import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize


if __name__ == '__main__':

	w1     	= 410.9941333333333
	w2 		= 34.903289782244556
	rho_12 	= 0.9990959539661993

	k1 = 1 - rho_12**2
	k2 = w2/w1

	data = np.load('results/ML_lo_fi_model_rate_params.npz')

	acc_rate_param 	= data['acc_params']
	cost_rate_param = data['cost_params']

	# acc_rate_param = [0.18110276, 0.2575402]


	c1 		= acc_rate_param[0]
	alpha 	= acc_rate_param[1]
	c2 		= cost_rate_param[0]
	beta 	= cost_rate_param[1]

	print(c2, beta)

	# alpha *= 1.5

	# obj_ML 		= lambda n, p: ( k1*(1 - k2) + k2*c1*n**(-alpha) + c2*n**(beta) )/ (p - n)
	# obj_ML_grad = lambda n, p: (-k2*c1*n**(-alpha)*alpha/n + c2*n**beta*beta/n ) / (p - n) + ( k1*(1 - k2) + k2*c1*n**(-alpha) + c2*n**beta ) / (p - n)**2

	obj_ML 		= lambda n, p: ( k1 + k2*c1*n**(-alpha) + c2*n**(beta) )/ (p - n)
	obj_ML_grad = lambda n, p: (-k2*c1*n**(-alpha)*alpha/n + c2*n**beta*beta/n ) / (p - n) + ( k1 + k2*c1*n**(-alpha) + c2*n**beta ) / (p - n)**2


	budget 	= np.array([1e5, 3e5, 5e5, 8e5, 1e6, 3e6, 5e6, 8e6, 1e7, 3e7, 5e7, 8e7, 1e8])
	# budget = np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
	#budget = np.array([1e5, 5e5, 1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14, 1e15, 1e16, 1e17, 1e18])
	budget = np.floor(budget/w1)

	n_star_ML 	= np.zeros_like(budget, dtype=int)
	x0 			= np.array([1.])

	for i, p in enumerate(budget):

		obj_ML_f 		= lambda n: 1e10*p*obj_ML(n, p)
		obj_ML_f_grad 	= lambda n: 1e10*p*obj_ML_grad(n, p)


		bounds = Bounds([1], [p - 1])

		res = minimize(obj_ML_f, x0, method='trust-constr', jac=obj_ML_f_grad, options={'maxiter': 100000, 'gtol':1e-5, 'verbose': False}, bounds=bounds)
		# res = minimize(obj_ML_f, x0, method='nelder-mead', jac=obj_ML_f_grad, options={'xatol': 1e-6, 'maxiter': 10000, 'disp': True})

		if p - np.ceil(res.x[0]) > 1:		

			n_star_ML[i] = np.ceil(res.x[0])
			# print(res.fun)
		else:
			print(i)

	print(n_star_ML)

	print(c2*n_star_ML[3]**(beta))


	np.save('results/ML_after_Red_Phys_n_star.npy', n_star_ML)

	

