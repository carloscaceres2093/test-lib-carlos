from setuptools import setup, find_packages

setup(
    name='yuno-utils',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/carloscaceres2093/test-lib-carlos.git',
    packages=find_packages(),
    install_requires=[
        'bcrypt==4.1.3',
        'cffi==1.16.0',
        'cryptography==42.0.8',
        'paramiko==3.4.0',
        'pycparser==2.22',
        'PyNaCl==1.5.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
