import numpy as np
from matplotlib.pyplot import *

def mfmc_preproc(rho_12, rho_13, rho_14, w1, w2, w3, w4, p):


	r1 = 1.0
	r2 = np.sqrt(w1*(rho_12**2 - rho_13**2)/(w2 * (1 - rho_12**2)))
	r3 = np.sqrt(w1*(rho_13**2 - rho_14**2)/(w3 * (1 - rho_12**2)))
	r4 = np.sqrt(w1*rho_14**2/(w4 * (1 - rho_12**2)))

	
	m1 		= int(np.floor(p/(w1*r1 + w2*r2 + w3*r3 + w4*r4)))
	m2 		= int(np.floor(r2*m1))
	m3 		= int(np.floor(r3*m1))
	m4 		= int(np.floor(r4*m1))

	return m1, m2, m3, m4

def calc_mfmc_var_one_model(var_hi_fi, p, w1, w2, rho_12):

	mfmc_var_est = var_hi_fi/p * ( \
						np.sqrt(w1*(1 - rho_12**2)) + np.sqrt(w2*rho_12**2) \
						  )**2

	return mfmc_var_est

def calc_mfmc_var_two_models(var_hi_fi, p, w1, w2, w3, rho_12, rho_13):

	mfmc_var_est = var_hi_fi/p * ( \
						np.sqrt(w1*(1 - rho_12**2)) + \
						np.sqrt(w2*(rho_12**2 - rho_13**2)) + \
						np.sqrt(w3*rho_13**2) \
						  )**2

	return mfmc_var_est

def calc_mfmc_var_three_models(var_hi_fi, p, w1, w2, w3, w4, rho_12, rho_13, rho_14):

	mfmc_var_est = var_hi_fi/p * ( \
						np.sqrt(w1*(1 - rho_12**2)) + \
						np.sqrt(w2*(rho_12**2 - rho_13**2)) + \
						np.sqrt(w3*(rho_13**2 - rho_14**2)) + \
						np.sqrt(w4*rho_14**2) \
						  )**2

	return mfmc_var_est

if __name__ == '__main__':

	budget 		= 5e5
	no_cores 	= 32

	target_MSE = 5.74041975175521e-08

	var_hi_fi 		= 0.027953497280131814

	w1 				= 410.9941333333333
	w_red_phys 		= 34.903289782244556


	### MFMC Red Phys
	N_hi_fi_MFMC = 155
	N_lo_fi_MFMC = 12508
	###


	### CA-MFMC 1
	w_ASG_CAMFMC_1 = 0.00031220558362957834 * w1

	N_hi_fi_CAMFMC_1 		= 548
	N_ASG_lo_fi_CAMFMC_1 	= 734464

	n_star_ASG_CAMFMC_1 = 438
	##

	### CA-MFMC 3
	w_ASG_CAMFMC_2 	=  7.814510150451494e-05* w1

	N_hi_fi_CAMFMC_2 			= 565 
	N_Red_Phys_lo_fi_CAMFMC_2 	= 4114
	N_ASG_lo_fi_CAMFMC_2 		= 2102057

	n_star_ASG_CAMFMC_2 = 131
	##

	### CA-MFMC 3
	w_ML_CAMFMC_3 	= 4.725917347554188e-07 * w1

	N_hi_fi_CAMFMC_3 			= 342
	N_Red_Phys_lo_fi_CAMFMC_3 	= 8323
	N_ML_lo_fi_CAMFMC_3 		= 16158025

	n_star_ML_CAMFMC_3 = 159
	##

	# budget smallest MSE for MC sampling
	budget_MC_smallest_MSE = var_hi_fi/target_MSE*w1

	std_mc_mse 	= var_hi_fi/budget_MC_smallest_MSE * w1

	print(std_mc_mse)
	print(budget_MC_smallest_MSE)

	## std MC
	runtime_days_std_MC = budget_MC_smallest_MSE / (3600 * no_cores * 24)


	## MFMC
	runtime_days_MFMC = (N_hi_fi_MFMC*w1 + N_lo_fi_MFMC*w_red_phys) / (3600 * no_cores)


	## CAMFMC ASG
	runtime_days_AMFMC_ASG_online 	= (N_hi_fi_CAMFMC_1*w1 + N_ASG_lo_fi_CAMFMC_1*w_ASG_CAMFMC_1) / (3600 * no_cores)

	runtime_days_AMFMC_ASG_all = (N_hi_fi_CAMFMC_1*w1 + N_ASG_lo_fi_CAMFMC_1*w_ASG_CAMFMC_1 + w1*n_star_ASG_CAMFMC_1) / (3600 * no_cores)


	## CAMFMC Red Phys + ASG + ML
	runtime_days_AMFMC_Red_Phys_ASG_online 	= (N_hi_fi_CAMFMC_2*w1 + N_Red_Phys_lo_fi_CAMFMC_2*w_red_phys \
										 			+ N_ASG_lo_fi_CAMFMC_2*w_ASG_CAMFMC_2) / (3600 * no_cores )

	runtime_days_AMFMC_Red_Phys_ASG_all = (N_hi_fi_CAMFMC_2*w1 + N_Red_Phys_lo_fi_CAMFMC_2*w_red_phys \
										 			+ N_ASG_lo_fi_CAMFMC_2*w_ASG_CAMFMC_2 + n_star_ASG_CAMFMC_2 * w1) / (3600 * no_cores)
	
	
	## CAMFMC Red Phys + ASG + ML
	runtime_hours_AMFMC_Red_Phys_ML_online 	= (N_hi_fi_CAMFMC_3*w1 + N_Red_Phys_lo_fi_CAMFMC_3*w_red_phys \
										 			+ N_ML_lo_fi_CAMFMC_3*w_ML_CAMFMC_3) / (3600 * no_cores)

	runtime_hours_AMFMC_Red_Phys_ML_all = (N_hi_fi_CAMFMC_3*w1 + N_Red_Phys_lo_fi_CAMFMC_3*w_red_phys \
										 			+ N_ML_lo_fi_CAMFMC_3*w_ML_CAMFMC_3 \
										 			+ w1*(n_star_ML_CAMFMC_3)) / (3600 * no_cores)

	print('runtime std MC (days):', runtime_days_std_MC)
	print('runtime MFMC (hours):', runtime_days_MFMC)
	print('runtime CAMFMC ASG online (hours):', runtime_days_AMFMC_ASG_online)
	print('runtime CAMFMC ASG (hours):', runtime_days_AMFMC_ASG_all)
	print('runtime CAMFMC Red Phys ASG online (hours):', runtime_days_AMFMC_Red_Phys_ASG_online)
	print('runtime CAMFMC Red Phys ASG (hours):', runtime_days_AMFMC_Red_Phys_ASG_all)
	print('runtime CAMFMC Red Phys ML online (hours):', runtime_hours_AMFMC_Red_Phys_ML_online)
	print('runtime CAMFMC Red Phys ML (hours):', runtime_hours_AMFMC_Red_Phys_ML_all)