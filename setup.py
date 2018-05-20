from distutils.core import setup

setup(
    name='Screencaster',
    version='1.0',
    description='Record Desktop screen.',
    author='Michael Hegarty',
    author_email='horace.iii.3@gmx.com',
    url='',
    packages={'modules'}, install_requires={'PyQt5', 'python-vlc'}, requires=['PyQt5']
)

