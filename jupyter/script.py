from __future__ import print_function, unicode_literals
from builtins import zip
import argparse
import logging
import os
import time

import shutil

import muscima.dataset

__version__ = "0.0.1"
__author__ = "Jan Hajic jr."


def build_argument_parser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-r', '--root', action='store',
                        default=muscima.dataset.CVC_MUSCIMA_ROOT,
                        help='CVC-MUSCIMA dataset root directory (should'
                             ' contain subdirectories named after the'
                             ' CVC-MUSCIMA distortions).')
    parser.add_argument('-o', '--outdir', action='store',
                        help='Output directory for the copied files.'
                             ' If it does not exist, it will be created.')
    parser.add_argument('-i', '--items', action='store', nargs='+',
                        help='A list of writer:page pairs, such as 22:4.')
    parser.add_argument('-f', '--format', action='store',
                        default='CVC-MUSCIMA_W-{w:02}_N-{n:02}_D-ideal',
                        help='The desired output filenames. {w} and {n}'
                             ' stand for writer and page number: for'
                             ' item 4:22, for instance, the filename'
                             ' would be CVC_MUSCIMA_W-22_N-04_D-ideal.png'
                             ' (the *.png suffix is retained from the'
                             ' corresponding CVC-MUSCIMA file).')
    parser.add_argument('-m', '--mode', action='store', default='symbol',
                        help='The CVC-MUSCIMA image mode: \'full\', \'symbol\','
                             ' or \'staff_only\'.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Turn on INFO messages.')
    parser.add_argument('--debug', action='store_true',
                        help='Turn on DEBUG messages.')

    return parser


def main(args):
    logging.info('Starting main...')
    _start_time = time.perf_counter()

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    dataset = muscima.dataset.CVC_MUSCIMA(root=args.root)

    writers = []
    pages = []
    for item in args.items:
        ws, ps = item.split(':')
        writers.append(int(ws))
        pages.append(int(ps))

    for w, p in zip(writers, pages):
        imfile = dataset.imfile(page=p, writer=w,
                                distortion='ideal',
                                mode=args.mode)
        # Format the filename
        _, out_ext = os.path.splitext(imfile)
        out_fname = args.format.format(w=w, n=p) + out_ext
        out_file = os.path.join(args.outdir, out_fname)
        # Copy the file
        shutil.copyfile(imfile, out_file)

    _end_time = time.perf_counter()
    logging.info('get_images_from_muscima.py done in {0:.3f} s'
                 ''.format(_end_time - _start_time))




if __name__ == '__main__':
    parser = build_argument_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    if args.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    main(args)