from distutils.core import setup
import dsopz.config as config

setup(
  name = 'dsopz',
  packages = ['dsopz'],
  version = config.version,
  description = 'Google Datastore Operations',
  entry_points = {
      "console_scripts": [
          "dsopz = dsopz:main",
      ]
  },
  author = 'Paulo Henrique Murer',
  author_email = 'fuweweu@gmail.com',
  url = 'https://github.com/murer/dsopz', 
  download_url = 'https://github.com/murer/dsopz/tarball/dsopz-%s' % (config.version),
  keywords = ['gae', 'datastore', 'appengine'],
  classifiers = [],
)

