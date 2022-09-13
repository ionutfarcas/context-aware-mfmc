import numpy as np
from matplotlib.pyplot import *
from math import trunc

if __name__ == '__main__':
	
	p 			= np.array([1, 5, 10, 30, 50, 80, 100, 300, 500]) 
	n_hi_fi 	= np.array([9, 44, 87, 261, 435, 696, 870, 2609, 4348])
	n_star    	= np.array([3, 18, 19, 19, 19, 19, 19, 20, 20], dtype=float)

	w1 			= 0.1150

	online_budget 		= n_hi_fi - n_star
	online_budget_int 	= p - w1*n_star

	p_labels = ['%.2E' % p_ for p_ in online_budget_int]

	N_lo_fi = 100 * n_star/n_hi_fi
	N_hi_fi = 100 - N_lo_fi

	r = range(len(n_hi_fi))


	rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
	rc("text", usetex=True)         # Crisp axis ticks
	rc("font", family="serif")      # Crisp axis labels
	rc("legend", edgecolor='none')  # No boxes around legends
	rcParams["figure.figsize"] = (9, 3)
	rcParams.update({'font.size': 10})

	# line settings for white base
	charcoal    = [0.0, 0.0, 0.0]
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

	# ax1.spines['bottom'].set_bounds(0.8, 500)
	# ax1.spines['left'].set_bounds(5, 20)

	ax1.semilogx(p, n_star, linestyle='--', marker='o', color=charcoal, lw=1.0, ms=3)
	ax1.set_xlabel('computational budget p (seconds)')
	ax1.set_ylabel('hi-fi evaluations needed to construct ' + ' ' + r'$f_{n_1}^{(1)}$')

	ax1.text(30, 1.04*n_star[-1], r'$n_1^*$' + ' ' + 'for CA-MFMC: ' + ' ' r'$f^{(0)}, f^{(1)}_{n_1}$', color=charcoal)


	x_pos_all 	= [1, 5, 10, 30, 50, 100, 300, 500]
	labels 		= [1, 5, 10, 30, 50, 100, 300, 500]
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)

	y_pos_all 	= [5, 10, 15, 20]
	labels 		= ['5', '10', '15', '20']
	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)

	ax1.axhline(y=20, linestyle=':', lw=0.75, color=charcoal)


	barWidth = 0.4

	lo_fi 	= ax2.bar(r, N_lo_fi, color='grey', edgecolor='white', width=barWidth)
	hi_fi 	= ax2.bar(r, N_hi_fi, bottom=N_lo_fi, color=color3, edgecolor='white', width=barWidth) 

	# Custom x ax2is
	ax2.set_xticks(r)
	ax2.set_xticklabels(p)
	ax2.set_xlabel('computational budget p (seconds)')
	ax2.set_ylabel('offline/online computational budget split')

	legend = ax2.legend((lo_fi[0], hi_fi[0]), \
				('offline budget' + ' ' + r'$n_1^*$', 'online budget' + ' ' + r'$p - n_1^*$'), \
				loc='upper center', bbox_to_anchor=(0.5, 1.15), frameon=False, ncol=2)


	colors = ['grey', color3]
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colors[i])


	x_pos_all 	= range(len(p))
	labels 		= [1, 5, 10, 30, 50, 80, 100, 300, 500]
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)

	y_pos_all 	= [0, 25, 50, 75, 100]
	labels 		= [r'$0 \%$', r'$25 \%$', r'$50 \%$', r'$75 \%$', r'$100 \%$']
	ax2.set_yticks(y_pos_all)
	ax2.set_yticklabels(labels)



	tight_layout()

	#show()

	savefig('figures/TB_RB_n_star_offline_online.pdf', pad_inches=3)
	close()