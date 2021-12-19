from setuptools import setup, find_packages

VERSION = '0.0.5.0' 
DESCRIPTION = 'Python API wrapper for bus.gal'
with open("README.rst", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
        name="busGal_api", 
        version=VERSION,
        author="Pedro Rey Anca",
        author_email="contact@peprolinbot.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["certifi>=2021.5.30", "chardet>=4.0.0", "idna>=2.10", "requests>=2.25.1", "urllib3>=1.26.5"],
        url="https://github.com/peprolinbot/bus.gal-api",
        project_urls={
            "Bug Tracker": "https://github.com/peprolinbot/bus.gal-api/issues",
            "Documentation": "https://busgal-api.readthedocs.io/en/latest/",
        },
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ]
)
