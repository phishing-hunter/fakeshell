from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fakeshell",
    version="1.0.1",
    author="tatsui",
    install_requires=requirements,
    include_package_data=True,
    author_email="2360691+tatsu-i@users.noreply.github.com",
    description="A virtual shell implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phishing-hunter/fakeshell",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
