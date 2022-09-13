import numpy as np
from matplotlib.pyplot import *
from math import trunc

if __name__ == '__main__':
	
	p 							= np.array([1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9, 5e9, 1e10])
	p_ML 						= np.array([1e5, 5e5, 1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14, 1e15, 1e16, 1e17, 1e18])
	n_star_SG   				= np.load('results/SG_n_star.npy')
	n_star_SG_after_Red_Phys 	= np.load('results/SG_after_Red_Phys_n_star.npy')
	n_star_ML_after_Red_Phys 	= np.load('results/ML_after_Red_Phys_n_star_large_budgets.npy')

	print(n_star_SG)
	print(n_star_SG_after_Red_Phys)


	rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
	rc("text", usetex=True)         # Crisp axis ticks
	rc("font", family="serif")      # Crisp axis labels
	rc("legend", edgecolor='none')  # No boxes around legends
	rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
	rcParams["figure.figsize"] = (6, 3)
	rcParams.update({'font.size': 8})

	# line settings for white base
	charcoal    = [0.0, 0.0, 0.0]
	color1      = '#d95f02'
	color2      = '#7570b3'
	color3 		= '#377eb8'

	color11     = '#E69F00'
	color21     = '#D55E00'
	color31     = '#CC79A7'
	color41     = '#74a9cf'
	color51 	= '#0570b0' 
	color61 	= '#0c2c84' 


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

	ax1.semilogx(p, n_star_SG, linestyle='--', marker='o', color=charcoal, lw=1.0, ms=3)
	ax1.semilogx(p, n_star_SG_after_Red_Phys, linestyle='-.', marker='s', color=charcoal, lw=1.0, ms=3)
	# ax1.semilogx(p, n_star_ML_after_Red_Phys, linestyle='-.', marker='s', color=color2, lw=1.0, ms=3)
	ax1.set_xlabel('computational budget p (seconds)')
	ax1.set_ylabel('quasi-optimal no. of needed hi-fi evaluations')


	ax1.semilogx(p[1], n_star_SG[1], linestyle='none', marker='o', color=color41, lw=1.0, ms=3)
	ax1.semilogx(p[1], n_star_SG_after_Red_Phys[1], linestyle='none', marker='s', color=color51, lw=1.0, ms=3)

	ax1.text(5e6, 1.02*n_star_SG[-1], r'$n_2^*$: ' + ' ' + 'for CA-MFMC: ' + ' '  r'$f^{(0)}, f^{(2)}_{n_2}$', color=charcoal)
	ax1.text(9e5, 1.06*n_star_SG_after_Red_Phys[-1], r'$n_2^*$: ' + ' ' + 'for CA-MFMC: ' + ' '  r'$f^{(0)}, f^{(1)}, f^{(2)}_{n_2}$', color=charcoal)


	ax1.text(2e5, 0.87*n_star_SG[1], r'$n_2^* = $' + str(n_star_SG[1]), color=color41, rotation=70)
	ax1.text(1.5e5, 0.90*n_star_SG_after_Red_Phys[1], r'$n_2^* = $' + str(n_star_SG_after_Red_Phys[1]), color=color51, rotation=27)


	ax1.axhline(y=n_star_SG[-1], linestyle=':', lw=0.75, color=charcoal)
	ax1.axhline(y=n_star_SG_after_Red_Phys[-1], linestyle=':', lw=0.75, color=charcoal)

	
	ax2.semilogx(p_ML, n_star_ML_after_Red_Phys, linestyle='-.', marker='s', color=charcoal, lw=1.0, ms=3)
	ax2.set_xlabel('computational budget p (seconds)')
	ax2.set_ylabel('quasi-optimal no. of needed hi-fi evaluations')

	ax2.semilogx(5e5, n_star_ML_after_Red_Phys[1], linestyle='none', marker='s', color=color61, lw=1.0, ms=3)

	ax2.text(5e7, 1.02*n_star_ML_after_Red_Phys[-1], r'$n_3^*$: ' + ' ' + 'for CA-MFMC: ' + ' ' r'$f^{(0)}, f^{(1)}, f^{(3)}_{n_3}$', color=charcoal)

	n_star_ML = n_star_ML_after_Red_Phys[1]
	ax2.text(1e5, 3e8, r'$n_3^* = $' + str(n_star_ML_after_Red_Phys[1]), color=color61)

	ax2.axhline(y=n_star_ML_after_Red_Phys[-1], linestyle=':', lw=0.75, color=charcoal)


	x_pos_all 	= [5e5, 1e7, 1e8, 1e9, 1e10]
	labels 		= [r'$\boldsymbol{5\times10^5}$', r'$10^{7}$', r'$10^8$', r'$10^{9}$', r'$10^{10}$']
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels)

	x_pos_all 	= [5e5, 1e9, 1e12, 1e15, 1e18]
	labels 		= [r'$\boldsymbol{5 \times 10^5}$', r'$10^{9}$', r'$10^{12}$', r'$10^{15}$', r'$10^{18}$']
	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels)

	y_pos_all 	= [50, 100, 265, 500, 700, 904]
	labels 		= [50, 100, 265, 500, 700, 904]
	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)


	tight_layout()

	#show()

	savefig('figures/AUG_n_star.pdf', pad_inches=3)
	close()