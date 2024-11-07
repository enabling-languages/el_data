from setuptools import setup

setup(
    name='el_data',
    version='0.3.2',
    description='Helper functions for accessing internationalisation data',
    url='https://github.com/enabling-languages/el_data',
    author='Andrew Cunningham',
    author_email='',
    license='MIT',
    packages=['el_data'],
    install_requires=[
        'hexdump',
        'lxml',
        'pyicu',
        'requests',
        'rich'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities'
    ],
)
