#!/usr/bin/env python
# coding: utf-8

# In[83]:


import numpy as np
from math import pi, sqrt, exp
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import moyal

from matplotlib.widgets import Slider, Button, TextBox
get_ipython().run_line_magic('matplotlib', 'widget')


def squarewave(time_array, frequency, phase):
    squarewave_temp = signal.square(2*pi*frequency*time_array + phase)
    squarewave_array = squarewave_mover(squarewave_temp)
    return squarewave_array

def landau(time_array):
    return ((1/sqrt(2*pi)) * exp(-1 * (time_array  + exp(-1*time_array))/2) *4)

def squarewave_mover(squarewave):
    for i in range(len(squarewave)):
        if squarewave[i] < 0:
            squarewave[i] = 0
        else:
            continue
    return squarewave
def landau_array_creator(time_array, landau_x_shift):
    landau_array = np.array([])
    for i in range(len(time_array)):
        landau_array = np.append(landau_array, landau(time_array[i] -landau_x_shift))
    return landau_array

def integral_calculator(time_array, landau_array, timer_array, spacing):
    integral = 0.0
    for i in range(len(time_array)):
        if timer_array[i] > 0:
            integral += landau_array[i] * spacing
        else:
            continue
    return integral

def threshold_calc(time_array, threshold):
    temp = np.array([])
    for i in range(len(time_array)):
        temp = np.append(temp, threshold)
    return temp
        

    
N = 500
time_end = 150
time_array = np.linspace(0, time_end, N)

spacing = time_end/N

frequency_timer = .025
frequency_tdc = frequency_timer * 8
phase_timer = 0
phase_tdc = 0
landau_x_shift = 5
threshold_int = .5

squarewave_timer = squarewave(time_array,frequency_timer, phase_timer)
squarewave_tdc = squarewave(time_array,frequency_tdc,phase_timer)


landau_array = landau_array_creator(time_array, landau_x_shift)

threshold_array = threshold_calc(time_array, threshold_int)

# Create the figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(7, 7))
plt.suptitle("Trigger and Distrubution")

axs[0].plot(time_array, landau_array, label = "Landau Distribution")
axs[0].plot(time_array, threshold_array,label = "Threshold")
axs[1].plot(time_array, squarewave_timer, 'tab:red', label = "Timer")
axs[2].plot(time_array, squarewave_tdc, 'tab:green', label = "TDC")
plt.xlabel("Time (ns)")
fig.legend()

fig.subplots_adjust(left=.20, bottom=0.22)


axfreq = fig.add_axes([0.25, 0.05, 0.65, 0.03])
phase_slider = Slider(
    ax=axfreq,
    label='Phase Shift',
    valmin=-5,
    valmax=5,
    valinit=phase_timer,
)

axpos = fig.add_axes([0.25, 0.01, 0.65, 0.03])
pos_slider = Slider(
    ax=axpos,
    label='Position of Distrubution',
    valmin=0.1,
    valmax=time_end,
    valinit=landau_x_shift,
)


axthresh = fig.add_axes([0.25, 0.09, 0.65, 0.03])
thresh_slider = Slider(
    ax=axthresh,
    label='Threshold',
    valmin=0.1,
    valmax=1,
    valinit=threshold_int,
)


t1 = fig.text(.05, .90,  "The total Integral is: " +str(round(integral_calculator(time_array,landau_array, squarewave_timer, spacing),4)))


# The function to be called anytime a slider's value changes
def update(val):
    phase= phase_slider.val
    x_shift = pos_slider.val
    threshold = thresh_slider.val
    
    
    
    y1 = squarewave(time_array,frequency_timer,phase)
    y2 =squarewave(time_array,frequency_tdc,phase)
    x1 = landau_array_creator(time_array,x_shift)
    x2 = threshold_calc(time_array,threshold)
    axs[1].lines[0].set_ydata(y1)
    axs[2].lines[0].set_ydata(y2)
    axs[0].lines[0].set_ydata(x1)
    axs[0].lines[1].set_ydata(x2)
    t1.set_text("The total Integral is: " + str(round(integral_calculator(time_array,x1, y1, spacing),4)))
    fig.canvas.draw_idle()
    
    
phase_slider.on_changed(update)
pos_slider.on_changed(update)
thresh_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.13, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    phase_slider.reset()
    pos_slider.reset()
    thresh_slider.reset()
button.on_clicked(reset)




#This text box is working but it is very scuffed at the moment 



print(integral_calculator(time_array,landau_array, squarewave_timer, spacing))

plt.show()


# In[ ]:




