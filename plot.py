#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
    Plot some data with Bokeh

    Based on a Bokeh application server example
    https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py
"""

from math import cos, sin, tan, sqrt, atan2, exp, log, pi
from random import random
from time import sleep
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Button
from bokeh.plotting import figure


# CLASS BasePlot
class BasePlot:
    """ Base class for plotting
    """

    def __init__(self):
        self.Ns = 200   # Number of sampling points


    def set_axes(self, x_range=None, y_range=None):
        """ Update the axes of the plot

            Parameters:
            - (optional) x_range: list of the lower and uper bound for the x axis
            - (optional) y_range: list of the lower and uper bound for the y axis
        """

        if not hasattr(self, 'plot'):
            return

        if x_range is not None:
            self.plot.x_range.start = x_range[0]
            self.plot.x_range.end   = x_range[1]

        if y_range is not None:
            self.plot.y_range.start = y_range[0]
            self.plot.y_range.end   = y_range[1]


    def plot_curve(self):
        self.plot.line('x', 'y', source=self.source, line_width=3, line_alpha=0.6)


    def update_title(self, attrname, old, new):
        if hasattr(self, 'plot'):
            self.plot.title.text = new



# CLASS FunctionPlot
class FunctionPlot(BasePlot):
    """ Class for plotting in real time a given function
    """

    def __init__(self):
        BasePlot.__init__(self)

        self.t = 0.0    # Starting point of the x axis
        self.period_tick = 0.100  # Delay between two ticks

        # Set up widgets
        self.function_input = TextInput(title="Function of x (Python expression)", value='3*pi*exp(-5*sin(2*pi*x))')
        self.x_range  = Slider(title="Range x", value=1.0, start=0.1, end=20.0, step=0.1)
        self.speed    = Slider(title="Speed", value=0.0, start=0.0, end=2.0, step=0.01)
        self.reset_time_button  = Button(label="Reset time")

        # Set up callbacks
        self.function_input.on_change('value', self.update_function)
        self.x_range.on_change('value', self.update_axes)
        self.reset_time_button.on_click(self.reset_time)

        # Set up layouts and add to document
        inputs = widgetbox(self.function_input,
                           self.x_range,
                           self.speed,
                           self.reset_time_button)

        # Set up data
        self.update_function(None, None, None)  # (will also call update_data())

        # Set up plot
        self.plot = figure(plot_height=400, plot_width=400, title="3*pi*exp(-5*sin(2*pi*x))",
                      tools="pan,reset,save,wheel_zoom",
                      x_range=[0.0, 1.0], y_range=[0.0, 1.0])
        # self.set_axes()
        self.plot_curve()

        curdoc().add_root(row(inputs, self.plot, width=800))
        curdoc().title = "Function plot"
        curdoc().add_periodic_callback(self.tick_callback, 1/self.period_tick)


    def tick_callback(self):
        """ Callback called periodically to update the graph dataset
        """

        self.t += self.speed.value * self.period_tick
        self.update_axes(None, None, None)


    def reset_time(self):
        self.t = 0.0


    def update_data(self, attrname, old, new):
        """ Update the data of the plot
        """

        x = np.linspace(self.t, self.t+self.x_range.value, self.Ns)
        y = [self.function(t) for t in x]

        if not hasattr(self, 'source'):
            self.source = ColumnDataSource(data=dict(x=x, y=y))
        else:
            self.source.data = dict(x=x, y=y)


    def update_function(self, attrname, old, new):
        """ Update the function to plot
        """

        def f(x):
            try :
                return eval(self.function_input.value)
            except:
                return 0.0

        self.function = f
        self.update_title(None, None, self.function_input.value)
        self.update_axes(None, None, None)


    def update_axes(self, attrname, old, new):
        """ Update the range of the x axis
        """

        self.update_data(None, None, None)

        y_min = 10**9
        y_max = -10**9

        for k in range(self.Ns):
            y = self.source.data['y'][k]
            if y > y_max:
                y_max = y
            if y < y_min:
                y_min = y

        self.set_axes(x_range=[self.t, self.t+self.x_range.value],
                      y_range=[y_min, y_max])




# Run everything
plot_object = FunctionPlot()
