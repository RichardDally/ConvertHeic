import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setuptools.setup(
    author="Richard Dally",
    name="convert_heic",
    version="1.0.0",
    description="Convert heic to png in command line",
    url="https://github.com/RichardDally/ConvertHeic",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
)
