import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoQuant",
    version="0.4.0",
    author="NAUTIDEA",
    author_email="xian@nautidea.com",
    description="Auto Quant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcnuth/AutoQuant",
    project_urls={
        "Bug Tracker": "https://github.com/marcnuth/AutoQuant/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "autoquant"},
    packages=setuptools.find_packages(where="autoquant"),
    python_requires=">=3.6",
)
