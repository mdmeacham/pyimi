import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="igel",
    version="0.0.1",
    author="Mike Meacham",
    author_email="mdmeacham@gmail.com",
    description="A python library for accessing IGEL\'s IMI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdmeacham/imi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)