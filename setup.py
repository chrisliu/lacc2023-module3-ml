from setuptools import find_packages, setup

setup(
    name="lacc-module3",
    version="1.0",
    description="LACC Module 3",
    author="Dylan Kupsh and Chris Liu",
    author_email="dkupsh@cs.ucla.edu, c",
    package_dir={"lacc": "lacc"},
    install_requires=[
        "ipycanvas==0.11",
    ],  # external packages as dependencies
)
