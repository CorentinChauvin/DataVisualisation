#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""


    Based on a Bokeh application server example
    https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py
"""


from random import random
from time import sleep
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

class BasePlot:
    """ Base class for plotting
    """

    def __init__(self):
        # Set up data
        self.source = None
        self.update_data(None, None, None)
        self.set_axes()

        # Set up plot
        self.plot = figure(plot_height=400, plot_width=400, title="my sine wave",
                      tools="crosshair,pan,reset,save,wheel_zoom",
                      x_range=self.x_range, y_range=self.y_range)
        self.update_view()

        # Set up widgets
        self.text = TextInput(title="title", value='my sine wave')
        self.offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
        self.amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
        self.phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
        self.freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)

        # Set up callbacks
        self.text.on_change('value', self.update_title)
        for w in [self.offset, self.amplitude, self.phase, self.freq]:
            w.on_change('value', self.update_data)

        # Set up layouts and add to document
        inputs = widgetbox(self.text, self.offset, self.amplitude, self.phase, self.freq)

        curdoc().add_root(row(inputs, self.plot, width=800))
        curdoc().title = "Sliders"
        curdoc().add_periodic_callback(self.tick_callback, 100)


    def update_data(self, attrname, old, new):
        """ Update the data of the plot
        """

        if self.source is None:
            N = 200
            x = np.linspace(0, 4*np.pi, N)
            y = np.sin(x)
            self.source = ColumnDataSource(data=dict(x=x, y=y))
        else:
            # Get the current slider values
            a = self.amplitude.value
            b = self.offset.value
            w = self.phase.value
            k = self.freq.value

            # Generate the new curve
            N = 200
            x = np.linspace(0, 4*np.pi, N)
            y = a*np.sin(k*x + w)**2 + b

            self.source.data = dict(x=x, y=y)


    def set_axes(self, x_range=None, y_range=None):
        """ Update the axes of the plot

            Parameters:
            - (optional) x_range: list of the lower and uper bound for the x axis
            - (optional) y_range: list of the lower and uper bound for the y axis

            If the two previous parameters are not given, the range is
            determined on the data.
        """

        self.x_range = [0, 4*np.pi]  # Axis ranges
        self.y_range = [-2.5, 2.5]


    def update_view(self):
        self.plot.line('x', 'y', source=self.source, line_width=3, line_alpha=0.6)


    def update_title(self, attrname, old, new):
        self.plot.title.text = str(random())
        # plot.title.text = text.value


    def tick_callback(self):
        self.update_title(None, None, None)



# Run everything
plot_object = BasePlot()
