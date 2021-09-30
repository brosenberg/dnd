import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="second_gen",
    version="0.0.3",
    author="Ben Rosenberg",
    author_email="scdlbx@gmail.com",
    description="A generator of 2nd edition things",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brosenberg/dnd/tree/master/2e",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "src"},
    #packages=setuptools.find_packages(where="src"),
    packages=["second_gen"],
    package_dir={"second_gen": "src/second_gen"},
    include_package_data=True,
    package_data={"second_gen":
        [
            "spells/*.json", 
            "tables/*.json", 
        ]
    },
    python_requires=">=3.7",
)
