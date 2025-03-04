# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import itertools

import numpy as np
from bokeh.io import output_file
from bokeh.models import tools
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure, show


def save_plot_to_file(traces, set_indices, num_traces, outfile, add_mean_stddev=False):
    """Save plot figure to file."""
    if set_indices is None:
        colors = itertools.cycle(palette)
    else:
        assert len(traces) == len(set_indices)
        # set_indices[x] indicates to which set trace x belongs.
        trace_colors = []
        for i in range(len(set_indices)):
            color_idx = set_indices[i] % len(palette)
            trace_colors.append(palette[color_idx])
        # Generate iterable from list.
        colors = itertools.cycle(tuple(trace_colors))
    xrange = range(len(traces[0]))
    plot = figure(plot_width=800)
    plot.add_tools(tools.CrosshairTool())
    plot.add_tools(tools.HoverTool())
    for i in range(min(len(traces), num_traces)):
        if set_indices is None:
            if add_mean_stddev:
                plot.line(xrange, traces[i], line_color='grey')
            else:
                plot.line(xrange, traces[i], line_color=next(colors))
        else:
            plot.line(xrange, traces[i], line_color=next(colors), legend_label=str(set_indices[i]))

    if add_mean_stddev:
        # Add mean and std dev to figure
        # Convert selected traces to np array before processing
        traces_new = np.empty((num_traces, len(traces[0])), dtype=np.uint16)
        for i_trace in range(num_traces):
            traces_new[i_trace] = traces[i_trace]
        mean = traces_new.mean(axis=0)
        std = traces_new.std(axis=0)
        mean_stddev_upper = mean + std
        mean_stddev_lower = mean - std
        plot.line(xrange, mean_stddev_upper, line_color='firebrick',
                  line_width=2, legend_label='std')
        plot.line(xrange, mean_stddev_lower, line_color='firebrick',
                  line_width=2, legend_label='std')
        plot.line(xrange, mean, line_color='black', line_width=2, legend_label='mean')

    output_file(outfile)
    show(plot)
