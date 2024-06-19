from setuptools import setup, find_packages

VERSION = '0.2.0.0' 
DESCRIPTION = 'Python API wrapper for the galician public transport'
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
        install_requires=["requests>=2.25.1"],
        url="https://github.com/peprolinbot/bus.gal-api",
        project_urls={
            "Bug Tracker": "https://github.com/peprolinbot/bus.gal-api/issues",
            "Documentation": "https://busgal-api.readthedocs.io/en/latest/",
        },
        keywords=['bus', 'buses', 'transport', 'public transport', 'galicia', 'api'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ]
)
