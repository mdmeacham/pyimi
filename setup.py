import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyimi",
    version="0.0.5",
    author="Mike Meacham",
    author_email="mdmeacham@gmail.com",
    description="A python library for accessing IGEL\'s IMI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdmeacham/pyimi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
