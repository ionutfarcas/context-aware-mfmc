import numpy as np
from matplotlib.pyplot import *

from mpl_toolkits.axes_grid.inset_locator import inset_axes


def mfmc_var_one_model(var_hi_fi, p, w1, rho_1):

	mfmc_var_est = var_hi_fi/p * ( \
						np.sqrt((1 - rho_1**2)) + np.sqrt(w1*rho_1**2) \
						  )**2

	return mfmc_var_est


def mfmc_var_two_models(var_hi_fi, p, w2, w3, rho_12, rho_13):

	mfmc_var_est = var_hi_fi/p * ( \
						np.sqrt((1 - rho_12**2)) + \
						np.sqrt(w2*(rho_12**2 - rho_13**2)) + \
						np.sqrt(w3*rho_13**2) \
						  )**2

	return mfmc_var_est

def mfmc_var_three_models(var_hi_fi, p, w2, w3, w4, rho_12, rho_13, rho_14):

	mfmc_var_est = var_hi_fi/p * ( \
						np.sqrt((1 - rho_12**2)) + \
						np.sqrt(w2*(rho_12**2 - rho_13**2)) + \
						np.sqrt(w3*(rho_13**2 - rho_14**2)) + \
						np.sqrt(w4*rho_14**2) \
						  )**2

	return mfmc_var_est


