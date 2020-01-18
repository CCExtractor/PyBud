import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pybud',
    version='1.0.0',
    packages=['pybud'],
    entry_points={'console_scripts': ['pybud=pybud.main:main']},
    url='https://github.com/Tantan4321/PyBud',
    license='MIT',
    author='Eastan Giebler',
    author_email='kupa528@yahoo.com',
    description='A python debugger.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=['dictdiffer==0.8.1'],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
