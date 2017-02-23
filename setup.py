from setuptools import setup, find_packages

setup(
    name='NeteaseDownloader',
    version='1.0',
    keywords=('netease', 'music', 'downloader', 'download'),
    description='Neteasy Music/Ablum/Playlist downloader.',
    long_description='netease -music 29414460[-music, -ablum, -playlist] -thread 4',
    author='MyFaith',
    author_email='faith0725@outlook.com',
    url='https://github.com/MyFaith/netease-downloader',
    license='MIT',
    packages = find_packages(),
    install_requires = ['requests', 'gevent'],
    entry_points={
        'console_scripts': [
            'netease = netease.cmdline:execute'
        ]
    }
)
