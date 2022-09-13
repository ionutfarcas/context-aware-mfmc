import numpy as np
import matplotlib as mpl 
from matplotlib.lines import Line2D	
mpl.use('TkAgg')
from matplotlib.pyplot import *


if __name__ == '__main__':

	temp 	= np.load('results/ML_lo_fi_model_rate_params.npz')
	acc_p 	= temp['acc_params']
	cost_p 	= temp['cost_params']



	hi_fi_runtime = 410.9941333333333


	acc_rate_ev 	= np.load('results/ML_lo_fi_model_acc_rate_eval.npy')
	cost_rate_ev 	= np.load('results/ML_lo_fi_model_cost_rate_eval.npy')


	

	acc_rate 	= lambda n: acc_p[0] * n ** (-acc_p[1])
	cost_rate 	= lambda n: cost_p[0] * n ** (cost_p[1])

	n_acc     	= np.array([250, 500, 1100, 1300, 1500, 1800, 2300, 3000, 4000])
	n_acc_dense = np.linspace(np.min(n_acc), np.max(n_acc), 100)

	n_cost     	 = np.array([250, 500, 1100, 1300, 1500, 1800, 2300, 3000, 4000])
	n_cost_dense = np.linspace(np.min(n_cost), np.max(n_cost), 100)


	rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
	rc("text", usetex=True)         # Crisp axis ticks
	rc("font", family="serif")      # Crisp axis labels
	# rc("legend", edgecolor='none')  # No boxes around legends
	rcParams["figure.figsize"] = (6, 3)
	rcParams.update({'font.size': 8})

	# line settings for white base
	charcoal    = [0.0, 0.0, 0.0]
	color1      = '#d95f02'
	color2      = '#7570b3'

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


	ax1.loglog(n_acc, acc_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$1 - \rho_3^2$')
	ax1.loglog(n_acc_dense, acc_rate(n_acc_dense), linestyle='-', lw=0.75, color=color1, label=r'$r_{a,3}(n_3) = $' + r'${{{:.4}}} \times \strut n_{{3}}^{{{:.4}}}$'.format(acc_p[0], -acc_p[1]))
	ax1.set_xlabel('no. of hi-fi evaluations ' + r'$n_3$')
	
	legend = ax1.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color1]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])


	# ax2.loglog(n_cost, cost_rate_ev/hi_fi_runtime, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$\bar{w}_3$')
	ax2.loglog(n_cost, cost_rate_ev/hi_fi_runtime, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$w_3$')
	ax2.loglog(n_cost_dense, cost_rate(n_cost_dense), linestyle='-', lw=0.75, color=color2, label=r'$r_{c,3}(n_3) = $' + r'$3.6664 \times 10^{{-7}} \times \strut n_{{3}}^{{{:.3}}}$'.format(cost_p[1]))
	ax2.set_xlabel('no. of hi-fi evaluations ' + r'$n_3$')
	
	legend = ax2.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color2]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	ax1.set_xlim([200, 5000])
	ax2.set_xlim([200, 5000])

	ax2.set_ylim([4.45e-7, 5.6e-7])



	x_pos_all 	= np.array([250, 500, 1000, 2000, 4000], dtype=int)
	labels 		= [250, 500, 1000, 2000, 4000]
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)

	x_pos_all 	= np.array([250, 500, 1000, 2000, 4000], dtype=int)
	labels 		= [250, 500, 1000, 2000, 4000]
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)


	y_pos_all 	= np.array([5e-2, 4e-2, 3e-2, 2e-2])
	labels 		= np.array([r'$5 \times 10^{-2}$', r'$4 \times 10^{-2}$', r'$3 \times 10^{-2}$', r'$2 \times 10^{-3}$'])
	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)


	y_pos_all 	= np.array([4.6e-7, 4.8e-7, 5e-7, 5.2e-7, 5.4e-7, 5.6e-7])
	labels 		= [r'$4.6 \times 10^{-7}$', r'$4.8 \times 10^{-7}$', r'$5 \times 10^{-7}$', r'$5.2 \times 10^{-7}$', r'$5.4 \times 10^{-7}$', r'$5.6 \times 10^{-7}$']
	ax2.set_yticks(y_pos_all)
	ax2.set_yticklabels(labels)


	tight_layout()

	#plt.show()

	savefig('figures/AUG_ML_lo_fi_model_rates.pdf', pad_inches=3)
	close()