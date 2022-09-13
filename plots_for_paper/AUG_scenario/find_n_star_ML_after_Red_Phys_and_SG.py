import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize

from matplotlib.pyplot import *


if __name__ == '__main__':

	w1     	= 410.9941333333333
	w2 		= 34.903289782244556
	rho_12 	= 0.9990959539661993

	k_a_1 = 1 - rho_12**2
	k_c_1 = w2/w1


	#### SG lo-fi model ####
	data 		= np.load('results/SG_lo_fi_model_rate_params.npz')
	acc_p_SG 	= data['acc_params']
	cost_p_SG 	= data['cost_params']

	c1_SG 		= acc_p_SG[0]
	alpha_SG 	= acc_p_SG[1]
	c2_SG 		= cost_p_SG[0] 
	beta_SG 	= cost_p_SG[1] 

	acc_rate_SG 	= lambda n: c1_SG * n ** (-alpha_SG)
	cost_rate_SG 	= lambda n: c2_SG * n ** beta_SG

	d_acc_rate_SG 	= lambda n: -alpha_SG * c1_SG * n ** (-alpha_SG - 1)
	d_cost_rate_SG 	= lambda n: beta_SG * c2_SG * n ** (beta_SG  - 1)  


	obj_SG 		= lambda n, p: ( k_a_1 + k_c_1*acc_rate_SG(n) + cost_rate_SG(n) )/ (p - n)
	obj_SG_grad = lambda n, p: (k_c_1*d_acc_rate_SG(n) + d_cost_rate_SG(n) ) / (p - n) + \
								( k_a_1 + k_c_1*acc_rate_SG(n) + cost_rate_SG(n)  ) / (p - n)**2


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

	obj_ML 		= lambda k_a_2, k_c_2, n, p: ( k_a_1 + k_a_2*k_c_1 + \
												k_c_2*acc_rate_ML(n) + cost_rate_ML(n) )/ (p - n)
	obj_ML_grad = lambda k_a_2, k_c_2, n, p: (k_c_2*d_acc_rate_ML(n) + d_cost_rate_ML(n) ) / (p - n) + \
											( k_a_1 + k_a_2*k_c_1 + \
												k_c_2*acc_rate_ML(n) + cost_rate_ML(n) ) / (p - n)**2

	#############

	budget = np.array([1e5, 3e5, 5e5, 8e5, 1e6, 3e6, 5e6, 8e6, 1e7, 3e7, 5e7, 8e7, 1e8])

	# budget = np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])


	budget 		= np.floor(budget/w1)
	n_star_SG 	= np.zeros_like(budget, dtype=int)
	n_star_ML 	= np.zeros_like(budget, dtype=int)
	x0 			= np.array([1.])

	for i, p in enumerate(budget):

		## SG part ##
		#############

		obj_SG_f 		= lambda n: 1e4*p*obj_SG(n, p)
		obj_SG_f_grad 	= lambda n: 1e4*p*obj_SG_grad(n, p)

		bounds 	= Bounds([1], [p - 1])
		res 	= minimize(obj_SG_f, x0, method='trust-constr', jac=obj_SG_f_grad, options={'maxiter': 10000, 'gtol':1e-15}, bounds=bounds)

		if p - np.ceil(res.x[0]) > 1:		
			n_star_SG[i] = np.ceil(res.x[0])
		else:
			print(i)


		## ML part ##
		#############
		new_p = p - n_star_SG[i]

		k_a_2 = acc_rate_SG(n_star_SG[i])
		k_c_2 = cost_rate_SG(n_star_SG[i])

		obj_ML_f 		= lambda n: 1e4*new_p*obj_ML(k_a_2, k_c_2, n, new_p)
		obj_ML_f_grad 	= lambda n: 1e4*new_p*obj_ML_grad(k_a_2, k_c_2, n, new_p)

		bounds 	= Bounds([1], [new_p - 1])
		res 	= minimize(obj_ML_f, x0, method='trust-constr', jac=obj_ML_f_grad, options={'maxiter': 10000, 'gtol':1e-15}, bounds=bounds)

		if new_p - np.ceil(res.x[0]) > 1:		

			n_star_ML[i] = np.ceil(res.x[0])
		else:
			print(i)


	print(n_star_SG)
	print(n_star_ML)

	np.save('results/ML_after_Red_Phys_and_SG_n_star.npy', n_star_ML)

	

