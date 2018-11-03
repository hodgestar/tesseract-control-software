from setuptools import setup, find_packages

setup(
    name="tessled",
    version="0.0.1",
    url='http://github.com/hodgestar/tesseract-control-software',
    license='MIT',
    description="Tesseract control software and simulator.",
    long_description=open('README.rst', 'r').read(),
    author='Simon Cross',
    author_email='hodgestar+tesseract@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'numpy',
        'randomcolor',
        'zmq',
    ],
    extras_require={
        'simulator': ['faulthandler', 'pygame_cffi', 'PyOpenGL'],
    },
    entry_points={  # Optional
        'console_scripts': [
            'tesseract-effectbox=tessled.effectbox:main',
            'tesseract-simulator=tessled.simulator:main',
        ],
    },
    scripts=[
        'bin/tesseract-runner',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment',
    ],
)
