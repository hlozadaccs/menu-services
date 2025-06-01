import signal
import sys
from concurrent import futures

import grpc

from interfaces.grpc.generated import menu_pb2_grpc
from interfaces.services.menu_services import MenuService
from main import create_app

app = create_app()


def graceful_shutdown(signum, frame):
    print("Terminando GRPC")
    server.stop(0)
    sys.exit(0)


def serve():
    global server  # Para acceder desde graceful_shutdown
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    menu_pb2_grpc.add_MenuServiceServicer_to_server(MenuService(), server)
    server.add_insecure_port("[::]:50051")

    # Manejar señales de terminación
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    server.start()
    print("🚀 gRPC server running on port 50051 (Ctrl+C para detener)")

    with app.app_context():
        server.wait_for_termination()


if __name__ == "__main__":
    serve()
