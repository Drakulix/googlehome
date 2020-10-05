# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.internal.home.foyer import v1_pb2 as google_dot_internal_dot_home_dot_foyer_dot_v1__pb2


class HomeControlServiceStub(object):
    """Home Control Service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAssistantRoutines = channel.unary_stream(
                '/google.internal.home.foyer.v1.HomeControlService/GetAssistantRoutines',
                request_serializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.None.SerializeToString,
                response_deserializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetAssistantRoutinesResponse.FromString,
                )


class HomeControlServiceServicer(object):
    """Home Control Service
    """

    def GetAssistantRoutines(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HomeControlServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAssistantRoutines': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAssistantRoutines,
                    request_deserializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.None.FromString,
                    response_serializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetAssistantRoutinesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.internal.home.foyer.v1.HomeControlService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class HomeControlService(object):
    """Home Control Service
    """

    @staticmethod
    def GetAssistantRoutines(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/google.internal.home.foyer.v1.HomeControlService/GetAssistantRoutines',
            google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.None.SerializeToString,
            google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetAssistantRoutinesResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)


class StructuresServiceStub(object):
    """Structure Service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetHomeGraph = channel.unary_unary(
                '/google.internal.home.foyer.v1.StructuresService/GetHomeGraph',
                request_serializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetHomeGraphRequest.SerializeToString,
                response_deserializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetHomeGraphResponse.FromString,
                )


class StructuresServiceServicer(object):
    """Structure Service
    """

    def GetHomeGraph(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StructuresServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetHomeGraph': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHomeGraph,
                    request_deserializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetHomeGraphRequest.FromString,
                    response_serializer=google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetHomeGraphResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.internal.home.foyer.v1.StructuresService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class StructuresService(object):
    """Structure Service
    """

    @staticmethod
    def GetHomeGraph(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.internal.home.foyer.v1.StructuresService/GetHomeGraph',
            google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetHomeGraphRequest.SerializeToString,
            google_dot_internal_dot_home_dot_foyer_dot_v1__pb2.GetHomeGraphResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
