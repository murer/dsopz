from distutils.core import setup

version = '2.0.beta10'

setup(
  name = 'dsopz',
  packages = ['dsopz'],
  version = version,
  description = 'Google Datastore Operations',
  entry_points = {
      "console_scripts": [
          "dsopz = dsopz.main:main"
      ]
  },
  author = 'Paulo Henrique Murer',
  author_email = 'paulo.murer@gmail.com',
  url = 'https://github.com/murer/dsopz',
  download_url = 'https://github.com/murer/dsopz/tarball/dsopz-%s' % (version),
  keywords = ['gae', 'datastore', 'appengine'],
  classifiers= [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
