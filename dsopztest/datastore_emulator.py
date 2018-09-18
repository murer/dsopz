import subprocess
import time
from dsopz.http import req_json

def main():
    server = subprocess.Popen(
        [ 'gcloud', 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk' ]
    )
    print('xxx', server)
    time.sleep(5)
    req_json('POST', 'http://localhost:8082/shutdown', '')
    time.sleep(5)
    server.kill()

if __name__ == '__main__':
    main()
