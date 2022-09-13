import numpy as np
from matplotlib.pyplot import *

from scipy.io import loadmat

if __name__ == '__main__':

	p 	= np.array([1e0, 5e0, 1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2])
	
	## analytical MSEs
	mses 						= loadmat('results/MSE_TB_RB_analytic.mat')
	mse_std_mc_analytic 		= mses['mse_std_mc_eval']
	mse_mfmc_RB_analytic 		= mses['mse_mfmc_rb_eval']
	mse_ca_mfmc_RB_analytic 	= mses['mse_ca_mfmc_rb_eval']
	mse_ca_mfmc_RB_SVR_analytic = mses['mse_ca_mfmc_rb_svr_eval']
	###

	## calculated MSEs
	mses 						= loadmat('results/MSE_TB_RB_computed.mat')
	mse_std_mc_computed 		= mses['mse_std_mc_calc']
	mse_mfmc_RB_computed 		= mses['mse_mfmc_rb_calc']
	mse_ca_mfmc_RB_computed 	= mses['mse_ca_mfmc_rb_calc']
	mse_ca_mfmc_RB_SVR_computed = mses['mse_ca_mfmc_rb_svr_calc']
	###


	rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
	rc("text", usetex=True)         # Crisp axis ticks
	rc("font", family="serif")      # Crisp axis labels
	rc("legend", edgecolor='none')  # No boxes around legends
	rcParams["figure.figsize"] = (6, 3)
	rcParams.update({'font.size': 8})

	# line settings for white base
	# plot colors
	charcoal    = [0.0, 0.0, 0.0]
	color1      = '#E69F00'
	color2      = '#D55E00'
	color3      = '#CC79A7'
	color4      = '#1d91c0'
	color5 		= '#0c2c84' 
	    

	linestyle1 = '--'
	linestyle2 = (0, (5, 1))
	linestyle3 = '-.'
	linestyle4 = (0, (3, 1, 1, 1))
	linestyle5 = (0, (5, 5))
	linestyle6 = (0, (5, 1, 1, 1))

	# white base settings
	rc("figure",facecolor='w')
	rc("axes",facecolor='w',edgecolor=charcoal,labelcolor=charcoal)
	rc("savefig",facecolor='w')
	rc("text",color=charcoal)
	rc("xtick",color=charcoal)
	rc("ytick",color=charcoal)



	fig1 	= figure()
	ax1 	= fig1.add_subplot(121)
	ax2 	= fig1.add_subplot(122)

	ax1.spines['right'].set_visible(False)
	ax1.spines['top'].set_visible(False)
	ax1.yaxis.set_ticks_position('left')
	ax1.xaxis.set_ticks_position('bottom')


	ax2.spines['right'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax2.yaxis.set_ticks_position('left')
	ax2.xaxis.set_ticks_position('bottom')

	
	ax1.loglog(p[:7], 5e-3*p[:7]**(-1), '-', lw=1.0, color=charcoal)
	ax1.text(1e1, 6e-4, r'$p^{-1}$', color=charcoal)

	ax1.loglog(p, mse_std_mc_analytic, linestyle=linestyle1, lw=0.5, marker='*', ms=3, color=charcoal)
	ax1.loglog(p, mse_mfmc_RB_analytic[:, 0], linestyle=linestyle2, lw=0.5, marker='s', ms=3, color=color1)
	ax1.loglog(p[1:], mse_mfmc_RB_analytic[1:, 1], linestyle=linestyle3, lw=0.5, marker='s', ms=3, color=color2)
	# ax1.loglog(p[2:], mse_mfmc_RB_analytic[2:, 2], linestyle=linestyle4, lw=0.5, marker='s', ms=3, color=color3)
	ax1.loglog(p, mse_ca_mfmc_RB_analytic, linestyle=linestyle5, lw=0.5, marker='o', ms=3, color=color4)
	ax1.loglog(p[2:], mse_ca_mfmc_RB_SVR_analytic[2:], linestyle=linestyle6, lw=0.5, marker='o', ms=3, color=color5)
	ax1.set_xlabel('computational budget p (seconds)')
	ax1.set_ylabel('mean-squared error')


	ax1.text(25, 3.5*mse_std_mc_analytic[-1], 'std. MC:' + ' ' + r'$f^{(0)}$', color=charcoal, rotation=-22)
	ax1.text(19, 0.9*mse_mfmc_RB_analytic[:, 0][-1], 'MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}$' + ' ' + '(2 RB)', color=color1, rotation=-22)
	ax1.text(17, 1.0*mse_mfmc_RB_analytic[:, 1][-1], 'MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}$' + ' ' + '(8 RB)', color=color2, rotation=-22)
	# ax1.text(20, 1.0*mse_mfmc_RB_analytic[:, 2][-1], 'MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}$' + ' ' + '(50 RB)', color=color3, rotation=-22)
	# ax1.text(1, 2.8e-8, 'CA-MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}_{n_1}$', color=color4, rotation=-55)
	ax1.text(10, 2.3*mse_ca_mfmc_RB_analytic[-1], 'CA-MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}_{n_1}$', color=color4, rotation=-23)
	ax1.text(3, 0.7*mse_ca_mfmc_RB_SVR_analytic[-1], 'CA-MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}_{n_1}, f^{(2)}_{n_2}$', color=color5, rotation=-30)


	ax2.loglog(p[:7], 5e-3*p[:7]**(-1), '-', lw=1.0, color=charcoal)
	ax2.text(1e1, 6e-4, r'$p^{-1}$', color=charcoal)

	ax2.loglog(p, mse_std_mc_computed, linestyle=linestyle1, lw=0.5, marker='*', ms=3, color=charcoal)
	ax2.loglog(p, mse_mfmc_RB_computed[:, 0], linestyle=linestyle2, lw=0.5, marker='s', ms=3, color=color1)
	ax2.loglog(p[1:], mse_mfmc_RB_computed[1:, 1], linestyle=linestyle3, lw=0.5, marker='s', ms=3, color=color2)
	# ax2.loglog(p[2:], mse_mfmc_RB_computed[2:, 2], linestyle=linestyle4, lw=0.5, marker='s', ms=3, color=color3)
	ax2.loglog(p, mse_ca_mfmc_RB_computed, linestyle=linestyle5, lw=0.5, marker='o', ms=3, color=color4)
	ax2.loglog(p[2:], mse_ca_mfmc_RB_SVR_computed[2:], linestyle=linestyle6, lw=0.5, marker='o', ms=3, color=color5)
	ax2.set_xlabel('computational budget p (seconds)')
	ax2.set_ylabel('estimated mean-squared error')


	ax2.text(25, 4.0*mse_std_mc_analytic[-1], 'std. MC:' + ' ' + r'$f^{(0)}$', color=charcoal, rotation=-22)
	ax2.text(19, 1.0*mse_mfmc_RB_analytic[:, 0][-1], 'MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}$' + ' ' + '(2 RB)', color=color1, rotation=-22)
	ax2.text(17, 1.3*mse_mfmc_RB_analytic[:, 1][-1], 'MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}$' + ' ' + '(8 RB)', color=color2, rotation=-22)
	# ax1.text(20, 1.1*mse_mfmc_RB_analytic[:, 2][-1], 'MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}$' + ' ' + '(50 RB)', color=color3, rotation=-25)
	ax2.text(10, 2.9*mse_ca_mfmc_RB_analytic[-1], 'CA-MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}_{n_1}$', color=color4, rotation=-25)
	ax2.text(3, 0.7*mse_ca_mfmc_RB_SVR_analytic[-1], 'CA-MFMC:' + ' ' + r'$f^{(0)}, f^{(1)}_{n_1}, f^{(2)}_{n_2}$', color=color5, rotation=-30)

	ylim = ax2.get_ylim()

	print(ylim)

	ax1.set_ylim(ylim)


	x_pos_all 	= [1, 10, 100, 500]
	labels 		= [1, 10, 100, 500]
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)
	
	tight_layout()

	#show()

	savefig('figures/TB_RB_SVR_MSE.pdf', pad_inches=3)
	close()