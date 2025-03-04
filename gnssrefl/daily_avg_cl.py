# command line module that calls daily_avg.py
# Kristine Larson May 2019
import argparse
import matplotlib.pyplot as plt
import os

# my code
import gnssrefl.gps as g
# this was originally all one file - now moving the computations to a library
import gnssrefl.daily_avg as da

from gnssrefl.utils import str2bool

# changes to output requested by Kelly Enloe for JN
# two text files will now always made - but you can override the name of the average file via command line


def parse_arguments():
    # must input start and end year
    parser = argparse.ArgumentParser()
    parser.add_argument("station", help="station name", type=str)
    parser.add_argument("medfilter", help="Median filter for daily RH (m). Start with 0.25 ", type=float)
    parser.add_argument("ReqTracks", help="required number of tracks", type=int)
    parser.add_argument("-txtfile", default=None, type=str, help="Set your own output filename")
    parser.add_argument("-plt", default=None, type=str, help="plt to screen: True or False")
    parser.add_argument("-extension", default=None, type=str, help="extension for solution names")
    parser.add_argument("-year1", default=None, type=int, help="restrict to years starting with")
    parser.add_argument("-year2", default=None, type=int, help="restrict to years ending with")
    parser.add_argument("-fr", default=0, type=int, help="frequency, default is to use all")
    parser.add_argument("-csv", default=None, type=str, help="True if you want csv instead of plain text")
    args = parser.parse_args().__dict__

    # convert all expected boolean inputs from strings to booleans
    boolean_args = ['plt', 'csv']
    args = str2bool(args, boolean_args)

    # only return a dictionary of arguments that were added from the user - all other defaults will be set in code below
    return {key: value for key, value in args.items() if value is not None}


def daily_avg(station: str , medfilter: float, ReqTracks: int, txtfile: str = None, plt2screen: bool = True,
              extension: str = '', year1: int = 2005, year2: int = 2030, fr: int = 0, csv: bool = False):
    """
        Parameters:
        ___________
        station : string
            4 or 9 character ID of the station.

        medfilter : float
            Median filter for daily reflector height (m). Start with 0.25

        ReqTracks : integer
            Required number of tracks.

        txtfile : string, optional
            Use this parameter to set your own output filename.
            default is None.

        plt2 : boolean, optional
            whether to print plots to screen or not.
            default is True.

        extension : string, optional
            extension for solution names.
            default is ''. (empty string)

        year1 : integer, optional
            restrict to years starting with.
            default is 2005.

        year2 : integer, optional
            restrict to years ending with.
            default is 2021.

        fr : integer, optional
            GNSS frequency.
            value options:
                0 (default) : all
                1 : GPS L1
                2 : GPS L2
                20 : GPS L2C
                5 : GPS L5
                101 : GLONASS L1
                102 : GLONASS L2
                201 : GALILEO E1
                205 : GALILEO E5a
                206 : GALILEO E6
                207 : GALILEO E5b
                208 : GALILEO E5
                302 : BEIDOU B1
                306 : BEIDOU B3
                307 : BEIDOU B2
            default is 0. (all)

        csv : boolean, optional
            Whether you want csv instead of a plain text file.
            default is False (plain text).
    """
    # make surer environment variables are set
    g.check_environ_variables()
    xdir = os.environ['REFL_CODE']

# where the summary files will be written to
    txtdir = xdir + '/Files' 

    if not os.path.exists(txtdir):
        print('make an output directory', txtdir)
        os.makedirs(txtdir)

    # set the name of the output format
    if csv:
        alldatafile = txtdir + '/' + station + '_allRH.csv' 
    else:
        alldatafile = txtdir + '/' + station + '_allRH.txt' 

    tv, obstimes = da.readin_plot_daily(station, extension, year1, year2, fr, alldatafile, csv, medfilter, ReqTracks)

    # default is to show the plots
    if plt2screen:
        plt.show()

    # now write out the result file:

    if txtfile is None:
        if csv:
            outfile = txtdir + '/' + station + '_dailyRH.csv' 
        else:
        # use default  filename for the average
            outfile = txtdir + '/' + station + '_dailyRH.txt' 
    else:
        # use filename provided by the user
        outfile = txtdir + '/' + txtfile

    da.write_out_RH_file(obstimes, tv, outfile, csv)


def main():
    args = parse_arguments()
    daily_avg(**args)


if __name__ == "__main__":
    main()
