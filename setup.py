from setuptools import setup, find_packages

setup(
    name='email_classification',
    version='0.1.0',
    description='A package for email classification model building',
    author='Bob Marcotte',
    author_email='elastingbob@gmail.com',
    url='https://github.com/yourusername/email_classification',
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.24.0',
        'pandas>=1.2.0',
        'numpy>=1.19.0',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)