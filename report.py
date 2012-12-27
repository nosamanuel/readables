import sys
import pprint

from readables.backends import get_backend


def main(script, *args):
    """
    Service can be one of:

    - readability
    - instapaper
    - pocket
    """
    backend = get_backend('readability')()
    report = backend.get_report()
    pprint.pprint(report)


if __name__ == '__main__':
    main(*sys.argv)
