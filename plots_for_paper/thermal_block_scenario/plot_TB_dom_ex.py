from matplotlib.pyplot import *
import numpy as np
import pandas

from matplotlib.table import Table

def checkerboard_table(fig, ax, data, fmt='{:.2f}', bkg_color='white'):
    tb = Table(ax, bbox=[0,0,1,1])

    nrows, ncols = (3, 3)
    width, height = 1.0 / ncols, 1.0 / nrows

    color = bkg_color

    # Add cells
    for i in range(3):
        for j in range(3):

            val = data[i][j]

            tb.add_cell(i, j, width, height, text=val, loc='center', facecolor=color)
            tb.set_fontsize(50)

        ax.add_table(tb)

        ax.text(0.5,  1.02, r'$\Gamma_{D}$', fontsize=45)
        ax.text(0.5, -0.10, r'$\Gamma_{N_1}$', fontsize=45)
        ax.text(1.02, 0.5, r'$\Gamma_{N_0}$', fontsize=45)

        arrow(0.2, -0.2, 0.0, 0.1)

if __name__ == '__main__':

    data = [[r'$\Omega_7$', r'$\Omega_8$', r'$\Omega_9$'], [r'$\Omega_4$', r'$\Omega_5$', r'$\Omega_6$'], [r'$\Omega_1$', r'$\Omega_2$', r'$\Omega_3$']]

    rc("figure", dpi=400)           # High-quality figure ("dots-per-inch")
    rc("text", usetex=True)         # Crisp axis ticks
    rc("font", family="serif")      # Crisp axis labels
    # rc("legend", edgecolor='none')  # No boxes around legends
    rcParams["figure.figsize"] = (10, 10)
    rcParams.update({'font.size': 8})

    charcoal    = [0., 0., 0.]

    rc("figure",facecolor='w')
    rc("axes",facecolor='w',edgecolor=charcoal,labelcolor=charcoal)
    rc("savefig",facecolor='w')
    rc("text",color=charcoal)
    rc("xtick",color=charcoal)
    rc("ytick",color=charcoal)


      
    fig, ax = subplots()
    ax.set_axis_off()

    checkerboard_table(fig, ax, data)
    
    # tight_layout()

    #show()

    savefig('figures/TB_domain_ex.png', pad_inches=3)
    close()