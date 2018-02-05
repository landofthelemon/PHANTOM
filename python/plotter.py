"""
Usage:
    plotter_v2.py (peak|line|euclidean) <id>... --timeunit=<UNIT> [options]

Arguments:
    -t --timeunit=<UNIT>    Time unit of the x axis. Units: day, week, month, year
Options:
    -h --help           Show this screen.
    -h --hide           Hide the diagram / Don't show the diagram
    -o --out=<file>     Path to output file. You can specify the file format by using the desired file extension (e.g. png, pdf)
    --shift=<direction> Shift the dates of projects [values: left, right]
    --norm              Normalises all y values to be between 0 and 1
    --acc               Accumulate y values
"""
from docopt import docopt
import data_provider as provider
import data_processor as processor
import matplotlib.pyplot as pyplot

if __name__ == '__main__':
    args = docopt(__doc__)
    print args
    # Validate command line arguments ----------------------------------------------------------------------------------
    valid_timeunits = ["day", "week", "month", "year"]
    if not args['--timeunit'] in valid_timeunits:
        print("Invalid timeunit. Use --help to get more information.")
        exit(1)

    valid_shift_values = ["left", "right", None]
    if not args['--shift'] in valid_shift_values:
        print("Invalid shift value. Use --help to get more information.")
        exit(1)

    # Process command line arguments -----------------------------------------------------------------------------------
    convert_date_functions = {
        "day": provider.DateUtil.date_to_day,
        "week": provider.DateUtil.date_to_week,
        "month": provider.DateUtil.date_to_month,
        "year": provider.DateUtil.date_to_year,
    }

    arg_ids = args['<id>']
    arg_time_unit = args['--timeunit']
    arg_acc = args['--acc']
    arg_norm = args['--norm']
    arg_shift = args['--shift']

    # Get the data -----------------------------------------------------------------------------------------------------
    data = provider.get_commit_frequencies(arg_ids, convert_date_functions[arg_time_unit])
    
    # Process the data -------------------------------------------------------------------------------------------------
    data = processor.process(data, accumulate=arg_acc, normalise=arg_norm, shift=arg_shift)

    # Plot the specified graph -----------------------------------------------------------------------------------------
    if (args['peak']):
        pass
    elif args['line']:
        pass
    elif args['euclidean']:
        pass

    fig, ax = pyplot.subplots()
    plot_fun = ax.plot_date
    if not arg_shift is None:
        plot_fun = ax.plot
    for row in data:
        #ax.plot_date(row[0], row[1], '-')
        plot_fun(row[0], row[1], '-')

    pyplot.title('Number of commits over time (' + arg_time_unit + 's)')
    fig.autofmt_xdate()
    pyplot.legend(loc='upper left')
    pyplot.show()