import os

from setuptools import find_packages, setup

# Read README.md content as long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get version from environment variable or use default value
# version = os.getenv("RELEASE_VERSION", "0.3.2")

setup(
    name="wuying_agentbay_sdk",
    version='0.5.0',
    author="Alibaba Cloud",
    author_email="wuying@alibaba-inc.com",
    description="Python SDK for AgentBay service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliyun/wuying-agentbay-sdk",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "urllib3>=1.26.0",
        "typing-extensions>=4.0.0",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=0.900",
            "flake8>=3.9.0",
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/aliyun/wuying-agentbay-sdk/issues",
        "Documentation": "https://github.com/aliyun/wuying-agentbay-sdk/blob/main/README.md",
        "Source Code": "https://github.com/aliyun/wuying-agentbay-sdk",
    },
    keywords=[
        "alibaba",
        "aliyun",
        "wuying",
        "agentbay",
        "sdk",
        "cloud",
        "api",
    ],
)
