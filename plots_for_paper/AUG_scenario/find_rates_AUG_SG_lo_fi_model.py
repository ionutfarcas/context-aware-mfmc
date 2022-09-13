import numpy as np
from scipy.linalg import lstsq

if __name__ == '__main__':

	acc_rate_ev 	= np.load('results/SG_lo_fi_model_acc_rate_eval.npy')
	cost_rate_ev 	= np.load('results/SG_lo_fi_model_cost_rate_eval.npy')

	
	# acc_rate_ev 	= np.mean(acc_data, axis=0)
	# cost_rate_ev 	= np.mean(cost_data, axis=0)

	print(acc_rate_ev)

	# exit(0)

	hi_fi_runtime = 410.9941333333333


	N_acc       = np.load('results/SG_lo_fi_model_n_hi_fi_evals.npy')
	N_cost      = np.load('results/SG_lo_fi_model_n_hi_fi_evals.npy')



	cost_rate_ev = cost_rate_ev/hi_fi_runtime


	A_acc 			= np.ones((len(N_acc), 2))
	A_acc[:, 1]    	= -np.log(N_acc)
	y_acc          	= np.log(acc_rate_ev)

	acc_params, resid, rnk, sss = lstsq(A_acc, y_acc)
	acc_params[0] 				= np.exp(acc_params[0])


	A_cost 			= np.ones((len(N_cost), 2))
	A_cost[:, 1]    = np.log(N_cost)
	y_cost          = np.log(cost_rate_ev)

	cost_params, resid, rnk, sss 	= lstsq(A_cost, y_cost)
	cost_params[0] 					= np.exp(cost_params[0])

	


	print(acc_params)
	print(cost_params)

	np.savez('results/SG_lo_fi_model_rate_params.npz', acc_params=acc_params, cost_params=cost_params)