from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent
README = (BASE_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name="cli-top-ai-features",
    version="0.1.0",
    description="LangChain-powered AI companion for the CLI-Top project",
    long_description=README,
    long_description_content_type="text/markdown",
    author="CLI-Top Contributors",
    packages=find_packages(exclude=("tests", "tests.*")),
    python_requires=">=3.9",
    install_requires=[
    "langchain==0.3.18",
    "langchain-core==0.3.75",
        "langchain-community==0.3.17",
        "langchain-google-genai==2.1.12",
        "google-cloud-aiplatform==1.76.0",
    "chromadb==0.5.23",
        "pypdf==5.1.0",
        "python-docx==1.1.2",
        "sentence-transformers==3.3.1",
        "sqlalchemy==2.0.36",
        "alembic==1.14.0",
        "pandas==2.2.3",
        "numpy==1.26.4",
    "scipy==1.14.1",
        "python-dotenv==1.0.1",
        "pydantic==2.10.5",
        "pydantic-settings==2.6.1",
    ],
    extras_require={
        "dev": [
            "pytest==8.3.4",
            "pytest-asyncio==0.24.0",
            "black==24.10.0",
            "flake8==7.1.1",
        ],
        "viz": [
            "matplotlib==3.9.2",
            "seaborn==0.13.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "cli-top-ai=ai_features.main:run",
        ]
    },
)
