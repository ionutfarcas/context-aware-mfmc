import numpy as np
from matplotlib.pyplot import *
from math import trunc

if __name__ == '__main__':

	w1     	= 0.1150
	
	p 			= np.array([1e1, 3e1, 5e1, 8e1, 1e2, 3e2, 5e2, 8e2, 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6]) 
	n_star_RB  	= np.array([19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], dtype=float)
	n_star_SVR  = np.array([17, 48, 72, 98, 112, 192, 220, 240, 247, 276, 280, 284, 284, 284, 284], dtype=float)

	p -= w1*n_star_RB


	rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
	rc("text", usetex=True)         # Crisp axis ticks
	rc("font", family="serif")      # Crisp axis labels
	rc("legend", edgecolor='none')  # No boxes around legends
	rcParams["figure.figsize"] = (9, 3)
	rcParams.update({'font.size': 9})

	# line settings for white base
	charcoal    = [0.2, 0.2, 0.2]
	color1      = '#d95f02'
	color2      = '#7570b3'
	color3 		= '#377eb8'

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

	# ax1.semilogx(p, n_star_RB, linestyle='--', marker='s', color=charcoal, lw=1.0, ms=3)
	ax1.semilogx(p, n_star_SVR, linestyle='--', marker='o', color=charcoal, lw=1.0, ms=3)
	ax1.set_xlabel('computational budget ' + r'$p - n_1^*$' + ' ' + '(seconds)')
	ax1.set_ylabel('hi-fi evaluations needed to construct ' + ' ' + r'$f_{n_2}^{(2)}$')

	# ax1.text(1e3, 25, r'$n_1^*$' + ' ' + '(reduced-basis low-fidelity model, ' + ' ' + r'$f^{(1)}_{n_1}$' + ')', color=charcoal)
	# ax1.text(2e3, 290, r'$n_2^*$' + ' ' + '(' + r'$\epsilon$' + '-SVR regression low-fidelity model, ' + ' ' + r'$f^{(2)}_{n_2}$' + ')', color=color2)

	ax1.text(1e3, 1.04*n_star_SVR[-1], r'$n_2^*$' + ' ' + 'for CA-MFMC: ' + ' ' r'$f^{(0)}, f^{(1)}_{n_1}, f^{(2)}_{n_2}$', color=charcoal)


	x_pos_all 	= [10, 100, 1000, 10000, 100000, 1000000]
	labels 		= [r'$10^{1}$', r'$10^{2}$', r'$10^{3}$', r'$10^{4}$', r'$10^{5}$', r'$10^{6}$']
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)

	y_pos_all 	= [10, 100, 200, 284, 300]
	labels 		= ['10', '100', '200', '284', '']
	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)

	ax1.axhline(y=284, linestyle=':', lw=0.75, color=charcoal)



	p 			= np.array([10, 30, 50, 80, 100, 300, 500]) 
	n_hi_fi 	= np.array([87, 261, 435, 696, 870, 2609, 4348])
	n1_star    	= np.array([19, 19, 20, 20, 20, 20, 20], dtype=float)
	n2_star    	= np.array([17, 48, 72, 98, 112, 192, 220])
	w1 			= 0.1150

	online_budget 		= n_hi_fi - n1_star - n2_star
	online_budget_int 	= p - w1*n1_star - w1*n2_star

	p_labels = ['%.2E' % p_ for p_ in online_budget_int]

	N_lo_fi_1 	= 100 * n1_star/n_hi_fi
	N_lo_fi_2 	= 100 * n2_star/n_hi_fi
	N_hi_fi 	= 100 - N_lo_fi_1 - N_lo_fi_2

	r = range(len(n_hi_fi))


	barWidth = 0.35

	lo_fi 	= ax2.bar(r, N_lo_fi_1 + N_lo_fi_2, color='grey', edgecolor='white', width=barWidth)
	hi_fi 	= ax2.bar(r, N_hi_fi, bottom=N_lo_fi_1 + N_lo_fi_2, color=color3, edgecolor='white', width=barWidth) 

	
	# Custom x ax2is
	ax2.set_xticks(r)
	ax2.set_xticklabels(p)
	ax2.set_xlabel('computational budget p (seconds)')
	ax2.set_ylabel('offline/online computational budget split')

	legend = ax2.legend((lo_fi[0], hi_fi[0]), \
				('offline budget' + ' ' + r'$n_1^* + n_2^*$', 'online budget' + ' ' + r'$p - (n_1^* + n_2^*)$'), \
				loc='upper center', bbox_to_anchor=(0.48, 1.15), frameon=False, ncol=2)

	colors = ['grey', color3]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])

	x_pos_all 	= range(len(p))
	labels 		= [10, 30, 50, 80, 100, 300, 500]
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)

	y_pos_all 	= [0, 25, 50, 75, 100]
	labels 		= [r'$0 \%$', r'$25 \%$', r'$50 \%$', r'$75 \%$', r'$100 \%$']
	ax2.set_yticks(y_pos_all)
	ax2.set_yticklabels(labels)


	tight_layout()

	#show()

	savefig('figures/TB_SVR_n_star_offline_online.pdf', pad_inches=3)
	close()