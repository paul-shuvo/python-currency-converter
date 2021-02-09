from setuptools import _install_setup_requires, setup

setup(
    name="Currency Converter Lite",
    version="0.0.1",
    description="A simple currency converter",
    py_modules=["currency_converter"],
    package_dir={"": "currency-converter"},
    url="",
    author="Shuvo Kumar Paul",
    author_email="shuvo.k.paul@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
    ],
    install_requies=["beautifulsoup4", "requests", "lxml", "html5lib", "future-fstrings"],
    extras_require={"dev": ["pytest", "coverage", "check-manifest", "twine", "tox"]},
)

# python setup.py bdist_wheel
# python setup.py sdist
# pip install -e .
# pip install -e .[dev]

# python setup.py bdist_wheel sdist
# ls sdist
# twine upload dist/*

# bump version
