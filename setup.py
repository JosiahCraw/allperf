import setuptools

with open("README.md", 'r') as file_handler:
    long_description  = file_handler.read()

setuptools.setup(
    name="allperf",
    version="0.0.1",
    author="Josiah Craw",
    author_email="jos@joscraw.net",
    description="A Python CLI to perform and plot statistics for performance testing a git tracked C program",  
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JosiahCraw/allperf",
    packages=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        allperf=allperf.allperf:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)