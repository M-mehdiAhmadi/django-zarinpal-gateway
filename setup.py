from setuptools import setup, find_packages

setup(
    name="django-zarinpal-gateway",
    version="0.1.0",
    description="A reusable Django app for ZarinPal payment integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="git@github.com:M-mehdiAhmadi/django-zarinpal-gateway",
    author="Mehdi Ahmadi",
    author_email="ahmadi.mehd2@gmail.com",
    install_requires=[
        "Django>=5.0",
        "requests>=2.32"
    ],
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
