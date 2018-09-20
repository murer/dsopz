import subprocess
from dsopz import util
from dsopz.http import req_text
import os

class DSEmulator(object):

    def start(self):
        cmd = 'gen/google-cloud-sdk/bin/gcloud'
        if not os.path.isfile(cmd):
            cmd = 'gcloud'
        self.server = subprocess.Popen(
            [ cmd, 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk' ]
        )
        util.wait_check_port('localhost', 8082, sleep=1)

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
