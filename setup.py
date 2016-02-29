from distutils.core import setup
from shayfara.variables import __version__

setup(
    name='shayfara',
    keywords=['backup', 'aes', 'encrypt', 'decrypt', 'encryption',
              'decryption', 'pbkdf2', 'hmac', 'secure', 'crypto',
              'cryptography'],
    url='https://github.com/ghantoos/shayfara',
    requires='simplecrypt',
    packages=['shayfara'],
    scripts=['bin/shayfara'],
    package_dir={'shayfara': 'shayfara'},
    version=__version__,
    description='A command-line-user-friendly backup encryption application',
    author='Ignace Mouzannar',
    author_email='ghantoos@ghantoos.org',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Intended Audience :: System Administrators',
                 'License :: OSI Approved :: ISC License (ISCL)',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Security',
                 'Topic :: Security :: Cryptography'],
)
