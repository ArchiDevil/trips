from setuptools import setup, find_packages

setup(
    name='trips_organizer',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=open('requirements.txt').readlines(),

    url='https://bitbucket.org/ArchiDevil/trips/',
    author='Denis Bezykornov',
    author_email='archidevil52@gmail.com'
)
