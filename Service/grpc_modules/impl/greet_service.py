from ..generated import greet_pb2, greet_pb2_grpc


class Greeter(greet_pb2_grpc.GreeterServicer):
    """
    Greeter service implementation
    """

    async def SayHello(self, request: greet_pb2.HelloRequest, context):
        """
        implementation of SayHello
        """
        return greet_pb2.HelloReply(
            message="Hello, %s! (By Mental Connect Backend Algorithm)" % request.name
        )
