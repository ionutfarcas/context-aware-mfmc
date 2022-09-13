import numpy as np
import matplotlib as mpl 
from matplotlib.lines import Line2D	
mpl.use('TkAgg')
from matplotlib.pyplot import *

def sci_notation(num, decimal_digits=1, precision=None, exponent=None):
 
    if exponent is None:
        exponent = int(np.floor(np.log10(np.abs(num))))

    coeff = np.round(num / float(10**exponent), decimal_digits)
    
    if precision is None:
        precision = decimal_digits

    return r"${0:.{2}f}\times10^{{{1:d}}}$".format(coeff, exponent, precision)



if __name__ == '__main__':

	# MSEs
	MSE = [1.4430638909629904e-05, 1.6410271501601725e-06, 3.4685194443360736e-07, 1.707231050255703e-07, 2.0127226767446525e-07]
	x   = range(len(MSE))

	# std MC
	N_std_MC 	= np.array([1216, 0, 0, 0])
	perc_MC 	= 100*np.array([item/np.sum(N_std_MC) for item in N_std_MC]) 

	# MFMC
	N_MFMC 		= np.array([155, 12508, 0, 0])
	perc_MFMC 	= 100*np.array([item/np.sum(N_MFMC) for item in N_MFMC])

	# CAMFMC 1
	N_CAMFMC_1 		= np.array([548, 0, 734464, 0])
	perc_CAMFMC_1 	= 100*np.array([item/np.sum(N_CAMFMC_1) for item in N_CAMFMC_1])

	# CAMFMC 2
	N_CAMFMC_2 		= np.array([565, 4114, 2102057, 0])
	perc_CAMFMC_2 	= 100*np.array([item/np.sum(N_CAMFMC_2) for item in N_CAMFMC_2])

	# CAMFMC 3
	N_CAMFMC_3 		= np.array([342, 8323, 0, 16158025])
	perc_CAMFMC_3 	= 100*np.array([item/np.sum(N_CAMFMC_3) for item in N_CAMFMC_3])


	data = np.vstack((perc_MC, perc_MFMC, perc_CAMFMC_1, perc_CAMFMC_2, perc_CAMFMC_3)).T
	
	rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
	rc("text", usetex=True)         # Crisp axis ticks
	rc("font", family="serif")      # Crisp axis labels
	rc("legend", edgecolor='none')  # No boxes around legends
	rcParams["figure.figsize"] = (9.5, 4)
	rcParams.update({'font.size': 10})

	# line settings for white base
	charcoal    = [0.0, 0.0, 0.0]
	color1      = '#E69F00'
	color2      = '#D55E00'
	color3      = '#CC79A7'
	color4      = '#74a9cf'
	color5 		= '#0570b0' 
	color6 		= '#0c2c84' 

	colors = [charcoal, color2, color4, color5, color6]


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

	w 		= 0.2
	
	x_pos_all   = np.array([0, 1, 2, 3, 4])
	labels      = [r'std. MC:' + '\n'  + r'$f^{(0)}$', 
					r'MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(2)}_{n_2}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}, f^{(2)}_{n_2}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}, f^{(3)}_{n_3}$']


	bars = ax1.bar(x, MSE, w, color=colors)
	ax1.set_yscale('log')
	ax1.set_xticks(x_pos_all)
	ax1.set_xticklabels(labels, rotation=45)

	[t.set_color(colors[i]) for i, t in enumerate(ax1.xaxis.get_ticklabels())]


	for i, bar in enumerate(bars):
		y_val = bar.get_height()	

		x_height 	= (bar.get_x() - 0.5) * (i <= 2) + (bar.get_x() - 0.6) * (i == 3)  + (bar.get_x() - 0.4) * (i == 4) 
		y_height 	= 1.2*y_val * (i <= 3) + 1.8*y_val  * (i == 4)

		ax1.text(x_height, y_height, sci_notation(y_val, 4), color=colors[i])

	y_pos_all   = np.array([1e-5, 1e-6, 1e-7, 1e-8])
	labels      = [r'$10^{-5}$', r'$10^{-6}$', r'$10^{-7}$', r'$10^{-8}$']

	ax1.set_yticks(y_pos_all)
	ax1.set_yticklabels(labels)

	ax1.set_xlim([-0.7, 4.2])
	ax1.set_xlim([-0.7, 4.2])

	ax1.set_ylabel('estimated mean-squared error')


	w 		= 0.1
	colors 	= [get_cmap('pink')(0.6), get_cmap('pink')(0.5), get_cmap('pink')(0.3), get_cmap('pink')(0.2)]


	# sample distr
	ny 	= len(data[0])
	ind = list(range(ny))

	axes 		= []
	cum_size 	= np.zeros(ny)

	yscale('log')
	ylim((5e-5, 100))


	models = [r'$f^{(0)}$', r'$f^{(1)}$', r'$f^{(2)}_{n_2}$', r'$f^{(3)}_{n_3}$']

	for i, row_data in enumerate(data):
	    axes.append(ax2.bar(ind, row_data, bottom=cum_size, label=models[i],
	                        color=colors[i]))
	    cum_size += row_data

	for axis in axes:
	        for bar in axis:
	            w, h = bar.get_width(), bar.get_height()
	            if h > 1e-5:
	                string = r'$\mathsf {{{:.4f}}} $ \%'.format(h)

	                ax2.text(bar.get_x() + w/2, bar.get_y() + h/2,
	                         string, ha="center",
	                         va="center", weight='bold', fontsize=8)


	x_pos_all   = np.array([0, 1, 2, 3, 4])
	labels      = [r'std. MC:' + '\n'  + r'$f^{(0)}$', 
					r'MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(2)}_{n_2}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}, f^{(2)}_{n_2}$', \
					r'CA-MFMC:' + '\n' + r'$f^{(0)}, f^{(1)}, f^{(3)}_{n_3}$']

	ax2.set_ylabel( 'samples distribution ' + ' ' + '(' + r'$\%$' + ')')


	ax2.set_xticks(x_pos_all)
	ax2.set_xticklabels(labels, rotation=45)



	y_pos_all   = np.array([100, 10, 1, 1e-1, 1e-2, 1e-3, 1e-4, 5e-5])
	labels      = [r'$100$', r'$10$', r'$1$', r'$10^{-1}$', \
					r'$10^{-2}$', r'$10^{-3}$', r'$10^{-4}$', '']

	ax2.set_yticks(y_pos_all)
	ax2.set_yticklabels(labels)


	ax2.legend((axes[0], axes[1], axes[2], axes[3]), \
				(models[0], models[1], models[2], models[3]), loc=3, frameon=True, shadow=False, edgecolor='white')

	color1      = '#E69F00'
	color2      = '#D55E00'
	color3      = '#CC79A7'
	color4      = '#74a9cf'
	color5 		= '#0570b0' 
	color6 		= '#0c2c84' 
	colors 		= [charcoal, color2, color4, color5, color6]

	[t.set_color(colors[i]) for i, t in enumerate(ax2.xaxis.get_ticklabels())]

	tight_layout()

	#plt.show()

	savefig('figures/AUG_sample_MSE_and_distribution.pdf', pad_inches=3)
	close()