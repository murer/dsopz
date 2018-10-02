from distutils.core import setup

version = '2.0.beta2'

setup(
  name = 'dsopz',
  packages = ['dsopz','dsopz.cmd'],
  version = version,
  description = 'Google Datastore Operations',
  entry_points = {
      "console_scripts": [
          "dsopz = dsopz"
      ]
  },
  author = 'Paulo Henrique Murer',
  author_email = 'paulo.murer@gmail.com',
  url = 'https://github.com/murer/dsopz',
  download_url = 'https://github.com/murer/dsopz/tarball/dsopz-%s' % (version),
  keywords = ['gae', 'datastore', 'appengine'],
  classifiers = [],
)
