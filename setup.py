from distutils.core import setup

setup(
  name = 'dsopz',
  packages = ['dsopz'],
  version = '1.0.5.6',
  description = 'Google Datastore Operations',
  entry_points = {
      "console_scripts": [
          "dsopz = dsopz:main",
      ]
  },
  author = 'Paulo Henrique Murer',
  author_email = 'fuweweu@gmail.com',
  url = 'https://github.com/murer/dsopz', 
  download_url = 'https://github.com/murer/dsopz/tarball/dsopz-1.0.5', # I'll explain this in a second
  keywords = ['gae', 'datastore', 'appengine'],
  classifiers = [],


