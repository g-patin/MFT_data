####### IMPORT PACKAGES #######

import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


from ipywidgets import Layout, Button, Box, interact, interactive, fixed, interact_manual
import ipywidgets as wg
from IPython.display import display, clear_output

import scipy.interpolate as sip
from glob import glob
import imageio

import colour
from colour.plotting import *
from colour.colorimetry import *
from colour.models import *
from colour import SDS_ILLUMINANTS



def MFT(sample, lamp):    
    '''
    Function that displays the micro-fading results on blue wool standard samples.

    Inputs
    ====================================================
    sample: a string
    Description of the sample that has been faded ('BW1','BW2', 'BW3'). 
    
    lamp: a string
    Light source that has used been to fade the sample. Only two light sources have
    been used ('HPX' or 'LED'). See table 1 of the article for more information 
    about these two lamps.

    Returns
    ====================================================
    It returns an ipywidget object composed of several tabs where the micro-fading are being displayed. 
  
    '''
    
    d65 = colour.CCS_ILLUMINANTS["cie_10_1964"]["D65"]
    
    ###### CREATE THE WIDGET TABS #######
    
    out1 = wg.Output()
    out2 = wg.Output()
    out3 = wg.Output()
    out4 = wg.Output()
    out5 = wg.Output()
    out6 = wg.Output()
    out7 = wg.Output()
    out8 = wg.Output()
    out9 = wg.Output()


    tab = wg.Tab(children = [out1,out2,out3,out4,out5,out6,out7,out8,out9])
    tab.set_title(0,'Refl sp')
    tab.set_title(1,'Colour diff')
    tab.set_title(2,'Lab-LCh')
    tab.set_title(3,'CIELAB space')
    tab.set_title(4,'Colour patches')
    tab.set_title(5, 'Colour change slider')
    tab.set_title(6,'Data')
    tab.set_title(7,'Fading beam')
    tab.set_title(8,'Parameters')
    
    file_SP = glob(f'*{sample}*{lamp}*SP*')[0]
    file_dE = glob(f'*{sample}*{lamp}*dE*')[0]
    
    
    ###### CREATE SAVE BUTTON #######
    
    b1 = wg.Button(description='Save plot')
    vbox1 = wg.VBox([b1])
    vbox1bis = wg.Output()
    
    b2 = wg.Button(description='Save plot')
    vbox2 = wg.VBox([b2])
    vbox2bis = wg.Output()
    
    b3 = wg.Button(description='Save plot')
    vbox3 = wg.VBox([b3])
    vbox3bis = wg.Output()
    
    b4 = wg.Button(description='Save plot')
    vbox4 = wg.VBox([b4])
    vbox4bis = wg.Output()
    
    b5 = wg.Button(description='Save plot')
    vbox5 = wg.VBox([b5])
    vbox5bis = wg.Output()
    
  
    b7 = wg.Button(description='Save plot')
    vbox7 = wg.VBox([b7])
    vbox7bis = wg.Output()
    
    with out1:
        
        date = file_SP.split('_')[0]
        Id = file_SP.split('_')[1]
        pigment = file_SP.split('_')[2]
        
        df_SP = pd.read_csv(file_SP, header = [0,1])
        wl = df_SP['time','wavelength_nm'].values
        
        sp_i_n = df_SP['00:00:00.000','mean']/100
        sp_i_s = df_SP['00:00:00.000','std']/100

        sp_f_n = df_SP.iloc[:,-2]/100
        sp_f_s = df_SP.iloc[:,-1]/100
        
        
        fig1, ax = plt.subplots(1,1,figsize = (15,10))
        sns.set()
        fs = 18
        
        ax.plot(wl,sp_i_n, ls = '-', color = 'blue', label = 'initial')
        ax.plot(wl,sp_f_n, ls = '--', color = 'red', label = 'final')
        
        ax.fill_between(wl, sp_i_n - sp_i_s, sp_i_n + sp_i_s, alpha=0.3)
        ax.fill_between(wl, sp_f_n - sp_f_s, sp_f_n + sp_f_s, alpha=0.3)
        
        ax.set_xlim(305,1140)
        ax.set_ylim(0,1)
        
        ax.set_xlabel('Wavelength $\lambda$ (nm)', fontsize = fs)
        ax.set_ylabel('Reflectance factor', fontsize = fs)
        ax.set_title(f'Micro-fading measurement, Reflectance spectra, {sample}, {lamp}',fontsize = fs + 2)
        
        ax.xaxis.set_tick_params(labelsize=fs)
        ax.yaxis.set_tick_params(labelsize=fs)
        
        plt.legend(fontsize = fs)        
        plt.tight_layout()
        plt.show()
        
        def button(_):
            with vbox1bis:
                fig1.savefig(f'{date}_{Id}_{pigment}_SP.png', dpi = 300)
                print('figure saved !')
        
        b1.on_click(button)
        
        display(wg.HBox([vbox2, vbox2bis]))
    
    with out2:
        
        date = file_dE.split('_')[0]
        Id = file_dE.split('_')[1]
        pigment = file_dE.split('_')[2]
        
        df_dE = pd.read_csv(file_dE, header = [0,1])
        
        E_pho = df_dE['cum_klux_hr', 'value']
        E_rad = df_dE['cum_MJ/m2', 'value']
        dE76_mean = df_dE['dE76', 'mean']
        dE76_std = df_dE['dE76', 'std']
        
        dE00_mean = df_dE['dE00', 'mean']
        dE00_std = df_dE['dE00', 'std']
        
        dR_VIS_mean = df_dE['dR_VIS', 'mean']
        dR_VIS_std = df_dE['dR_VIS', 'std']

        fig2, ax = plt.subplots(1,1,figsize = (15,10))
        sns.set()
        ax2 = ax.twiny()
        fs = 18
        
        ax2.plot(E_pho,dE76_mean, ls = '-', color = 'blue', label = '$\Delta E_{76}$')
        ax2.plot(E_pho,dE00_mean, ls = '-', color = 'red', label = '$\Delta E_{00}$')
        ax2.plot(E_pho,dR_VIS_mean, ls = '--', color = 'green', label = '$\Delta R_{VIS}$')
        
        ax.plot(E_rad,dE76_mean, ls = '-', color = 'blue', label = '$\Delta E_{76}$')
        ax.plot(E_rad,dE00_mean, ls = '-', color = 'red', label = '$\Delta E_{00}$')
        ax.plot(E_rad,dR_VIS_mean, ls = '--', color = 'green', label = '$\Delta R_{VIS}$')
        
        ax.fill_between(E_rad, dE76_mean - dE76_std, dE76_mean + dE76_std, alpha=0.3)
        ax.fill_between(E_rad, dE00_mean - dE00_std, dE00_mean + dE00_std, alpha=0.3)
        ax.fill_between(E_rad, dR_VIS_mean - dR_VIS_std, dR_VIS_mean + dR_VIS_std, alpha=0.3)
        
        
        ax.set_xlim(left = 0)
        ax2.set_xlim(left = 0)
        ax.set_ylim(bottom = 0)
        ax2.grid(False)
        
        ax.set_xlabel('Radiant exposure (MJ/m²)', fontsize = fs)
        ax2.set_xlabel('Exposure dose (klux.hr)', fontsize = fs)
        ax.set_ylabel('Colour difference $\Delta$', fontsize = fs)
        ax.set_title(f'Micro-fading measurement, Colour difference equations, {sample}, {lamp}',fontsize = fs + 2)
        
        ax.xaxis.set_tick_params(labelsize=fs)
        ax2.xaxis.set_tick_params(labelsize=fs)
        ax.yaxis.set_tick_params(labelsize=fs)
        
        plt.legend(fontsize = fs)        
        plt.tight_layout()
        plt.show()
        
        def button(_):
            with vbox2bis:
                fig2.savefig(f'{date}_{Id}_{pigment}_dE.png', dpi = 300)
                print('figure saved !')
        
        b2.on_click(button)
        
        display(wg.HBox([vbox2, vbox2bis]))
        
    with out3:
        
        date = file_dE.split('_')[0]
        Id = file_dE.split('_')[1]
        pigment = file_dE.split('_')[2]
        
        df_dE = pd.read_csv(file_dE, header = [0,1])
                
        t = df_dE['time_s', 'value']        
        
        L_mean = df_dE['L*', 'mean']
        L_std = df_dE['L*', 'std']        
        a_mean = df_dE['a*', 'mean']
        a_std = df_dE['a*', 'std']        
        b_mean = df_dE['b*', 'mean']
        b_std = df_dE['b*', 'std']
        C_mean = df_dE['C*', 'mean']
        C_std = df_dE['C*', 'std']        
        h_mean = df_dE['h', 'mean']
        h_std = df_dE['h', 'std']
        
        dL_abs = np.round(L_mean.values[-1] - L_mean.values[0],1)
        da_abs = np.round(a_mean.values[-1] - a_mean.values[0],1)
        db_abs = np.round(b_mean.values[-1] - b_mean.values[0],1)
        dC_abs = np.round(C_mean.values[-1] - C_mean.values[0],1)
        dh_abs = np.round(h_mean.values[-1] - h_mean.values[0],1)
        
        dL_rel = np.round(dL_abs,1)
        da_rel = np.round((da_abs * 100)/120,1)
        db_rel = np.round((db_abs * 100)/120,1)
        dC_rel = np.round((dC_abs * 100)/120,1)
        dh_rel = np.round((dh_abs * 100)/360,1)
        
        fig3, ax4 = plt.subplots(3,1, figsize = (10,10))
        fs = 16

        ax4[0].plot(t/60,L_mean, color = 'blue')
        ax4[0].fill_between(t/60, L_mean - L_std, L_mean + L_std, alpha=0.3)

        ax4[0].set_xlim(left = 0)
        ax4[0].set_ylabel(r'Brigthness (CIE $L^*$)', color = 'blue', fontsize = fs)
        ax4[0].xaxis.set_tick_params(labelsize=fs)
        ax4[0].yaxis.set_tick_params(labelsize=fs)   
        for tl in ax4[0].get_yticklabels():
            tl.set_color('blue')   

        ax5 = ax4[1].twinx()  
        
        ax4[1].plot(t/60,a_mean, color  ='red')
        ax4[1].fill_between(t/60, a_mean - a_std, a_mean + a_std, alpha=0.3)
        
        ax5.plot(t/60,b_mean, color = 'black')
        ax5.fill_between(t/60, b_mean - b_std, b_mean + b_std, alpha=0.3)

        for tl in ax4[1].get_yticklabels():
            tl.set_color('red')

        for tl in ax5.get_yticklabels():
            tl.set_color('black')

        ax5.grid(False)
        ax4[1].set_xlim(left = 0)
        ax4[1].set_ylabel(r'CIE $a^*$', fontsize = fs, color = 'red')
        ax5.set_ylabel(r'CIE $b^*$', fontsize = fs)
        ax4[1].xaxis.set_tick_params(labelsize=fs)
        ax4[1].yaxis.set_tick_params(labelsize=fs) 
        ax5.yaxis.set_tick_params(labelsize=fs) 

        ax6 = ax4[2].twinx()
        ax4[2].plot(t/60,C_mean, color = 'red')
        ax4[2].fill_between(t/60, C_mean - C_std, C_mean + C_std, alpha=0.3)
        ax6.plot(t/60,h_mean, color = 'black')
        ax6.fill_between(t/60, h_mean - h_std, h_mean + h_std, alpha=0.3)

        ax4[2].set_xlim(left = 0)

        for tl in ax4[2].get_yticklabels():
            tl.set_color('red')

        for tl in ax6.get_yticklabels():
            tl.set_color('black')

        ax6.grid(False)
        ax4[2].set_xlabel(r'Exposure time (min)', fontsize = fs)
        ax4[2].set_ylabel(r'Saturation (CIE $C^*$)', fontsize = fs, color = 'red')
        ax6.set_ylabel(r'Hue (CIE $h$)', fontsize = fs)
        ax4[2].xaxis.set_tick_params(labelsize=fs)
        ax4[2].yaxis.set_tick_params(labelsize=fs) 
        ax6.yaxis.set_tick_params(labelsize=fs)
        
        props = dict(boxstyle="round", facecolor="white", alpha=0.5) 
        
        ax4[0].text(
            0.82,
            0.12,
            f'$\Delta L^*$ = {dL_abs} ({dL_rel}%)',
            transform=ax4[0].transAxes,
            fontsize=fs-6,
            verticalalignment="top",
            bbox=props,
        )
        
        ax4[1].text(
            0.02,
            0.12,
            f'$\Delta a^*$ = {da_abs} ({da_rel}%)',
            transform=ax4[1].transAxes,
            fontsize=fs-6,
            verticalalignment="top",
            bbox=props,
        )
        
        ax4[1].text(
            0.82,
            0.12,
            f'$\Delta b^*$ = {db_abs} ({db_rel}%)',
            transform=ax4[1].transAxes,
            fontsize=fs-6,
            verticalalignment="top",
            bbox=props,
        )
        
        ax4[2].text(
            0.02,
            0.12,
            f'$\Delta C^*$ = {dC_abs} ({dC_rel}%)',
            transform=ax4[2].transAxes,
            fontsize=fs-6,
            verticalalignment="top",
            bbox=props,
        )
        
        ax4[2].text(
            0.82,
            0.12,
            f'$\Delta h$ = {dh_abs} ({dh_rel}%)',
            transform=ax4[2].transAxes,
            fontsize=fs-6,
            verticalalignment="top",
            bbox=props,
        )
        
        
        name = 'Micro-fading analysis - Colorimetric values \n' + date +', '+Id+', ' + r"$\bf{" + pigment + "}$"
        plt.suptitle(name,fontsize = fs+2)
        plt.tight_layout(rect = (0,0,1,0.99))
        plt.show()
        
        def button(_):
            with vbox3bis:
                fig3.savefig(f'{date}_{Id}_{pigment}_Lab.png', dpi = 300)
                print('figure saved !')
        
        b3.on_click(button)
        
        display(wg.HBox([vbox3, vbox3bis]))
    
    
    with out4:
        
        date = file_dE.split('_')[0]
        Id = file_dE.split('_')[1]
        pigment = file_dE.split('_')[2]
        
        df_dE = pd.read_csv(file_dE, header = [0,1])
        
        L_mean = df_dE['L*', 'mean']
        L_std = df_dE['L*', 'std']        
        a_mean = df_dE['a*', 'mean']
        a_std = df_dE['a*', 'std']        
        b_mean = df_dE['b*', 'mean']
        b_std = df_dE['b*', 'std']
        
        lab = np.array([L_mean, a_mean, b_mean]).transpose()
        srgb = colour.XYZ_to_sRGB(colour.Lab_to_XYZ(lab), d65).clip(0, 1)
        
        fig4, ax = plt.subplots(2,2, figsize=(10, 10), gridspec_kw=dict(width_ratios=[1, 2], height_ratios=[2, 1]))
        s = 30
        fs = 16
  
        Lb = ax[0,0]
        ab = ax[0,1]
        AB = ax[1,0]
        aL = ax[1,1]
        
        
        
        Lb.scatter(L_mean[0], b_mean[0], marker = 'x', s = 40, color=srgb[0])
        ab.scatter(a_mean[0], b_mean[0], marker = 'x', s = 40, color=srgb[0], label = 'start point')
        aL.scatter(a_mean[0], L_mean[0], marker = 'x', s = 40, color=srgb[0])        
        
        Lb.plot(L_mean, b_mean, color=srgb[1])
        ab.plot(a_mean, b_mean, color=srgb[1])
        AB.scatter(a_mean, b_mean,s = s, color=srgb)
        aL.plot(a_mean, L_mean, color=srgb[1])
        
        Lb.fill_between(L_mean, b_mean - b_std, b_mean + b_std, alpha=0.3)
        ab.fill_between(a_mean, b_mean - b_std, b_mean + b_std, alpha=0.3)
        aL.fill_between(a_mean, L_mean - L_std, L_mean + L_std, alpha=0.3)
        
        Lb.axhline(0, color="black", lw=0.5)
        ab.axhline(0, color="black", lw=0.5)
        AB.axhline(0, color="black", lw=0.5)
        aL.axhline(50, color="black", lw=0.5)

        Lb.axvline(50, color="black", lw=0.5)
        ab.axvline(0, color="black", lw=0.5)
        AB.axvline(0, color="black", lw=0.5)
        aL.axvline(0, color="black", lw=0.5)
        
        
        Lb.set_xlim(L_mean.min()-0.5, L_mean.max()+0.5)
        Lb.set_ylim(b_mean.min()-0.5, b_mean.max()+0.5)
        ab.set_xlim(a_mean.min()-0.5, a_mean.max()+0.5)
        ab.set_ylim(b_mean.min()-0.5, b_mean.max()+0.5) 
        AB.set_xlim(-100, 100)
        AB.set_ylim(-100, 100)  
        aL.set_xlim(a_mean.min()-0.5, a_mean.max()+0.5)
        aL.set_ylim(L_mean.min()-0.5, L_mean.max()+0.5)       
                     
        Lb.set_xlabel("CIE $L^*$", fontsize=fs)
        Lb.set_ylabel("CIE $b^*$", fontsize=fs)
        AB.set_xlabel("CIE $a^*$", fontsize=fs)
        AB.set_ylabel("CIE $b^*$", fontsize=fs)
        aL.set_xlabel("CIE $a^*$", fontsize=fs)
        aL.set_ylabel("CIE $L^*$", fontsize=fs) 
        
        
        Lb.xaxis.set_tick_params(labelsize=fs)
        Lb.yaxis.set_tick_params(labelsize=fs)
        ab.xaxis.set_tick_params(labelsize=fs)
        ab.yaxis.set_tick_params(labelsize=fs)   
        AB.xaxis.set_tick_params(labelsize=fs)
        AB.yaxis.set_tick_params(labelsize=fs)
        aL.xaxis.set_tick_params(labelsize=fs)
        aL.yaxis.set_tick_params(labelsize=fs)
                      
     
        red = matplotlib.patches.Rectangle((90,-7), 14, 14, color='red', alpha = 1)
        yellow = matplotlib.patches.Rectangle((-7,90), 14, 14, color='yellow', alpha = 1)
        green = matplotlib.patches.Rectangle((-100,-7), 14, 14, color='green', alpha = 1)
        blue = matplotlib.patches.Rectangle((-7,-100), 14, 14, color='blue', alpha = 1)
        black = matplotlib.patches.Rectangle((a_mean.min()-10,b_mean.min()-10), (a_mean.max()-a_mean.min())+20, (b_mean.max()-b_mean.min())+20,fill=None, ls = '--', color='black', alpha = 1)
        AB.add_patch(red)
        AB.add_patch(yellow)
        AB.add_patch(green)
        AB.add_patch(blue)
        AB.add_patch(black)
        
        ab.legend(loc = 'best')
        
        name = 'Micro-fading analysis - CIELAB space \n' + date +', '+Id+', '+r"$\bf{" + pigment + "}$"
        plt.suptitle(name,fontsize = fs+2)
        plt.tight_layout(rect = (0,0,1,0.99))
        plt.show()
        
        def button(_):
            with vbox4bis:
                fig4.savefig(dir_path+f'{date}_{Id}_{pigment}_CIELAB.png', dpi = 300)
                print('figure saved !')
        
        b4.on_click(button)
        
        display(wg.HBox([vbox4, vbox4bis]))
        
    with out5: 
        
        date = file_dE.split('_')[0]
        Id = file_dE.split('_')[1]
        pigment = file_dE.split('_')[2]
        
        df_dE = pd.read_csv(file_dE, header = [0,1])
        
        t = df_dE['time_s']
        t_fin = int(np.round((t.values[-1]/60),0))
        
        E_pho = df_dE['cum_klux_hr', 'value'].values.astype(int)
        E_rad = df_dE['cum_MJ/m2', 'value'].values
        E_rad_last = E_rad[-1]  # in MJ/m²
        E_pho_last = E_pho[-1] # in Mlx.hr
        
        L_mean = df_dE['L*', 'mean']                
        a_mean = df_dE['a*', 'mean']                
        b_mean = df_dE['b*', 'mean']        
        
        lab = np.array([L_mean, a_mean, b_mean]).transpose()
        srgb = colour.XYZ_to_sRGB(colour.Lab_to_XYZ(lab), d65).clip(0, 1)
        
        fig5, axes = plt.subplots(2,1,figsize = (15,7))        
        fig5.patch.set_facecolor((0.75, 0.75, 0.75))
        
        x = np.linspace(0,len(srgb),num = 5, endpoint = True,dtype = 'int')
        #t_int = np.linspace(0,t_fin,num = 5, endpoint = True,dtype = 'int')
        E_rad_values = np.linspace(0,E_rad_last, num = 5, endpoint = True, dtype = 'int')
        E_pho_values = np.round(np.linspace(0,E_pho_last, num = 5, endpoint = True, dtype = 'int'),2)
        
        cp_0 = matplotlib.patches.Rectangle((0,0), 0.2, 1, color=srgb[0])
        cp_1 = matplotlib.patches.Rectangle((0.2,0), 0.2, 1, color=srgb[x[1]])
        cp_2 = matplotlib.patches.Rectangle((0.4,0), 0.2, 1, color=srgb[x[2]])
        cp_3 = matplotlib.patches.Rectangle((0.6,0), 0.2, 1, color=srgb[x[3]])
        cp_4 = matplotlib.patches.Rectangle((0.8,0), 0.2, 1, color=srgb[-1])
        
        axes[0].add_patch(cp_0)
        axes[0].add_patch(cp_1)    
        axes[0].add_patch(cp_2) 
        axes[0].add_patch(cp_3) 
        axes[0].add_patch(cp_4) 
        axes[0].grid(False)
        axes[0].axis('off')
        
        if L_mean[0] > 50:
            axes[0].annotate('0 MJ/m²',(0.06, 0.05),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[1]} MJ/m²',(0.25, 0.05),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[2]} MJ/m²',(0.45, 0.05),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[3]} MJ/m²',(0.65, 0.05),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[4]} MJ/m²',(0.85, 0.05),weight='bold',fontsize = fs)            
            axes[0].annotate('0 klx.hr',(0.06, 0.9),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[1]} klx.hr',(0.25, 0.9),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[2]} klx.hr',(0.45, 0.9),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[3]} klx.hr',(0.65, 0.9),weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[4]} klx.hr',(0.85, 0.9),weight='bold',fontsize = fs)  
            
        else:
            axes[0].annotate('0 MJ/m²',(0.06, 0.05),color = 'white', weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[1]} MJ/m²',(0.25, 0.05),color = 'white', weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[2]} MJ/m²',(0.45, 0.05),color = 'white', weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[3]} MJ/m²',(0.65, 0.05),color = 'white', weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_rad_values[4]} MJ/m²',(0.85, 0.05),color = 'white', weight='bold',fontsize = fs)  
            axes[0].annotate('0 klx.hr',(0.06, 0.9),color = 'white',weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[1]} klx.hr',(0.25, 0.9),color = 'white',weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[2]} klx.hr',(0.45, 0.9),color = 'white',weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[3]} klx.hr',(0.65, 0.9),color = 'white',weight='bold',fontsize = fs)
            axes[0].annotate(f'{E_pho_values[4]} klx.hr',(0.85, 0.9),color = 'white',weight='bold',fontsize = fs) 

        cp_i = matplotlib.patches.Rectangle((0,0), 0.5, 1, color=srgb[0])
        cp_f = matplotlib.patches.Rectangle((0.5,0), 0.5, 1, color=srgb[-1])
        axes[1].add_patch(cp_i)
        axes[1].add_patch(cp_f)    
        axes[1].grid(False)
        axes[1].axis('off')

        if L_mean[0] > 50:
            axes[1].annotate('Initial - 0 min',(0.02, 0.05),weight='bold',fontsize = fs)
            axes[1].annotate(f'Final - {t_fin} min',(0.8, 0.05),weight='bold',fontsize = fs)
            
        else:
            axes[1].annotate('Initial - 0 min',(0.02, 0.05),color = 'white', weight='bold',fontsize = fs)
            axes[1].annotate(f'Final - {t_fin} min',(0.8, 0.05),color = 'white', weight='bold',fontsize = fs) 
            
        name = 'Micro-fading analysis - Colour patches \n' + date +', '+Id+', '+r"$\bf{" + pigment + "}$"
        plt.suptitle(name,fontsize = fs+2)
        #plt.tight_layout(rect = (0,0,1,0.95))
        plt.show()
        
        def button(_):
            with vbox5bis:
                fig5.savefig(dir_path+f'{date}_{Id}_{pigment}_CP.png', facecolor = (0.75, 0.75, 0.75), dpi = 300)
                print('figure saved !')
        
        b5.on_click(button)
        
        display(wg.HBox([vbox5, vbox5bis]))
        
    with out6:
        
        df_dE = pd.read_csv(file_dE, header = [0,1])
        
       
        E_pho = df_dE['cum_klux_hr', 'value'].values.astype(int)
        E_rad = df_dE['cum_MJ/m2', 'value'].values
        E_rad_last = E_rad[-1]  # in MJ/m²
        E_pho_last = E_pho[-1] # in Mlx.hr
        
        dE00_mean = df_dE['dE00', 'mean'] 
        L_mean = df_dE['L*', 'mean']                
        a_mean = df_dE['a*', 'mean']                
        b_mean = df_dE['b*', 'mean'] 
        
        
        style = {'description_width': 'initial'}
        L_i = L_mean[0]
        a_i = a_mean[0]
        b_i = b_mean[0]
        Lab_i = (L_i,a_i,b_i) 
        sRGB_i = colour.XYZ_to_sRGB(colour.Lab_to_XYZ(Lab_i), d65).clip(0, 1)
        
        
        max_dose = E_pho.max()

        def f(ill_slider,t_slider,hpd):

            range_dose = np.arange(0,E_pho[-1],1)
            range_dE = np.arange(0,dE00_mean.values[-1],0.01)

            f_dose = sip.interp1d(dE00_mean,E_pho)
            f_dE = sip.interp1d(E_pho,dE00_mean)
            f_L = sip.interp1d(E_pho,L_mean)
            f_a = sip.interp1d(E_pho,a_mean)
            f_b = sip.interp1d(E_pho,b_mean)

            f_L(range_dose)
            f_a(range_dose)
            f_b(range_dose)    
            f_dE(range_dose)
            f_dose(range_dE)


            days = int(t_slider/hpd)
            d = np.round((ill_slider/1000)*t_slider,2)
            

            if d <= max_dose:

                dE = np.round(f_dE(d),2)
                L_val = np.round(f_L(d),2)
                a_val = np.round(f_a(d),2)
                b_val = np.round(f_b(d),2)

                Lab_val = (L_val,a_val,b_val)    
                sRGB = colour.XYZ_to_sRGB(colour.Lab_to_XYZ(Lab_val), d65).clip(0, 1)

                fig7, ax8 = plt.subplots(figsize=(12, 7),facecolor = '#BFBFBF')


                cp_i = matplotlib.patches.Rectangle((0,0), 0.5, 1, color=(sRGB_i[0],sRGB_i[1],sRGB_i[2]))
                cp_f = matplotlib.patches.Rectangle((0.5,0), 0.5, 1, color=(sRGB[0],sRGB[1],sRGB[2]))
                ax8.add_patch(cp_i)
                ax8.add_patch(cp_f)
                ax8.set_xlim(-0.05, 1.05)
                ax8.set_ylim(-0.1, 1.1)
                ax8.axis('off')        

                ax8.annotate('Initial colour',(0.02, 0.05),fontsize = 20)
                ax8.annotate('Estimated colour',(0.7, 0.05),fontsize = 20)
                ax8.set_title(r'$\Delta E^*_{00}$' + f' = {dE}, Days of exposure = {days}, Exposure dose = {d} klx.hr', fontsize = 18, y = 0.99)

                plt.show()

            else:
                print('The given exposure exceeds the maximum dose for which data is available.')

            b6 = wg.Button(description='Save image')
            vbox6 = wg.VBox([b6])
            vbox6bis = wg.Output()

            def button(_):
                with vbox6bis:                    
                    fig7.savefig(f'{Id}_{pigment}_cp.png',facecolor = (0.75, 0.75, 0.75))
                    print('figure saved !')

            b6.on_click(button)

            display(wg.HBox([vbox6, vbox6bis]))

        ill_slider = wg.IntSlider(description='Illuminance (lux)', value = 100,min = 0, max = 500, step = 1,style = style,layout=Layout(width='47%', height='30px'))
        t_slider = wg.IntSlider(description='Duration (hrs)', min = 0, max = 10000, step = 1, style = style,layout=Layout(width='47%', height='30px'))
        hpd = wg.IntText(description = 'Hours per day', value = 10, max = 24, step = 1, style = style, layout=Layout(width='15%', height='30px'))

        interactive_plot = wg.interactive(f,ill_slider = ill_slider, t_slider = t_slider, hpd = hpd)
        output = interactive_plot.children[-1]
        output.layout.height = '550px'
        display(interactive_plot)
        
    with out7:
        
        df_dE = pd.read_csv(file_dE, header = [0,1])
        display(df_dE)
        
    with out8:
        date = file_dE.split('_')[0]
        photo_nb = '01'
        BS_plot_file = glob(f'*{date}*{photo_nb}*BS-PLOT*')[0]
        BS_irr_file = glob(f'*{date}*{photo_nb}*BS-IRR*')[0]
        
        
        fig, ax6 = plt.subplots(1,2,figsize = (45,30))
        
        im1 = imageio.imread(BS_irr_file)
        ax6[0].imshow(im1)
        ax6[0].grid(False)
        ax6[0].axis('off')
        
        im2 = imageio.imread(BS_plot_file)
        ax6[1].imshow(im2)
        ax6[1].grid(False)
        ax6[1].axis('off')
        
        plt.tight_layout()        
        plt.show()
        
    with out9:
        
        date = file_dE.split('_')[0]        
        file_info = glob(f'*{date}*{sample}*{lamp}*INFO*')[0]
        df_info = pd.read_csv(file_info,index_col ='parameter')
        display(df_info)
        
    display(tab)
    
    ###### SET PARAMATERS #######
 