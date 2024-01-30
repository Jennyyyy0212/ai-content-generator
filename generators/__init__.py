# __init__.py
"""
my_package: A Python package for performing various tasks.
"""
PACKAGE_NAME = "generator"
VERSION = "1.0"

"""
Note: 
info_generator.py import content.py
auto_generator.py import both data_to_csv.py and info_generator.py

Relationship:
generator/
    __init__.py
    auto_generator.py /
        data_to_csv.py
        info_generator.py /
            content.py
"""
