import setuptools
import os.path

# from official Python version-detection recommendations: https://packaging.python.org/guides/single-sourcing-package-version/

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'deepgram', '_version.py'), encoding="utf8") as file:
    exec(file.read())
# imports as __version__

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding="utf8") as file:
    long_description = file.read()

setuptools.setup(
    name='deepgram-sdk',
    version=__version__, # type: ignore
    description='The official Python SDK for the Deepgram automated speech recognition platform.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/deepgram/deepgram-python-sdk',
    author='Luca Todd',
    author_email='luca.todd@deepgram.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='deepgram speech-to-text',
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp',
        'websockets',
        'typing-extensions; python_version < "3.8.0"'
    ],
)