import numpy as np
import matplotlib as mpl 
from matplotlib.lines import Line2D	
mpl.use('TkAgg')
from matplotlib.pyplot import *

if __name__ == '__main__':

	temp 	= np.load('results/SG_lo_fi_model_rate_params.npz')
	acc_p 	= temp['acc_params']
	cost_p 	= temp['cost_params']

	hi_fi_runtime = 410.9941333333333


	acc_rate_ev 	= np.load('results/SG_lo_fi_model_acc_rate_eval.npy')
	cost_rate_ev 	= np.load('results/SG_lo_fi_model_cost_rate_eval.npy')

	acc_rate 	= lambda n: acc_p[0] * n ** (-acc_p[1])
	cost_rate 	= lambda n: cost_p[0] * n ** (cost_p[1])

	print(acc_p)
	print(cost_p)

	n_acc_cost     = np.load('results/SG_lo_fi_model_n_hi_fi_evals.npy')
	n_dense 	   = np.linspace(np.min(n_acc_cost), np.max(n_acc_cost), 100)



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


	ax1.loglog(n_acc_cost, acc_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$1 - \rho_2^2$')
	ax1.loglog(n_dense, acc_rate(n_dense), linestyle='-', lw=0.75, color=color1, label=r'$r_{a,2}(n_2) = $' + r'${{{:.4}}} \times \strut n_{{2}}^{{{:.4}}}$'.format(acc_p[0], -acc_p[1]))
	ax1.set_xlabel('no. of hi-fi evaluations ' + r'$n_2$')
	
	legend = ax1.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color1]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])


	# ax2.loglog(n_acc_cost, cost_rate_ev/hi_fi_runtime, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$\bar{w}_2$')
	ax2.loglog(n_acc_cost, cost_rate_ev/hi_fi_runtime, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$w_2$')
	ax2.loglog(n_dense, cost_rate(n_dense), linestyle='-', lw=0.75, color=color2, label=r'$r_{c,2}(n_2) = $' + r'$2.906 \times 10^{{-7}} \times \strut n_{{2}}^{{{:.4}}}$'.format(cost_p[1]))
	ax2.set_xlabel('no. of hi-fi evaluations ' + r'$n_2$')
	
	legend = ax2.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color2]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	ax1.set_xlim([1e1, 1.1e3])
	ax2.set_xlim([1e1, 1.1e3])

	ax1.set_ylim([5e-4, 1e-1])
	ax2.set_ylim([2e-6, 1.1e-3])



	x_pos_all 	= np.array([10, 100, 1000], dtype=int)
	labels 		= [10, 100, 1000]
	
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)


	# y_pos_all 	= np.array([1e0, 1e-1, 1e-2, 1e-3, 1e-4])
	# labels 		= np.array([r'$10^{0}$', r'$10^{-1}$', r'$10^{-2}$', r'$10^{-3}$', r'$10^{-4}$'])
	# ax1.set_yticks(y_pos_all)
	# ax1.set_yticklabels(labels)


	# y_pos_all 	= np.array([0.2, 0.3, 0.4, 0.6, 0.9])
	# labels 		= ['0.2', '0.3', '0.4', '0.6', '0.9']
	# ax2.set_yticks(y_pos_all)
	# ax2.set_yticklabels(labels)


	tight_layout()

	#show()

	savefig('figures/AUG_SG_lo_fi_model_rates.pdf', pad_inches=3)
	close()