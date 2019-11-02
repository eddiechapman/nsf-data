import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="nsf-data",
    author="Eddie Chapman",
    author_email="edward.chapman@marquette.edu",
    description="Download and parse NSF award data.",
    long_description=long_description,
    url="https://github.com/eddiechapman/nsf-data",
    packages=setuptools.find_packages(),
    scripts=['scripts/download.py', 'scripts/filter_awards.py'],
    requires=[
        'nltk',
        'beautifulsoup4',
        'lxml',
        'requests',
    ]
)

