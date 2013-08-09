from distutils.core import setup

setup(
    name='ovirt-scheduler-proxy',
    version='0.1',
    license='ASL2',
    description='oVirt Scheduler Proxy',
    author='Laszlo Hornyak',
    author_email='lhornyak@redhat.com',
    url='http://www.ovirt.org/Features/oVirt_External_Scheduling_Proxy',
    packages=['ovirtscheduler'],
    package_dir={ '': 'src' },
    long_description=open('README').read(),
)

