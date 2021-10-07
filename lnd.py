import base64
import os
from os.path import expanduser
import codecs
import grpc
import sys
from lnd_grpc import rpc_pb2 as ln
from lnd_grpc import rpc_pb2_grpc as lnrpc
from lnd_grpc import router_pb2 as lnrouter
from lnd_grpc import router_pb2_grpc as lnrouterrpc

MESSAGE_SIZE_MB = 50 * 1024 * 1024


class Lnd:
    def __init__(self, lnd_dir, host, tls_path, macaroon_path):
        os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
        lnd_dir = expanduser(lnd_dir)
        combined_credentials = self.get_credentials(lnd_dir, tls_path, macaroon_path)
        channel_options = [
            ('grpc.max_message_length', MESSAGE_SIZE_MB),
            ('grpc.max_receive_message_length', MESSAGE_SIZE_MB)
        ]
        grpc_channel = grpc.secure_channel(host, combined_credentials, channel_options)
        self.stub = lnrpc.LightningStub(grpc_channel)
        self.router_stub = lnrouterrpc.RouterStub(grpc_channel)
        self.info = None
        self.channels = None

    @staticmethod
    def get_credentials(lnd_dir, tls_path, macaroon_path):
        
        if not tls_path:
            tls_path = lnd_dir + '/tls.cert'

        if not macaroon_path:
            macaroon_path = lnd_dir + '/data/chain/bitcoin/mainnet/readonly.macaroon'
            
        tls_certificate = open(tls_path, 'rb').read()
        ssl_credentials = grpc.ssl_channel_credentials(tls_certificate)
        macaroon = codecs.encode(open(macaroon_path, 'rb').read(), 'hex')
        auth_credentials = grpc.metadata_call_credentials(lambda _, callback: callback([('macaroon', macaroon)], None))
        combined_credentials = grpc.composite_channel_credentials(ssl_credentials, auth_credentials)
        return combined_credentials

    def get_node_alias(self, pub_key):
        return self.stub.GetNodeInfo(ln.NodeInfoRequest(pub_key=pub_key, include_channels=False)).node.alias

    def get_channels(self):
        return self.stub.ListChannels(ln.ListChannelsRequest(active_only=False)).channels

    def get_alias_from_channel_id(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return self.get_node_alias(channel.remote_pubkey)

    def get_channel_capacity(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.capacity

    def get_channel_capacity(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.capacity

    def get_channel_local_balance(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.local_balance

    def get_channel_remote_balance(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.remote_balance

    def get_info(self):
        return self.stub.GetInfo(ln.GetInfoRequest())

    def get_own_pubkey(self):
        return self.get_info().identity_pubkey

    def get_own_alias(self):
        return self.get_info().alias

    def get_htlc_events(self):
        request = lnrouter.SubscribeHtlcEventsRequest()
        return self.router_stub.SubscribeHtlcEvents(request)
