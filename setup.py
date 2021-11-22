import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CompoTree", # Replace with your own username
    version="0.0.1",
    author="seantyh",
    author_email="seantyh@gmail.com",
    description="A unicode IDS component tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seantyh/ComponentTree",
    package_dir = {'': 'src'},
    packages=['CompoTree'],
    package_data={
        "": ["data/*.txt", "data/*.pkl"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
