import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BaseHangul",
    version="0.0.1",
    author="Heehoon Kim",
    author_email="heehoon@aces.snu.ac.kr",
    description="Binary-to-Hangul encoding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/csehydrogen/BaseHangul",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
