import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ovirt-scheduler-proxy',
    version=read('VERSION').strip(),
    license='ASL2',
    description='oVirt Scheduler Proxy',
    author='Doron Fediuck',
    author_email='dfediuck@redhat.com',
    url='http://www.ovirt.org/Features/oVirt_External_Scheduling_Proxy',
    packages=find_packages("src"),
    package_dir={'':'src'},
    long_description=read('README'),
)

