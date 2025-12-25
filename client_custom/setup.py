from setuptools import setup, find_packages

setup(
    name="client_custom",
    version="0.1.0",
    description="Custom CRM app for Frappe/ERPNext",
    packages=find_packages(),
    include_package_data=True,
)
