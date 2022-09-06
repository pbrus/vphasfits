import setuptools

setuptools.setup(
    name="vphasfits",
    version="1.0.0",
    author="Przemysław Bruś",
    description="A library allows to get data from the multi-extension VPHAS+ fits",
    packages=setuptools.find_packages(),
    install_requires=[
        "astropy",
        "numpy",
    ],
    scripts=[
        "scripts/vphas_srctbl.py",
        "scripts/vphas_pawprint.py",
        "scripts/vphas_cat.py",
    ],
    python_requires=">=3.6",
)
