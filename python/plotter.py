"""
Usage:
    plotter.py <files>... [options]

Arguments:
    files
    timeunit

Options:
    -t --time=<val>     Possible units are day, week, month, year [default: month]
    -h --hide           Hide the diagram / Don't show the diagram
    -o --out=<file>     Path to output file. You can specify the file format by using the desired file extension (e.g. png, pdf)
    --shiftleft         All projects start at x=0
    --norm              Normalises all y values to be between 0 and 1
    --acc               Accumulate y values
"""
from docopt import docopt
#plot(args['files'], args['-t'], args['-s'], args['-o'])
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
from datetime import datetime, timedelta
import numpy as np
import csv
from schema import Regex, SchemaError


def convert_date_to_day(date):
    return date


def convert_date_to_week(date):
    return date - timedelta(days=date.weekday())


def convert_date_to_month(date):
    return date.replace(day=1)


def convert_date_to_year(date):
    return date.replace(month=1, day=1)


def read_csv(path, convert_date_fun):
    date_count = {}
    with open(path) as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            date = convert_date_fun(datetime.strptime(row[0], '%Y-%m-%d'))
            date_count[date] = date_count.get(date, 0) + int(row[1])
    x = date_count.keys()
    y = date_count.values()
    # sort by date
    order = np.argsort(x)
    sorted_x = np.array(x)[order]
    sorted_y = np.array(y)[order]
    return sorted_x, sorted_y


def plot_from_csv(handle,
                  path,
                  time_unit,
                  shift_left,
                  accumulate,
                  normalise,
                  fmt='-',
                  label=None):
    convert_date_fun_options = {
        'day': convert_date_to_day,
        'week': convert_date_to_week,
        'month': convert_date_to_month,
        'year': convert_date_to_year,
    }
    x, y = read_csv(path, convert_date_fun_options[time_unit])

    if accumulate:
        y = np.add.accumulate(y)
    if normalise:
        y_max = np.amax(y)
        y = np.true_divide(y, y_max)

    if shift_left:
        x = [(val - x[0]).days for val in x]
        handle.plot(x, y, fmt, label=label)
    else:
        handle.plot_date(x, y, fmt, label=label)


def plot(files, time_unit, shift_left, accumulate, normalise, hide,
         output_file):
    years = YearLocator()
    months = MonthLocator()
    days = DayLocator()
    yearsFmt = mpl_dates.DateFormatter('%Y')

    fig, ax = plt.subplots()

    for file in files:
        plot_from_csv(
            handle=ax,
            path=file,
            time_unit=time_unit,
            shift_left=shift_left,
            accumulate=accumulate,
            normalise=normalise,
            label=file)

    # format settings
    # tick label
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    #ax.xaxis.set_minor_formatter(monthsFmt)
    ax.autoscale_view()

    plt.title('Number of commits over time (' + time_unit + 's)')
    fig.autofmt_xdate()
    plt.legend(loc='upper left')

    if not output_file == None:
        plt.savefig(output_file)
    if not hide:
        plt.show()


if __name__ == '__main__':
    args = docopt(__doc__)
    #TODO shift left : true or false
    #TODO accumulate: true or false
    #TODO normalize: true or false
    try:
        Regex('day|week|month|year').validate(args['--time'])
    except SchemaError as e:
        print("Invalid argument:")
        exit(e)
    plot(
        files=args['<files>'],
        time_unit=args['--time'],
        shift_left=args['--shiftleft'],
        accumulate=args['--acc'],
        normalise=args['--norm'],
        hide=args['--hide'],
        output_file=args['--out'],
    )