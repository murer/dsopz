import subprocess
import time
from dsopz.http import req_text

class DSEmulator(object):

    def start(self):
        self.server = subprocess.Popen(
            [ 'gcloud', 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk' ]
        )

    def shutdown(self):
        req_json('POST', 'http://localhost:8082/shutdown', '')

def main():
    server = subprocess.Popen(
        [ 'gcloud', 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk' ]
    )
    print('xxx', server)
    time.sleep(5)
    req_text('POST', 'http://localhost:8082/shutdown', '')
    server.wait()

if __name__ == '__main__':
    main()
