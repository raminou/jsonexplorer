import setuptools

setuptools.setup(
    name='jsonexplorer',
    version='1.0',
    author='Raminou',
    description='Module to get only part of JSON data depending on a request string',
    packages=['jsonexplorer', 'tests'],
    entry_points = {
        'console_scripts': ['jsonexplorer=jsonexplorer.cli:main'],
    },
    install_requires=[
        'lark-parser >= 0.11.2'
    ],
    python_requires='>=3.5',
    test_suite="tests"
)
