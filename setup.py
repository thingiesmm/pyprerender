from setuptools import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setuptools.setup(
    name='pyprerender',
    version='0.0.4',
    author='Matas Minelga',
    author_email='minematas@gmail.com',
    description='A python prerender',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/thingiesmm/pyprerender',
    python_requires='>=3.7',
    install_requires=requirements,
    package_dir={"": "src"},
    packages=['pyprerender'],
    zip_safe=False,
    license='MIT',
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
