import numpy as np
import matplotlib as mpl 
from matplotlib.lines import Line2D	
mpl.use('TkAgg')
from matplotlib.pyplot import *
import matplotlib.ticker as mticker

if __name__ == '__main__':
	
	N_acc       	= np.array([100, 500, 1000, 2000, 3000, 5000, 6000, 7000, 8000, 10000, 12000, 15000, 18000, 20000])
	N_cost       	= np.array([100, 500, 1000, 2000, 3000, 5000, 6000, 7000, 8000, 10000, 12000, 15000, 18000, 20000])
	acc_rate_ev 	= np.array([0.101993823291195, 0.061583252959683, 0.049904995523059, 0.034811265146244, 0.030767113814480, \
								0.026192067544799, 0.019210429518349, 0.020036329679951, 0.017926439923276, 0.014946814659021, \
								0.014436265091090, 0.014315177418738, 0.015918092871568, 0.013982154885055])
	cost_rate_ev    = np.array([1.244208695652174e-05, 2.888782608695652e-05, 5.565408695652174e-05, 8.130730434782606e-05, 9.268452173913042e-05, \
							1.062326956521739e-04, 1.250798260869565e-04, 1.286368695652174e-04, 1.338290434782608e-04, 1.921278260869566e-04, \
							2.551445217391304e-04, 2.107680000000000e-04, 3.027869565217391e-04, 2.060504347826087e-04])

	acc_p 	= np.array([0.730921645355709, 0.405311750067212])
	cost_p 	= np.array([9.324558100773368e-07, 0.569586576788161])


	acc_rate 	= lambda N: acc_p[0]*N**(-acc_p[1])
	cost_rate 	= lambda N: cost_p[0]*N**(cost_p[1])


	f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
	g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.4e' % x))
	fmt = mticker.FuncFormatter(g)

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


	ax1.loglog(N_acc, acc_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$1 - \rho_2^2$')
	ax1.loglog(N_acc, acc_rate(N_acc), linestyle='-', lw=0.75, color=color1, label=r'$r_{a,2}(n_2) = $' + ' ' + r'$ {{{:.4}}} \times \strut n_{{2}}^{{{:.4}}}$'.format(acc_p[0], -acc_p[1]))
	ax1.set_xlabel('no. of hi-fi evaluations ' + r'$n_2$')
	
	legend = ax1.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color1]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	x_pos_all 	= [100, 1000, 5000, 20000]
	labels 		= [100, 1000, 5000, 20000]
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)

	y_pos_all 	= [1e-1, 1e-2, 5e-3]
	labels 		= [r'$1 \times 10^{-1}$', r'$2 \times 10^{-2}$', r'$5 \times 10^{-3}$']
	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)


	# ax2.loglog(N_cost, cost_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$\bar{w}_2$')
	ax2.loglog(N_cost, cost_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$w_2$')
	ax2.loglog(N_cost, cost_rate(N_cost), linestyle='-', lw=0.75, color=color2, label=r'$r_{c,2}(n_2) =$' + ' ' + r'$9.3245 \times 10^{{-7}} \times \strut n_{{2}}^{{{:.4}}}$'.format(cost_p[1]))
	ax2.set_xlabel('no. of hi-fi evaluations ' + r'$n_2$')
	
	legend = ax2.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color2]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	x_pos_all 	= [100, 1000, 5000, 20000]
	labels 		= [100, 1000, 5000, 20000]
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)

	y_pos_all 	= [1e-3, 1e-4, 1e-5]
	labels 		= [r'$10^{-3}$', r'$10^{-4}$', r'$10^{-5}$']
	ax2.set_yticks(y_pos_all)
	ax2.set_yticklabels(labels)


	tight_layout()

	#show()

	savefig('figures/TB_SVR_lo_fi_model_rates.pdf', pad_inches=3)
	close()