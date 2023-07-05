#!/usr/bin/env python3
import argparse
import gzip
import json
import logging
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

import evaluate.settings as settings
import metrics.utils as utils

# NOTE this script assumes that metrics are normalized to [0,1] with 0 bad and 1 good
# A collection of default metrics used for this plot
METRICS = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1",
    "F0.1",
    "Detected-Scenarios-Percent",
    "eTaF0.1",
    "eTaF1",
    "eTaR",
    "eTaP",
]
ALL = [m for metric in utils.get_all_metrics().values() for m in metric.defines()]

# Indicate whether a metric needs to be inverted such tat 0 is bad and 1 is good
INVERT = [m._name for m in utils.get_all_metrics().values() if not m._higher_is_better]

# Collection of colors for the IDSs
COLORS = [
    "#006ba5",
    "#f26c64",
    "#ffcc99",
    "#88d279",
    "#984ea3",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]


# Wrapper for hiding .gz files
def open_file(filename, mode):
    if filename.endswith(".gz"):
        return gzip.open(filename, mode=mode, compresslevel=settings.compresslevel)
    else:
        return open(filename, mode=mode, buffering=1)


# Initialize logger
def initialize_logger(args):
    if args.log:
        settings.log = getattr(logging, args.log.upper(), None)

        if not isinstance(settings.log, int):
            logging.getLogger("ipal-plot-metrics").error(
                "Option '--log' parameter not found"
            )
            exit(1)

    if args.logfile:
        settings.logfile = args.logfile
        logging.basicConfig(
            filename=settings.logfile, level=settings.log, format=settings.logformat
        )
    else:
        logging.basicConfig(level=settings.log, format=settings.logformat)

    settings.logger = logging.getLogger("ipal-plot-metrics")


# https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html
def radar_factory(num_vars, frame="circle"):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):
        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):
        name = "radar"
        rotate = 0
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location("N", offset=self.rotate)

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == "circle":
                return Circle((0.5, 0.5), 0.5)
            elif frame == "polygon":
                return RegularPolygon((0.5, 0.5), num_vars, radius=0.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == "circle":
                return super()._gen_axes_spines()
            elif frame == "polygon":
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(
                    axes=self,
                    spine_type="circle",
                    path=Path.unit_regular_polygon(num_vars),
                )
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(
                    Affine2D().rotate_deg(self.rotate).scale(0.5).translate(0.5, 0.5)
                    + self.transAxes
                )
                return {"polar": spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def load_data(files):
    data = []

    for file in files:
        settings.logger.info("Processing {}".format(file))

        with open_file(file, "r") as f:
            js = json.loads(f.read())

        metricdata = []
        for metric in METRICS:
            if metric not in js:
                settings.logger.error(
                    "Metric '{}' is missing in {}".format(metric, file)
                )
                metricdata.append(0)

            elif js[metric] is None:
                settings.logger.error("Metric '{}' is None in {}".format(metric, file))
                metricdata.append(0)

            elif not (0 <= js[metric] and js[metric] <= 1):
                settings.logger.error(
                    "Metric '{}' malformed or not between [0,1] for {}".format(
                        metric, file
                    )
                )
                metricdata.append(0)

            else:
                metricdata.append(1 - js[metric] if metric in INVERT else js[metric])

        # find out IIDS name from config
        if "_iids-config" in js and "idss" in js["_iids-config"]:
            idsname = ",".join(js["_iids-config"]["idss"].keys())

        else:  # fall back to file name
            idsname = (
                pathlib.Path(file)
                .stem.replace(".json", "")
                .replace(".ipal", "")
                .replace(".state", "")
            )
        data.append((idsname, metricdata))

    return data


def plot(ax, data, theta):
    global METRICS

    ax.set_rgrids([0.2, 0.4, 0.6, 0.8])

    # Plot each IDSs data
    for i, d in enumerate(data):
        _, metrics = d

        ax.plot(theta, metrics, color=COLORS[i % len(COLORS)])
        ax.fill(
            theta,
            metrics,
            facecolor=COLORS[i % len(COLORS)],
            alpha=0.25,
            label="_nolegend_",
        )

    ax.set_ylim([0, 1])

    spoke_labels = [
        metric if metric not in INVERT else "1-{}".format(metric) for metric in METRICS
    ]
    ax.set_varlabels(spoke_labels)

    # Put a legend BELOW current axis
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend(
        [name for name, _ in data],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
    )


def main():
    global METRICS

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--metrics",
        metavar="metrics",
        help="comma-separated list of metrics to be plotted (Default: '{}') Possible metrics are: {}".format(
            ",".join(METRICS),
            ",".join(ALL),
        ),
        required=False,
    )

    parser.add_argument(
        "--title",
        metavar="title",
        help="title to put on the plot (Default: '')",
        required=False,
    )

    parser.add_argument(
        "--output",
        metavar="output",
        help="file to save the plot to (Default: '': show in matplotlib window)",
        required=False,
    )

    parser.add_argument(
        "results",
        metavar="results",
        nargs="+",
        help="list of files containing evaluation data of ipal-evaluate",
    )

    # Logging
    parser.add_argument(
        "--log",
        dest="log",
        metavar="STR",
        help="define logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) (Default: WARNING)",
        required=False,
    )
    parser.add_argument(
        "--logfile",
        dest="logfile",
        metavar="FILE",
        default=False,
        help="file to log to (Default: stderr)",
        required=False,
    )

    # Version number
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {settings.version}"
    )

    args = parser.parse_args()
    initialize_logger(args)

    if args.metrics:
        METRICS = args.metrics.split(",")

    # Plot
    theta = radar_factory(len(METRICS), frame="polygon")
    _, ax = plt.subplots(1, subplot_kw=dict(projection="radar"))

    data = load_data(args.results)
    plot(ax, data, theta)

    if args.title:
        plt.title(args.title)

    settings.logger.info("Plotting...")
    if args.output is not None:
        plt.savefig(args.output)
    else:
        plt.show()


if __name__ == "__main__":
    main()
