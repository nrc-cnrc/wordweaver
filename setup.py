from setuptools import setup, find_packages
import wordweaver

setup(
    name='wordweaver',
    python_requires='>=3.6',
    version=wordweaver.VERSION,
    long_description='WordWeaver',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'flask_restful', 'flask_cors']
)
