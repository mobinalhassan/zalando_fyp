
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snapthat",
    version="0.3.5",
    author="snapthat",
    author_email="harris.perceptron@gmail.com",
    description="One common utilities to rule them all",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/snapthatxyz/core/commonutils.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'numpy',
        'pymongo',
        'boto3',
        'redis',
        'Pillow',
        'matplotlib',
        'Flask',
        'tqdm'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)