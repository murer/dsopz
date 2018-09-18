import subprocess



def main():
    x = subprocess.Popen(
        [ 'gcloud', 'beta', 'emulators', 'datastore', 'start', '--host-port', 'localhost:8082', '--no-store-on-disk' ],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print('xxx', x)

if __name__ == '__main__':
    main()
