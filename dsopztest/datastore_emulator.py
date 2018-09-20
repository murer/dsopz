import subprocess
import time
from dsopz.http import req_text

class DSEmulator(object):

    def start(self):
        self.server = subprocess.Popen(
            [ 'gcloud', 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk' ]
        )

    def wait(self):
        self.server.wait()

    def shutdown(self):
        req_text('POST', 'http://localhost:8082/shutdown', '')
        self.wait()

def main():
    server = DSEmulator()
    server.start()
    time.sleep(5)
    server.shutdown()
    server.wait()

if __name__ == '__main__':
    main()
