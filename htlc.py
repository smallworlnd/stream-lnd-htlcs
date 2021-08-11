from lnd_grpc import router_pb2 as lnrouter
from lnd_grpc import rpc_pb2 as lnrpc
from lnd import Lnd
import datetime

class Htlc:
    def __init__(self, lnd, htlc, humandates):
        if getattr(htlc, 'incoming_channel_id') != 0:
            self.incoming_channel = lnd.get_alias_from_channel_id(htlc.incoming_channel_id)
            self.incoming_channel_capacity = lnd.get_channel_capacity(htlc.incoming_channel_id)
            self.incoming_channel_remote_balance = lnd.get_channel_remote_balance(htlc.incoming_channel_id)
            self.incoming_channel_local_balance = lnd.get_channel_local_balance(htlc.incoming_channel_id)
        else:
            self.incoming_channel = lnd.get_own_alias()
        if getattr(htlc, 'outgoing_channel_id') != 0:
            self.outgoing_channel = lnd.get_alias_from_channel_id(htlc.outgoing_channel_id)
            self.outgoing_channel_capacity = lnd.get_channel_capacity(htlc.outgoing_channel_id)
            self.outgoing_channel_remote_balance = lnd.get_channel_remote_balance(htlc.outgoing_channel_id)
            self.outgoing_channel_local_balance = lnd.get_channel_local_balance(htlc.outgoing_channel_id)
        else:
            self.outgoing_channel = lnd.get_own_alias()
        if humandates == "false":
            self.timestamp = int(htlc.timestamp_ns/1e9)
        else:
            self.timestamp = datetime.datetime.utcfromtimestamp(int(htlc.timestamp_ns/1e9)).strftime('%Y-%m-%d %H:%M:%S')
        self.event_type = self.get_enum_name_from_value(htlc.EventType.items(), htlc.event_type)
        self.event_outcome = self.get_enum_name_from_value(htlc.DESCRIPTOR.fields_by_name.items(), htlc.ListFields()[-1][0].number)

        if self.event_outcome == 'link_fail_event':
            self.wire_failure = self.get_enum_name_from_value(lnrpc.Failure.FailureCode.items(), htlc.link_fail_event.wire_failure)
            self.failure_detail = self.get_enum_name_from_value(lnrouter.FailureDetail.items(), htlc.link_fail_event.failure_detail)
            self.failure_string = htlc.link_fail_event.failure_string
            self.event_outcome_info = self.get_event_info_enum_names_from_values(htlc.link_fail_event)
        elif self.event_outcome == 'forward_event':
            self.event_outcome_info = self.get_event_info_enum_names_from_values(htlc.forward_event)


    @staticmethod
    def get_enum_name_from_value(descriptor_items, value):
        for item_key, item_value in descriptor_items:
            if hasattr(item_value, 'number') and item_value.number == value or item_value == value:
                return item_key
        return None

    @staticmethod
    def get_event_info_enum_names_from_values(htlc_event):
        event_outcome_info = {}
        for f1, v1 in htlc_event.info.ListFields():
            for f2, v2 in htlc_event.info.DESCRIPTOR.fields_by_name.items():
                if f1 == v2:
                    event_outcome_info[f2] = v1
        return event_outcome_info
