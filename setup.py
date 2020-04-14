import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moocows-checkmate-pkg", # Replace with your own username
    version="0.0.4",
    author="MooCows",
    author_email="brennan.vandyke@eagles.oc.edu",
    description="Checkmate Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/b1dobbs/checkmate_library_d2d",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)