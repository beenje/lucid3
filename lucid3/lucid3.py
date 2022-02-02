#! /usr/bin/env python
# /*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ############################################################################*/
"""
Lucid 3 project - command line script for running lucid3
"""

import sys
import math
import imageio
import argparse

import lucid_core

import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt  # noqa E402


def getCommandlineOptions():
    parser = argparse.ArgumentParser(
        description="Application for finding loop in diffractometer snapshot of sample"
    )
    parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "snapshot_file_path",
        action="store",
        help="Path to snapshot jpg/png file",
    )
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--vertical",
        action="store_true",
        help="Vertical rotation axis",
        default=False,
    )
    optional.add_argument(
        "--display",
        action="store_true",
        help="Display snapshot with result",
        default=False,
    )
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--debug",
        action="store_true",
        help="Display snapshot with all intermediate steps and with result",
        default=False,
    )

    results = parser.parse_args()

    # Check that we have at leats one input
    if results.snapshot_file_path is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return results


if __name__ == "__main__":
    cmd_options = getCommandlineOptions()
    result = lucid_core.find_loop(
        cmd_options.snapshot_file_path,
        rotation=cmd_options.vertical,
        debug=cmd_options.debug,
    )
    print(result)
    if cmd_options.display and result[0] == "Coord":
        image = imageio.imread(cmd_options.snapshot_file_path, as_gray=True)
        imgshape = image.shape
        maxDiff = math.sqrt(imgshape[0] ** 2 + imgshape[1] ** 2) / 15.0
        extent = (0, imgshape[1], 0, imgshape[0])
        xPos = result[1]
        yPos = imgshape[0] - result[2]
        implot = plt.imshow(image, extent=extent)
        plt.title(cmd_options.snapshot_file_path)
        plt.plot(xPos, yPos, marker="+", markeredgewidth=2, markersize=25, color="red")
        plt.show()