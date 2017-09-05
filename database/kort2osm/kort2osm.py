"""
kort-to-osm

Usage:
  kort2osm.py [-d] [-q] [-v] [-c COUNT]
  kort2osm.py -h | --help
  kort2osm.py --version

Options:
  -h, --help               Show this help message and exit.
  -d, --dry                Do not actually make changes, only a dry run
  -q, --quiet              Run quietly, without any output.
  -v, --verbose            Show more verbose output.
  -c COUNT, --count=COUNT  Count of fixes to run through from kort to OSM.
  --version                Show the version and exit.

"""
import os
import logging

import docopt

from helper import osm_fix


__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


def setup_logging():
    logger=logging.getLogger(__name__)
    handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'kort2osm.log'))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='kort-to-osm 0.1')

    # Set up logging
    if arguments['--quiet']:
        logging.basicConfig(level=logging.WARNING)
    elif arguments['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        setup_logging()

    # Handle a dry run
    if arguments['--dry']:
        print('### Dry run: ###')

    # Apply the fixes from kort to OSM
    try:
        limit = int(arguments['--count'])
    except TypeError:
        limit = 1
    osm = osm_fix.OsmFix()
    osm.apply_kort_fix(limit, arguments['--dry'])
