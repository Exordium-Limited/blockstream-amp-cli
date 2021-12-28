from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="blocktstream-amp-cli",  # Required
    version="0.0.1",
    description="The CLI for the Blockstream AMP platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Exordium-Limited/blockstream-amp-cli",
    author="Exordium Limited",
    author_email="tservices@exordium.co",
    keywords="blockstream amp, security token, STO",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=["requests"],
    package_data={"blocktstream-amp-cli": []},
    entry_points={
        "console_scripts": [
            "amp=amp:main",
        ],
    },
)
