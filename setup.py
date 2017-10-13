from setuptools import setup, find_packages

install_requires = []

with open("README.md") as f:
    long_description = f.read()

setup(name='anyloadump',
      version='0.1dev',
      description='dumper and loader for various file formats.',
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
      ],
      packages=find_packages(exclude=["tests"]),
      url="https://github.com/knknkn1162/anyloadump",
      author="knknkn1162",
      author_email="knknkn1162@gmail.com",
      include_package_data=True,
      zip_safe=False,
      test_suite="tests",
      license="MIT",
      keywords="",
      install_requires=install_requires,
      entry_points="""
""")
