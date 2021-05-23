from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Python API wrapper for bus.gal'
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
        name="busGal_api", 
        version=VERSION,
        author="Pedro Rey Anca",
        author_email="contact@peprolinbot.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ]
)
