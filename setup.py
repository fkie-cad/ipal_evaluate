from setuptools import find_packages, setup

setup(
    name="ipal-evaluate",
    version="1.2.7",
    packages=find_packages(exclude="tests"),
    scripts=["ipal-evaluate", "ipal-plot-alerts", "ipal-plot-metrics", "ipal-tune"],
    install_requires=[
        "numpy",
        "scikit-learn",
        "opencv-python-headless",
        "eTaPR @ https://github.com/saurf4ng/eTaPR/blob/main/eTaPR-22.6.1-py3-none-any.whl?raw=true",
        "pandas",
        "matplotlib",
        "affiliation @ git+https://github.com/ahstat/affiliation-metrics-py.git",
        "ray[tune]",
    ],
    tests_require=["pre-commit", "black", "flake8", "pytest", "pytest-cov", "isort"],
    url="https://github.com/fkie-cad/ipal_evaluate",
    author="Konrad Wolsing",
    author_email="wolsing@comsys.rwth-aachen.de",
    long_description="Industrial systems are increasingly threatened by cyber attacks with potentially disastrous consequences. To counter such attacks, industrial intrusion detection systems strive to timely uncover even the most sophisticated breaches. Due to its criticality for society, this fast-growing field attracts researchers from diverse backgrounds, resulting in a huge momentum and diversity of contributions. Consequently, due to a lack of standard interfaces there exists not standard tools for evaluating IDSs. Based on IPAL - a common message format that decouples IIDSs from domain-specific communication protocols, we developed an  tool for scientific evaluation that combines different performance metrics into a single solution.",
    description="Industrial Intrusion Detection - a tool to evalute the performance of an IDS on IPAL.",
    keywords="IPAL IDS industrial CPS intrusion detection anomaly detection",
    classifiers=[
        "License :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
