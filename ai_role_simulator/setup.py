from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="ai_role_simulator",
    version="0.2.1",
    description="AI来访者模拟器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "regex>=2023.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)