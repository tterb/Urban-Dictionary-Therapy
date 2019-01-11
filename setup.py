import setuptools

with open('README.md') as f:
  long_description = f.read()

setuptools.setup(
  name = 'UDTherapy',
  version = '1.0.0',
  description = 'A simple rehabilitation program for coping with long days of programming',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Brett Stevenson',
  author_email = 'bstevensondev@gmail.com',
  url = 'https://github.com/tterb/Urban-Dictionary-Therapy',
  download_url = 'https://github.com/tterb/Urban-Dictionary-Therapy/archive/1.0.0.tar.gz',
  keywords = ['urban', 'dictionary', 'therapy', 'funny', 'entertainment', 'cli'],
  packages = setuptools.find_packages(),
  scripts=['bin/UDTherapy'],
  setup_requires=['pytest-runner'],
  tests_require=['pytest'],
  install_requires=[
    'colorama==0.4.1',
    'beautifulsoup4==4.6.3',
  ],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ]
)
