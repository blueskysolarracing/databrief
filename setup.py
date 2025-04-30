from setuptools import find_packages, setup

setup(
    name='databrief',
    version='0.0.2',
    description='A python library for serializing dataclasses to bytes and back.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/blueskysolarracing/databrief',
    author='Blue Sky Solar Racing',
    author_email='blueskysolar@studentorg.utoronto.ca',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.13',
    ],
    keywords=['dataclass', 'serialization'],
    project_urls={
        'Source': 'https://github.com/blueskysolarracing/databrief',
        'Tracker': 'https://github.com/blueskysolarracing/databrief/issues',
    },
    packages=find_packages(),
    python_requires='>=3.11',
    package_data={'databrief': ['py.typed']},
)
