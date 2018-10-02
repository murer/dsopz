import subprocess
from dsopz import util
from dsopz.http import req_text
import os
from threading import RLock

class Error(Exception):
    """Exceptions"""

class DSEmulator(object):

    def __init__(self):
        self._clients = 0
        self._lock = RLock()

    def boot(self):
        cmd = 'gen/google-cloud-sdk/bin/gcloud'
        if not os.path.isfile(cmd):
            cmd = 'gcloud'
        self.server = subprocess.Popen(
            [ cmd, 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk', '--consistency', '1.0' ]
        )
        util.wait_check_port('localhost', 8082)

    def wait(self):
        self.server.wait()

    def shutdown(self):
        req_text('POST', 'http://localhost:8082/shutdown', '')
        self.wait()

    def start(self):
        with self._lock:
            print('start', self._clients)
            if self._clients < 0:
                raise Error('wrong')
            if self._clients == 0:
                self.boot()
            self._clients = self._clients + 1

    def stop(self):
        with self._lock:
            print('stop', self._clients)
            if self._clients <= 0:
                raise Error('wrong')
            self._clients = self._clients - 1
            if self._clients == 0:
                self.shutdown()

dsemulator = DSEmulator()

def main():
    server = DSEmulator()
    server.start()
    server.stop()

if __name__ == '__main__':
    main()
