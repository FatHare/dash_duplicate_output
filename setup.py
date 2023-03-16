import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='dash_duplicate_output',
    packages=['dash_duplicate_output'],
    package_dir={'dash_duplicate_output':'src'},
    version='0.0.1',
    author='Kryizhnyiy Ilya',
    author_email='kryizhnyiy.ie@gmail.com',
    description=(
        'package for the ability to specify the same output in different'
        'callbacks (solves the error of duplicate outputs).'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/FatHare/dash_duplicate_output',
    license='MIT',
    install_requires=['dash>=2.3.1', 'MarkupSafe>=2.1.2']
)