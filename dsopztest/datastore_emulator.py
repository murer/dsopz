import subprocess
from dsopz import util
from dsopz.http import req_text

class DSEmulator(object):

    def start(self):
        self.server = subprocess.Popen(
            [ 'gcloud', 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk' ]
        )
        util.wait_check_port('localhost', 8082)

    def wait(self):
        self.server.wait()

    def shutdown(self):
        req_text('POST', 'http://localhost:8082/shutdown', '')
        self.wait()

def main():
    server = DSEmulator()
    server.start()
    server.shutdown()

if __name__ == '__main__':
    main()
