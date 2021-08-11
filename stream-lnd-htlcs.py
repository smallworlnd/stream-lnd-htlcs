#!/usr/bin/env python3

import argparse
from lnd import Lnd
from htlc import Htlc

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--lnd-dir", default="~/.lnd", dest="lnddir", help="lnd directory; default ~/.lnd",
    )
    arg_parser.add_argument(
        "--output-file", default="htlc-stream.json", dest="outfile", help="HTLC stream output file; default htlc-stream.json",
    )
    arg_parser.add_argument(
        "--stream-mode", default="false", dest="streammode", help="Stream output to stdout only; default false",
    )
    arg_parser.add_argument(
        "--silent", default="false", dest="silent", help="Disable stdout output; default false",
    )
    arg_parser.add_argument(
        "--human-dates", default="false", dest="humandates", help="Human friendly datetime; default false",
    )
    args = arg_parser.parse_args()

    lnd = Lnd(args.lnddir)

    for response in lnd.get_htlc_events():
        htlc = Htlc(lnd, response, args.humandates)
        if args.silent == "false":
            print(htlc.__dict__)
        if args.streammode == "false":
            with open(args.outfile, 'a') as f:
                print(htlc.__dict__, file=f)


if __name__ == "__main__":
    main()
