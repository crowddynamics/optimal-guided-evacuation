from setuptools import setup, find_packages

import versioneer


def readfile(filepath):
    with open(filepath) as f:
        return f.read()


setup(
    name='qtgui',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='',
    long_description=readfile('README.rst'),
    author='Jaan Tollander de Balsch',
    author_email='de.tollander@aalto.fi',
    url='https://github.com/jaantollander/crowddynamics-qtgui',
    license=readfile('LICENSE.txt'),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'crowddynamics-qtgui=qtgui.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT'
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # test_suite='',
    # test_requirements=[],
)
