# -*- coding: utf-8 -*-
"""
author: kristine m. larson
quickLook command line function 
# 
"""
import argparse
import sys

# my codes
import gnssrefl.gps as g
import gnssrefl.quickLook_function as quick

from gnssrefl.utils import validate_input_datatypes, str2bool


def parse_arguments():
# user inputs the observation file information
    parser = argparse.ArgumentParser()
# required arguments
    parser.add_argument("station", help="station", type=str)
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("doy", help="day of year", type=int)
# these are the optional inputs
    parser.add_argument("-snr", default=None, type=int, help="snr ending - default is 66")
    parser.add_argument("-fr", default=None, type=int, help="try -fr 1 for GPS L1 only, or -fr 101 for Glonass L1")
    parser.add_argument("-ampl", default=None, type=float, help="minimum spectral amplitude allowed")
    parser.add_argument("-e1",  default=None, type=int, help="lower limit elevation angle (deg)")
    parser.add_argument("-e2",  default=None, type=int, help="upper limit elevation angle (deg)")
    parser.add_argument("-h1",  default=None, type=float, help="lower limit reflector height (m)")
    parser.add_argument("-h2",  default=None, type=float, help="upper limit reflector height (m)")
    parser.add_argument("-sat", default=None, type=int, help="satellite")
    parser.add_argument("-screenstats", default=None, type=str, help="if True, Success and Failure info printed to the screen")
    parser.add_argument("-peak2noise",  default=None, type=float, help="Quality Control ratio")
    parser.add_argument("-fortran", default=None, type=str, help="Default is True: use Fortran translators")

    args = parser.parse_args().__dict__

    # convert all expected boolean inputs from strings to booleans
    boolean_args = ['screenstats', 'fortran']
    args = str2bool(args, boolean_args)

    # only return a dictionary of arguments that were added from the user - all other defaults will be set in code below
    return {key: value for key, value in args.items() if value is not None}


def quicklook(station: str, year: int, doy: int,
              snr: int = 66, fr: int = 1, ampl: float = 7.,
              e1: int = 5, e2: int = 25, h1: float = 0.5, h2: float = 6., sat: int = None,
              peak2noise: float = 3., screenstats: bool = False, fortran: bool = None, pltscreen: bool = True):
    """

        Parameters:
        ___________
        station : string
            4 or 9 character ID of the station

        year : integer
            Year

        doy : integer
            Day of year

        snr : integer, optional
            SNR format. This tells the code what elevation angles to save data for. Will be the snr file ending.
            value options:
                66 (default) : saves all data with elevation angles less than 30 degress
                99 : saves all data with elevation angles between 5 and 30 degrees
                88 : saves all data with elevation angles between 5 and 90 degrees
                50 : saves all data with elevation angles less than 10 degrees
        f : integer, optional
            GNSS frequency.
            value options:
                1 (default) : GPS L1
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

            reqAmp : array_like, optional
                Lomb-Scargle Periodogram (LSP) amplitude significance criterion in volts/volts.
                Default is [7].

            e1 : integer, optional
                elevation angle lower limit in degrees for the LSP.
                default is 5.

            e2: integer, optional
                elevation angle upper limit in degrees for the LSP.
                default is 25.

            h1 : float, optional
                The allowed LSP reflector height lower limit in meters.
                default is 0.5.

            h2 : float, optional
                The allowed LSP reflector height upper limit in meters.
                default is 6.

            sat : array_like, optional
                list of satellites numbers
                default is None.
                array items: integer

            peak2noise : integer, optional
                 peak to noise ratio of the periodogram values (periodogram peak divided by the periodogram noise).
                 peak to noise value is one way of defining that significance (not the only way).
                 For snow and ice, 3.5 or greater, tides can be tricky if the water is rough (and thus
                 you might go below 3 a bit, say 2.5-2.7
                 default is 3.

            screenstats : boolean, optional
                 Whether to print stats to the screen.
                 default is False.

            pltscreen : boolean, optional
                Whether to print plots to the screen.
                default is True.

    """

#   make sure environment variables exist.  set to current directory if not
    g.check_environ_variables()

    # not including ampl and fr in the data type validation since they are sometimes a list and sometimes a float/int
    # validate_input_datatypes(quicklook, station=station, year=year, doy=doy, snr=snr, e1=e1, e2=e2,
    #                          h1=h1, h2=h2, sat=sat, peak2noise=peak2noise, fortran=fortran, screenstats=screenstats)

    exitS = g.check_inputs(station, year, doy, snr)

    if exitS:
        sys.exit()


    # set some reasonable default values for LSP (Reflector Height calculation).
    # most of these can be overriden at the command line
    if fr is not type(list):
        fr = [fr]  # default is to do L1

    pele = [5, 30]  # polynomial fit limits
    if ampl is not type(list):
        ampl = [ampl]  # this is arbitrary  - but often true for L1 obs

    if e1 < 5:
        print('have to change the polynomial limits because you went below 5 degrees')
        print('this restriction is for quickLook only ')
        pele[0] = e1

    args = {'station': station.lower(), 'year': year, 'doy': doy, 'snr_type': snr, 'f': fr[0], 'reqAmp': ampl, 'e1': e1,
            'e2': e2, 'minH': h1, 'maxH': h2, 'PkNoise': peak2noise, 'satsel': sat, 'fortran': fortran, 'pele': pele,
            'pltscreen': pltscreen, 'screenstats': screenstats}

    return quick.quickLook_function(**args)
    # returns two variables: data, datakey = quick.quicklook_function(**args)

    # the key is saved wth the same keys as the data dictionary, in this order 
    # [avgAzim, RH, satNumber,frequency,maxAmplitude,Peak2Noise, UTChour]


def main():
    args = parse_arguments()
    data, datakey = quicklook(**args)


if __name__ == "__main__":
    main()
