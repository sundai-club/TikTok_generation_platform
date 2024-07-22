from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='tiktokgen',
    version='0.1.0',
    packages=find_packages(include=['tiktokgen', 'tiktokgen.*']),
    install_requires=requirements,
    include_package_data=True,
    description='A package for generating TikTok style videos',
    author='Sundai Club',
    author_email='sundaiclub@gmail.com',
    url='https://github.com/yourusername/tiktokgen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
