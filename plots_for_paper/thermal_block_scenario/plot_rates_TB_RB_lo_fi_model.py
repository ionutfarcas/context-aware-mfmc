import numpy as np
import matplotlib as mpl 
from matplotlib.lines import Line2D	
mpl.use('TkAgg')
from matplotlib.pyplot import *

if __name__ == '__main__':
	
	N_acc       = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 25])
	N_cost      = np.linspace(15, 33, 19)
	acc_rate_ev = np.array([0.139116608272340, 0.141082876470913, 0.0755202331262587, 0.0920732315030008, 0.0566141257562317, \
							0.0253720732311076, 0.0448153868550806, 0.0128276322464108, 0.00460034845389956, 0.00499833268576022, \
							0.00410670520939116, 0.00113715454664742, 0.000456359193173661, 0.000189344697781868, 0.000328316306367427, \
							8.49209016040575e-05, 2.34307310355009e-05, 9.24178961014821e-06, 1.71655594172204e-06, 2.85308124126082e-07]);
	cost_rate_ev    = np.array([0.000401677739130439, 0.000387286521739128, 0.000415694173913047, 0.000419178956521741, 0.000434296347826089, \
								0.000428873130434783, 0.000455027130434779, 0.000447882086956518, 0.000470553652173910, 0.000467042173913043, \
								0.000496735217391308, 0.000497683217391308, 0.000519957304347824, 0.000501966521739133, 0.000545490695652170, \
								0.000538927391304341, 0.000571243565217390, 0.000543962869565212, 0.000593329913043476])

	acc_p 	= np.array([0.164755097727376, 0.036466590444116, 1.885858754288085])
	cost_p 	= np.array([8.812465314363537e-05, 0.538023318720777])


	acc_rate 	= lambda N: acc_p[0]*np.exp(-acc_p[1]*N**(acc_p[2]))
	cost_rate 	= lambda N: cost_p[0]*N**(cost_p[1])


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


	ax1.loglog(N_acc, acc_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$1 - \rho_1^2$')
	ax1.loglog(N_acc, acc_rate(N_acc), linestyle='-', lw=0.75, color=color1, label=r'$r_{a,1}(n_1) = $' + ' ' +  r'${{{:.4}}} \times \strut {{e}}^{{( {{{:.3}}} \times n_{{1}}^{{{:.4}}} )}} $'.format(acc_p[0], -acc_p[1], acc_p[2]))
	ax1.set_xlabel('no. of hi-fi evaluations ' + r'$n_1$')
	
	legend = ax1.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color1]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	x_pos_all 	= [2, 5, 10, 20, 30]
	labels 		= [2, 5, 10, 20, 30]
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)

	y_pos_all 	= [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
	labels 		= [r'$10^{-1}$', r'$10^{-2}$', r'$10^{-3}$', r'$10^{-4}$', r'$10^{-5}$', r'$10^{-6}$', r'$10^{-7}$']
	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)

	
	# ax2.loglog(N_cost, cost_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$\bar{w}_1$')
	ax2.loglog(N_cost, cost_rate_ev, linestyle='None', marker='o', ms=3, color=charcoal, label=r'$w_1$')
	ax2.loglog(N_cost, cost_rate(N_cost), linestyle='-', lw=0.75, color=color2, label=r'$r_{c,1}(n_1) = $' + ' ' +  r'${{8.8124 \times 10^{{-5}}}} \times \strut n_{{1}}^{{{:.4}}}$'.format(cost_p[1]))
	ax2.set_xlabel('no. of hi-fi evaluations ' + r'$n_1$')
	
	legend = ax2.legend(loc='best', frameon=True, framealpha=0.5)
	colors = [charcoal, color2]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	x_pos_all 	= [15, 20, 25, 30, 35]
	labels 		= [15, 20, 25, 30, 35]
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)

	y_pos_all 	= [6e-4, 5e-4, 4e-4]
	labels 		= [r'$6 \times 10^{-4}$', r'$5 \times 10^{-4}$', r'$4 \times 10^{-4}$']
	ax2.set_yticks(y_pos_all)
	ax2.set_yticklabels(labels)

	ylim 		= list(ax1.get_ylim())
	ylim[0] 	= 1e-9
	ax1.set_ylim(ylim)

	ylim 		= list(ax2.get_ylim())
	ylim[1] 	= 7e-4
	ax2.set_ylim(ylim)


	tight_layout()

	#show()

	savefig('figures/TB_RB_lo_fi_model_rates.pdf', pad_inches=3)
	close()