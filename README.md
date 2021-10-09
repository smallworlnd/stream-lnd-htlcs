# stream-lnd-htlcs

Stream all HTLC events from an `lnd` node. Includes information about event type, event fate, incoming/outgoing peers, incoming/outgoing channel balance, and additional information depending on the event type. Basically, it's the default HTLC stream provided by the gRPC API but with a little spice.

## Installation

You'll need an active `lnd`, version 0.9.0+ (https://github.com/lightningnetwork/lnd), with routerrpc built in, Python 3 and the requirements.

Get the Repository in the directory where you want to install
```
git clone https://github.com/smallworlnd/stream-lnd-htlcs
```
Change Directory
```
cd stream-lnd-htlcs
```
Install

```
pip3 install -r requirements.txt
```

## Usage

Running the script will output HTLC event information both to the screen and to a file.

### Command line arguments

```
usage: stream-lnd-htlcs.py [-h] [--lnd-dir LNDDIR] [--output-file OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  --lnd-dir LNDDIR      lnd directory; default ~/.lnd
  --host HOST           host (node) to connect to; default localhost:10009
  --tls TLS             Path to tls.cert. Used as an alternative to --lnd-dir
  --macaroon MACAROON   Path to read_only.macaroon. Used as an alternative to --lnd-dir
  --output-file OUTFILE
                        HTLC stream output file; default htlc-stream.json
  --stream-mode 
                        If flagged no file will be written only streamed to stdout; default: false
  --silent 
                        If flagged will not output to stdout; default: false
  --human-dates
                        Human friendly datetime; default: false
```

### Example output

```
{"incoming_channel": "LN-node1-alias", "outgoing_channel": "LN-node2-alias", "outgoing_channel_capacity": 5000000, "outgoing_channel_remote_balance": 2500000, "outgoing_channel_local_balance": 2500000, "timestamp": 1626750720, "event_type": "SEND", "event_outcome": "forward_fail_event"}
...
{"incoming_channel": "LN-nodeX-alias", "incoming_channel_capacity": 5000000, "incoming_channel_remote_balance": 2500000, "incoming_channel_local_balance": 7500000, "outgoing_channel": "LN-nodeY-alias", "outgoing_channel_capacity": 10000000, "outgoing_channel_remote_balance": 5000000, "outgoing_channel_local_balance": 5000000, "timestamp": 1626751932, "event_type": "FORWARD", "event_outcome": "settle_event"}
```
