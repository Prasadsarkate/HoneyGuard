from setuptools import setup, find_packages

setup(
    name="HoneyGuard",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "watchdog",
        "colorama",
        "pyyaml",
        "flask",
        "requests",
        "cryptography",
        "geoip2",
        "schedule",
    ],
    entry_points={"console_scripts": ["honeyguard=src.cli.cli:main"]},
    include_package_data=True,
    description="Deception-based HoneyGuard detection tool with alerts, dashboard, and plugins.",
    author="",
    license="MIT",
)

