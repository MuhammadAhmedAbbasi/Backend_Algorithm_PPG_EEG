from concurrent import futures
import grpc

from dependencies import get_logger

from grpc_modules.impl import greet_service, eeg_service
from grpc_modules.generated import greet_pb2_grpc, eeg_pb2_grpc

logger = get_logger()

def add_service(server):
    greet_pb2_grpc.add_GreeterServicer_to_server(greet_service.Greeter(), server)
    eeg_pb2_grpc.add_EegServicer_to_server(eeg_service.EegService(), server)
    return server

async def start_grpc_server(port: int = 8091):
    try:
        logger.info("Starting gRPC server")
        server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        server.add_insecure_port('[::]:' + str(port))
        add_service(server)
        await server.start()
        logger.info("gRPC server started")
        await server.wait_for_termination()
    except Exception as e:
        logger.error(f"Error starting gRPC server: {e}")

def start_grpc_server_sync(port: int = 8091):
    try:
        logger.info("Starting gRPC server")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server.add_insecure_port('[::]:' + str(port))
        add_service(server)
        server.start()
        logger.info("gRPC server started")
        server.wait_for_termination()
    except Exception as e:
        logger.error(f"Error starting gRPC server: {e}")