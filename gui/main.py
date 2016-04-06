#!/usr/bin/python
# coding=utf-8

import sys
import datetime
import tkinter as tk

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class GUI(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.desc = tk.Label(self, text='This program is used to show plot.')
        self.desc.grid(row=0, column=0, columnspan=4
                , sticky=tk.N+tk.S+tk.E+tk.W)
        self.ent = tk.Entry(self)
        # self.ent.pack({"side": "left", "fill":"x", "expand":"1"})
        self.ent.grid(row=1, column=0, sticky=tk.E)

        self.gen = tk.Button(self)
        self.gen["text"] = "Generate",
        self.gen["command"] = self.pre_generation
        # self.gen.pack({"side": "left"})
        self.gen.grid(row=1, column=1, sticky='W')

        # self.QUIT = tk.Button(self)
        # self.QUIT["text"] = "QUIT"
        # self.QUIT["fg"]   = "red"
        # self.QUIT["command"] =  self.quit
        # self.QUIT.pack({"side": "left"})
        # self.QUIT.grid(row=1, column=2, sticky='W')

        # self.image_scene = self.make_label(self, 0, 0, 1100, 300)
        self.image_scene = tk.Label(self)# , width=100, height=30)
        # self.image_scene.pack(side="right")
        self.image_scene.grid(row=2, column=0, columnspan=4)

    def make_label(master, x, y, h, w, *args, **kwargs):
        f = tk.Frame(master, height=h, width=w)
        f.pack_propagate(0)
        f.place(x=x, y=y)
        label = tk.Label(f, *args, **kwargs)
        label.pack(fill=BOTH, expand=1)

        return label

    def pre_generation(self):
        '''
        Called to generate new image and update it in gui representation.
        '''
        image_name = self.generate_img('2016-01-07', True, True)
        self.update_image(image_name)

    def update_image(self, image_name):
        '''
        Just update label with new image.
        '''
        self.graf = tk.PhotoImage(file=image_name, 
                width=1100, height=300)
        self.image_scene.configure(image=self.graf)

    def generate_img(self, filename, raw_data_on, cal_data_on):
        '''
        This function is generate image from two data files (filename.txt and
        filename_result.txt). filename.txt contains raw data, 
        filename_result.txt contains calibrated data. Data in files should be in
        this format: [123456, 123456, 123456, 123456]. 4-th element is doesn't
        used.
        Args:
            filename: file name which contains data.
            raw_data_on: turn on/off raw data on plot
            cal_data_on: turn on/off calibrated data on plot
        Returns:
            Return filaname of generated image.
        '''
        calb_data = filename + '_result.txt'
        raw_data  = filename + '.txt'
        image_name = 'plot.png'

        #=======================================================================
        # Create plot
        fig, axes = plt.subplots(1, 3, figsize=(11, 3))
        # axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        fontsize = 8
        fig.suptitle('Raw and calibratedx10e3 data.', fontsize=fontsize)
        
        # Set up fonts for all text objects
        font = {'family' : 'Arial',
                'size'   : 6}
        
        matplotlib.rc('font', **font)

        #=======================================================================
        # Data processing
        for data_num in range(3):
            # Calibrated data
            if cal_data_on:
                lines = open(calb_data, 'r').readlines()
        
                x_calb = np.linspace(0, len(lines), len(lines))
                y_calb = list()
        
                for line in lines:
                    line = line[1:-2]
                    y_calb.append(float(line.split(', ')[data_num])/10e7)
                # Add plot
                axes[data_num].plot(x_calb, y_calb, 'r')
        
            # Raw data
            if raw_data_on:
                lines = open(raw_data, 'r').readlines()
        
                x_raw = np.linspace(0, len(lines), len(lines))
                y_raw = list()
        
                for line in lines:
                    line = line[1:-2]
                    y_raw.append(float(line.split(', ')[data_num + 1])/10e7)
                # Add plot
                axes[data_num].plot(x_raw, y_raw, 'g')
                    
            # Plot settings
            axes[data_num].grid(True)
            axes[data_num].set_xlabel('Iteration', fontsize=fontsize)
            axes[data_num].set_ylabel('Value [T]', fontsize=fontsize)
        
            for tick in axes[data_num].xaxis.get_major_ticks():
                tick.label.set_fontsize(fontsize) 
            for tick in axes[data_num].yaxis.get_major_ticks():
                tick.label.set_fontsize(fontsize) 
            # axes[data_num].set_title('title');

        #=======================================================================
        
            axes[data_num].legend(['Calibrated data', 'Raw data'], loc=7, 
                    prop={'size':fontsize})
        
        #=======================================================================
        # Save plot
        #=======================================================================
        plt.savefig(image_name)

        return image_name
                
    def quit(self):
        sys.exit()
    




if __name__ == '__main__':
    #create a new window
    root = tk.Tk()
    root.geometry('1100x400')
    GUI(root).pack()
    #draw the window, and start the 'application'
    root.mainloop()

    sys.exit(0)

