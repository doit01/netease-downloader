from setuptools import setup, find_packages

setup(
    name='NeteasyDownloader',
    version='0.6',
    keywords=('neteasy', 'music', 'downloader', 'download'),
    description='Neteasy Music/Ablum/Playlist downloader.',
    long_description='neteasy -m 29414460 [-m music, -a ablum, -p playlist]',
    author='MyFaith',
    author_email='faith0725@outlook.com',
    url='https://github.com/MyFaith/neteasy-downloader',
    license='MIT',
    packages = find_packages(),
    install_requires = ['requests', 'gevent'],
    entry_points={
        'console_scripts': [
            'neteasy = neteasy.cmdline:execute'
        ]
    }
)
