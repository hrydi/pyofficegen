from setuptools import setup, find_packages
setup(
  author="hrydi",
  author_email="hari dot nube at gmail dot com",
  description="Office Generator Helper",
  name="PyOfficeGen",
  version="1.0.0",
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    "typer[all]",
    "xlsxwriter",
    "requests"
  ]
)