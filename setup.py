from setuptools import setup, find_packages
import wordweaver

setup(
    name='wordweaver',
    python_requires='>=3.6',
    version=wordweaver.VERSION,
    long_description='WordWeaver',
    # packages=find_packages(),
    packages=['wordweaver',
              'wordweaver.buildtools',
              'wordweaver.static',
              'wordweaver.data',
              'wordweaver.data.api_data',
              'wordweaver.data.fomabins',
              'wordweaver.data.swagger',
              'wordweaver.fst',
              'wordweaver.fst.utils',
              'wordweaver.resources'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'flask_restful', 'flask_cors']
)