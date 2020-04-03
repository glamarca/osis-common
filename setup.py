import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osis-common",
    version="0.1",
    description="osis-common version 0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glamarca/osis-common",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4"
        "Operating System :: Unix",
    ],
    python_requires='>=3.4',
    install_requires=['osis', 'Django>=1.10']
)