if __name__ == '__main__':

	w0      = 410.9941333333333
	w1 		= 34.903289782244556/w0
	rho_1 	= 0.9990959539661993


	var_hi_fi 	= 0.027953497280131814
	budget 		= np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
	p 			= np.floor(budget/w0)


	# std MC
	mse_std_MC = var_hi_fi/p

	# MFMC Red Phys
	mse_MFMC = mfmc_var_one_model(var_hi_fi, p, w1, rho_1)


	# CA-MFMC + SG
	n_star_SG = np.load('results/SG_n_star_for_comparison.npy')

	data 		= np.load('results/SG_lo_fi_model_rate_params.npz')
	acc_p_SG 	= data['acc_params']
	cost_p_SG 	= data['cost_params']

	c1_SG 		= acc_p_SG[0]
	alpha_SG 	= acc_p_SG[1]
	c2_SG 		= cost_p_SG[0]
	beta_SG 	= cost_p_SG[1]

	acc_rate_SG 	= lambda n: c1_SG * n ** (-alpha_SG)
	cost_rate_SG 	= lambda n: c2_SG * n ** beta_SG

	w2 		= cost_rate_SG(n_star_SG)
	rho_2 	= np.sqrt(1 - acc_rate_SG(n_star_SG))

	mse_CA_MFMC_SG = mfmc_var_one_model(var_hi_fi, p - n_star_SG, w2, rho_2)

	# CA-MFMC + ML
	n_star_ML = np.load('results/ML_n_star_for_comparison.npy')

	data 		= np.load('results/ML_lo_fi_model_rate_params.npz')
	acc_p_ML 	= data['acc_params']
	cost_p_ML 	= data['cost_params']

	c1_ML 		= acc_p_ML[0]
	alpha_ML 	= acc_p_ML[1]
	c2_ML 		= cost_p_ML[0]
	beta_ML 	= cost_p_ML[1]

	acc_rate_ML 	= lambda n: c1_ML * n ** (-alpha_ML)
	cost_rate_ML 	= lambda n: c2_ML * n ** beta_ML

	w3 		= cost_rate_ML(n_star_ML)
	rho_3 	= np.sqrt(1 - acc_rate_ML(n_star_ML))

	mse_CA_MFMC_ML = mfmc_var_one_model(var_hi_fi, p - n_star_ML, w3, rho_3)


	# CA-MFMC + Red Phys + SG
	n_star_SG_after_Red_Phys = np.load('results/SG_after_Red_Phys_n_star_for_comparison.npy')

	
	w4 		= cost_rate_SG(n_star_SG_after_Red_Phys)
	rho_4 	= np.sqrt(1 - acc_rate_SG(n_star_SG_after_Red_Phys))

	mse_CA_MFMC_Red_Phys_SG = mfmc_var_two_models(var_hi_fi, p - n_star_SG_after_Red_Phys, w2, w4, rho_2, rho_4)

	# CA-MFMC + Red Phys + ML
	n_star_ML_after_Red_Phys = np.load('results/ML_after_Red_Phys_n_star_for_comparison.npy')

	
	w5 		= cost_rate_ML(n_star_ML_after_Red_Phys)
	rho_5 	= np.sqrt(1 - acc_rate_ML(n_star_ML_after_Red_Phys))

	mse_CA_MFMC_Red_Phys_ML = mfmc_var_two_models(var_hi_fi, p - n_star_ML_after_Red_Phys, w2, w5, rho_2, rho_5)

	# CA-MFMC + Red Phys + SG + ML
	n_star_ML_after_Red_Phys_and_SG = np.load('results/ML_after_Red_Phys_and_SG_n_star_for_comparison.npy')

	
	w6 		= cost_rate_ML(n_star_ML_after_Red_Phys_and_SG)
	rho_6 	= np.sqrt(1 - acc_rate_ML(n_star_ML_after_Red_Phys_and_SG))

	mse_CA_MFMC_Red_Phys_SG_ML = mfmc_var_three_models(var_hi_fi, p - n_star_SG_after_Red_Phys - n_star_ML_after_Red_Phys_and_SG, \
						 w2, w4, w6, rho_2, rho_4, rho_6)


	# CA-MFMC + SG + ML
	n_star_ML_after_SG = np.load('results/ML_after_SG_n_star_for_comparison.npy')

	w7 		= cost_rate_ML(n_star_ML_after_SG)
	rho_7 	= np.sqrt(1 - acc_rate_ML(n_star_ML_after_SG))

	mse_CA_MFMC_SG_ML = mfmc_var_two_models(var_hi_fi, p - n_star_SG - n_star_ML_after_SG, w2, w7, rho_2, rho_7)


	#### plot

	rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
	rc("text", usetex=True)         # Crisp axis ticks
	rc("font", family="serif")      # Crisp axis labels
	rc("legend", edgecolor='none')  # No boxes around legends
	rcParams["figure.figsize"] = (7, 4.5)
	rcParams.update({'font.size': 10})
	rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

	# line settings for white base
	charcoal    = [0.0, 0.0, 0.0]
	color1      = '#E69F00'
	color2      = '#D55E00'
	color3      = '#CC79A7'
	color4      = '#74a9cf'
	color5 		= '#0570b0' 
	color6 		= '#0c2c84'
	color7 		= '#2ca25f' 
	color8 		= '#8856a7'

	linestyle1 = '--'
	linestyle2 = (0, (5, 1))
	linestyle3 = '-.'
	linestyle4 = (0, (3, 1, 1, 1))
	linestyle5 = (0, (5, 5))
	linestyle6 = (0, (5, 1, 1, 1))

	colors = [charcoal, color2, color4, color1, color5, color6, color7, color8]

	# white base settings
	rc("figure",facecolor='w')
	rc("axes",facecolor='w',edgecolor=charcoal,labelcolor=charcoal)
	rc("savefig",facecolor='w')
	rc("text",color=charcoal)
	rc("xtick",color=charcoal)
	rc("ytick",color=charcoal)

	labels      = [r'std. MC:' + '\n'  + r'$f^{(0)}$', 
					r'MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(2)}_{n_2}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(3)}_{n_3}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}, f^{(2)}_{n_2}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}, f^{(3)}_{n_3}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(2)}_{n_2}, f^{(3)}_{n_3}$', \
					r'CA-MFMC:' + ' ' + r'$f^{(0)},$'  + '\n' + r'$f^{(1)}, f^{(2)}_{n_2}, f^{(3)}_{n_3}$']

	fig1 	= figure()
	ax1 	= fig1.add_subplot(111)

	ax1.spines['right'].set_visible(False)
	ax1.spines['top'].set_visible(False)
	ax1.yaxis.set_ticks_position('left')
	ax1.xaxis.set_ticks_position('bottom')

	ax1.spines['bottom'].set_bounds(9e3, 1e10)
	ax1.spines['left'].set_bounds(1e-15, 1e-2)

	ax1.loglog(budget, mse_std_MC, linestyle=linestyle1, lw=0.75, marker='*', ms=3, color=charcoal, label=labels[0])
	ax1.loglog(budget, mse_MFMC, linestyle=linestyle2, lw=0.75, marker='s', ms=3, color=color2, label=labels[1])
	ax1.loglog(budget, mse_CA_MFMC_SG, linestyle=linestyle4, lw=0.75, marker='o', ms=3, color=color4, label=labels[3])
	ax1.loglog(budget, mse_CA_MFMC_ML, linestyle=linestyle4, lw=0.75, marker='o', ms=3, color=color1, label=labels[3])
	ax1.loglog(budget, mse_CA_MFMC_Red_Phys_SG, linestyle=linestyle4, lw=0.75, marker='o', ms=3, color=color5, label=labels[4])
	ax1.loglog(budget, mse_CA_MFMC_Red_Phys_ML, linestyle=linestyle4, lw=0.75, marker='o', ms=3, color=color6, label=labels[5])
	ax1.loglog(budget, mse_CA_MFMC_SG_ML, linestyle=linestyle4, lw=0.75, marker='o', ms=3, color=color7, label=labels[6])
	ax1.loglog(budget, mse_CA_MFMC_Red_Phys_SG_ML, linestyle=linestyle4, lw=0.75, marker='o', ms=3, color=color8, label=labels[7])

	ax1.axvline(x=5e5, color=charcoal, linestyle='--', lw=0.75)

	ax1.set_xlabel('computational budget p (seconds)')
	ax1.set_ylabel('mean-squared error')

	legend = ax1.legend(loc=3, ncol=2, fontsize=8)

	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	ax1.set_xlim([9e3, 1.1e10])
	ax1.set_ylim([1e-15, 1e0])


	data 	= [mse_std_MC[3], mse_MFMC[3], mse_CA_MFMC_SG[3], mse_CA_MFMC_ML[3], mse_CA_MFMC_Red_Phys_SG[3], \
					mse_CA_MFMC_Red_Phys_ML[3], mse_CA_MFMC_SG_ML[3], mse_CA_MFMC_Red_Phys_SG_ML[3]]
	x 		= range(len(data))
	w 		= 0.2

	inset_axes = inset_axes(ax1,
                    width="55%", # width = 30% of parent_bbox
                    height=0.9, # height : 1 inch
                    loc=1)

	inset_axes.spines['right'].set_visible(False)
	inset_axes.spines['top'].set_visible(False)
	inset_axes.yaxis.set_ticks_position('left')
	inset_axes.xaxis.set_ticks_position('bottom')

	inset_axes.bar(x, data, w, color=colors)
	inset_axes.set_yscale('log')

	inset_axes.set_xticks(x)
	inset_axes.set_xticklabels(labels, rotation=45, fontsize=6)

	inset_axes.tick_params(axis='y', labelsize=6)

	inset_axes.set_ylim([1e-8, 2e-5])

	for tick in inset_axes.get_xaxis().get_major_ticks():
	    tick.set_pad(0.4)

	[t.set_color(colors[i]) for i, t in enumerate(inset_axes.xaxis.get_ticklabels())]


	x_pos_all 	= [1e4, 5e5, 1e7, 1e8, 1e9, 1e10]
	labels 		= [r'$10^4$', r'$\boldsymbol{5 \times 10^5}$', r'$10^{7}$', r'$10^{8}$', r'$10^{9}$', r'$10^{10}$']
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)


	y_pos_all 	= [1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2]
	labels 		= [r'$10^{-12}$', r'$10^{-10}$', r'$10^{-8}$', r'$10^{-6}$', r'$10^{-4}$', r'$10^{-2}$']
	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)


	tight_layout()

	#plt.show()

	savefig('figures/AUG_MSE_comparison.pdf', pad_inches=3)
	close()

