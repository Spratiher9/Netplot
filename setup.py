import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netplot",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Souvik Pratiher",                     # Full name of the author
    description="Ultralight 3D renderer of neural network architecture for TF/Keras Models",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["netplot"],             # Name of the python package
    package_dir={'':'src'},     # Directory of the source code of the package
    install_requires=[
        "cycler==0.10.0",
        "kiwisolver==1.3.2",
        "matplotlib==3.4.3",
        "numpy==1.21.2",
        "Pillow==8.3.2",
        "pyparsing==2.4.7",
        "python-dateutil==2.8.2",
        "six==1.16.0"
    ]                     # Install other dependencies if any
)

