import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pybud',
    version='0.2.0',
    packages=['pybud', 'pybud.tests'],
    entry_points={'console_scripts': ['pybud=pybud.main:main']},
    license='MIT',
    author='Eastan Giebler',
    author_email='kupa528@yahoo.com',
    url='https://github.com/Tantan4321/PyBud',
    download_url='https://github.com/Tantan4321/PyBud/archive/v0.2.0.tar.gz',
    description='A python tool for debugging and profiling python functions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['debugger', 'tool', 'python', 'video'],
    install_requires=['dictdiffer==0.8.1', 'Pillow==7.0.0', 'opencv-python', 'numpy'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
