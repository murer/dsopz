import argparse
import importer
import exporter
import reader
import console
import processor_indexed
import processor_csv
import processor_sql
import processor_update
import processor_mapper
import oauth
import oauth_gce
import oauth_installed
import oauth_local
import oauth_serviceaccount
import config

class Version(object):

    def argparse_prepare(self, sub):
        """ ok """

    def argparse_exec(self, args):
        print(config.version)

class Parser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='DSOpz')
        self.subparsers = self.parser.add_subparsers(dest="subparsers", title="Command")
        self.mods = {}

    def prepare(self, name, mod):
        sub = self.subparsers.add_parser(name)
        mod.argparse_prepare(sub)
        self.mods[name] = mod

    def handle_args(self):
        args = self.parser.parse_args()
        mod = self.mods[args.subparsers]
        mod.argparse_exec(args)

def main():
    parser = Parser()
    parser.prepare('version', Version())
    parser.prepare('console', console)
    parser.prepare('export', exporter)
    parser.prepare('import', importer)
    parser.prepare('gql', reader)
    parser.prepare('index', processor_indexed)
    parser.prepare('csv', processor_csv)
    parser.prepare('sql', processor_sql)
    parser.prepare('update', processor_update)
    parser.prepare('map', processor_mapper)
    parser.prepare('token', oauth)
    parser.prepare('login', oauth_local)
    parser.prepare('login-text', oauth_installed)
    parser.prepare('login-gce', oauth_gce)
    parser.prepare('login-serviceaccount', oauth_serviceaccount)
    parser.handle_args()

if __name__ == '__main__':
    main()
