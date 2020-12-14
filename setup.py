import setuptools


setuptools.setup(
    name="fiberspot",
    version="0.0.1",
    author="Julian Bauer",
    author_email="julian.bauer@kit.edu",
    description="Spot fiber properties on 2D optical images",
    url="https://git.scc.kit.edu/julian_/fiberspot",
    # packages=setuptools.find_packages(),
    # packages=["paramid"],
    # package_dir={"paramid": "paramid"},
    # package_data={
    #     "paramid_data": package_files(
    #         directory=os.path.realpath(
    #             os.path.join(
    #                 os.path.dirname(os.path.realpath(__file__)), "paramid_data", "data"
    #             )
    #         )
    #     )
    # },
    # entry_points={
    #     "console_scripts": [
    #         "export_data_sets_to_file = paramid_data.scripts:export_data_sets_to_file",
    #     ]
    # },
    # include_package_data=True,
    install_requires=["numpy", "matplotlib", "pillow"],
    extras_require={":python_version>'3.5'": ["natsort", "matplotlib"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
