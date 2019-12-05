import setuptools
from subprocess import STDOUT, check_call
import os


check_call(['sudo', 'apt-get', 'install', 'libdbus-glib-1-dev libdbus-glib-1-dev'],
           stdout=open(os.devnull, 'wb'), stderr=STDOUT)

check_call(['sudo', 'python', 'copytosystemd.py'],
           stdout=open(os.devnull, 'wb'), stderr=STDOUT)

check_call(['sudo', 'python', 'model_location.py'],
           stdout=open(os.devnull, 'wb'), stderr=STDOUT)


setuptools.setup(
    name='vplocation',
    version='0.1',
    description='Location system',
    url='https://vozplus.com/es',
    author='Danien Urbano',
    author_email='dannybombastic@gmail.com',
    license='MIT',
    packages=['vplocation'],
    zip_safe=False,
    install_requires=[
        'certifi==2018.4.16',
        'chardet==3.0.4',
        'coverage==5.0a1',
        'dbus-python==1.2.8',
        'idna==2.7',
        'netaddr==0.7.19',
        'pbkdf2==1.3',
        'PyRIC==0.1.6.3',
        'python-networkmanager==2.1',
        'requests==2.19.1',
        'six==1.11.0',
        'SQLAlchemy==1.2.8',
        'termcolor==1.1.0',
        'urllib3==1.23',
        'wifi==0.3.8',
    ],
)
