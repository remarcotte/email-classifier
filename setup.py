from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='email_classification',
    version='0.1.0',
    author='Bob Marcotte',
    author_email='elastingbob@gmail.com',
    description="A model to classify emails into categories like work, personal, ad, finance, spam.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remarcotte/email-classifier",
    packages=find_packages(),
    install_requires=[
        "json",
        "joblib",
        "pandas",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
