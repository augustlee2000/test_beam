#!/usr/bin/env python
# coding: utf-8
import numpy as np
from math import pi, sqrt, exp, cos, log
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import moyal
from scipy.integrate import quad

from matplotlib.widgets import Slider, Button, TextBox
%matplotlib widget

#function that give back an area that represent a square wave 
def squarewave(time_array, frequency, phase):
    squarewave_temp = signal.square(2*pi*frequency*time_array + phase)
    squarewave_array = squarewave_mover(squarewave_temp)
    return squarewave_array

#a simple form of the PDF of the landau distrubtuion 
def landau(time_array):
    return ((1/sqrt(2*pi)) * exp(-1 * (time_array  + exp(-1*time_array))/2) *4)

#The orginal square wave is from -1 to 1 I wanted it from 0 to 1
def squarewave_mover(squarewave):
    for i in range(len(squarewave)):
        if squarewave[i] < 0:
            squarewave[i] = 0
        else:
            continue
    return squarewave

#the PDF of the landau distribution used in the integration
def integrand(t):
    return (np.exp(-t) * np.cos(t*((x-u)/c) + (2*t*np.log(t/c))/(pi)))

#This create the array for the landau distrubution 
def landau_array_creator(time_array):
    global x
    test = np.array([])
    for i in range(len(time_array)):
        x = time_array[i]
        temp = quad(integrand,0,np.inf)
        if temp[0] < 0:
            test = np.append(test, 0)
        else:
            test  = np.append(test, temp[0])
    return test

    

#a quick and easy rectangluar integration calculator for the landau distrubution where it only does the integral if the square wave is 1
def integral_calculator(time_array, landau_array, timer_array, spacing):
    integral = 0.0
    for i in range(len(time_array)):
        if timer_array[i] > 0:
            integral += landau_array[i] * spacing
        else:
            continue
    return integral

#does the full integral
def integral_calculator_super_lazy(time_array, landau_array, spaceing):
    integral = 0.0
    for i in range(len(time_array)):
        integral += landau_array[i] * spacing
    return integral

# makes an array that shows the threshold         
def threshold_calc(time_array, threshold):
    temp = np.array([])
    for i in range(len(time_array)):
        temp = np.append(temp, threshold)
    return temp

# The function to be called anytime a slider's value changes
def update(val):
    phase= phase_slider.val
    x_shift = pos_slider.val
    threshold = thresh_slider.val
    y1 = squarewave(time_array,frequency_timer,phase)
    y2 =squarewave(time_array,frequency_tdc,phase)
    
    time_array_new = time_array - x_shift
    
    x1 = landau_array_creator(time_array_new)/integral_full
    x2 = threshold_calc(time_array,threshold)
    axs[1].lines[0].set_ydata(y1)
    axs[2].lines[0].set_ydata(y2)
    axs[0].lines[0].set_ydata(x1)
    axs[0].lines[1].set_ydata(x2)
    t1.set_text("The Total Percentage of Electrons seen by the Trigger: " + str(round(integral_calculator(time_array,x1, y1, spacing),4)))
    text_string = latency_finder(time_array, x1,tdc_array, threshold, phase)
    t2.set_text(text_string)
    fig.canvas.draw_idle()

# Resets the sliders
def reset(event):
    phase_slider.reset()
    pos_slider.reset()
    thresh_slider.reset()

def latency_finder(time_array_new, landau_array, tdc_array, threshold, phase):
    text_string = ""
    text_string += "\n"
    phase_integer = phase //3.125
    for i in range(len(tdc_array)):
        latency = 0
        landau_val = 0.0
        while latency < 6:
            timer_position = tdc_array[i] * 3.125 + latency *25 + phase_integer *3.125 
            index = np.where(time_array_new == timer_position)
            landau_val = landau_array[index[0]]
            if landau_val <= threshold:
                latency +=1
                continue
            else:
                break
                
        text_string +="TDC: "
        text_string += str(tdc_array[i])
        text_string +=" Has a latency of "
        text_string += str(5-latency)
        text_string += "\n"
    return text_string
    

#making the time array     
N = 481
time_end = 150
time_array = np.linspace(0, time_end, N)

spacing = time_end/N

#all of our inital conditions
frequency_timer = .040
frequency_tdc = frequency_timer * 8
phase_timer = 0
phase_tdc = 0
landau_x_shift = 10
threshold_int = .01

#controls the landau distribution
c = 10
u = 5
x = 0.0

#makes the timer and tdc squarewaves
squarewave_timer = squarewave(time_array,frequency_timer, phase_timer)
squarewave_tdc = squarewave(time_array,frequency_tdc,phase_timer)


#makes the landau distrubutino
landau_array = landau_array_creator(time_array - landau_x_shift)

#find the integral of the landau distrubution and normalized
integral_full = integral_calculator_super_lazy(time_array, landau_array, spacing)
                   
landau_array  = landau_array/integral_full


#makes the threshhold
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

fig.subplots_adjust(left=.20, bottom=0.37)

#This part is going to be about find the latency

tdc_array = np.linspace(0,7,8)
    
text_string =latency_finder(time_array, landau_array, tdc_array, threshold_int, phase_timer)


#makes the three slider that we want in the program
axfreq = fig.add_axes([0.25, 0.04, 0.65, 0.02])
phase_slider = Slider(
    ax=axfreq,
    label='Phase Shift',
    valmin=-5,
    valmax=5,
    valinit=phase_timer,
)

axpos = fig.add_axes([0.25, 0.01, 0.65, 0.02])
pos_slider = Slider(
    ax=axpos,
    label='Position of Distrubution',
    valmin=0.1,
    valmax=time_end,
    valinit=landau_x_shift,
)


axthresh = fig.add_axes([0.25, 0.07, 0.65, 0.02])
thresh_slider = Slider(
    ax=axthresh,
    label='Threshold',
    valmin=0.001,
    valmax=.025,
    valinit=threshold_int,
)


t1 = fig.text(.05, .90,  "The Total Percentage of Electrons seen by the Trigger: " +str(round(integral_calculator(time_array,landau_array, squarewave_timer, spacing),4)))

t2 = fig.text(.40,.085, text_string)

#updates the sliders
phase_slider.on_changed(update)
pos_slider.on_changed(update)
thresh_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.13, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

button.on_clicked(reset)

plt.show()
print("If Latency is -1 then that TDC Value never found a value above threshold")
