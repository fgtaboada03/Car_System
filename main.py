from LocalServer.server import start_server
import time

def main():
    print("Server Start!")
    server = start_server()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        server.loop_stop()

if __name__ == "__main__":
    main()