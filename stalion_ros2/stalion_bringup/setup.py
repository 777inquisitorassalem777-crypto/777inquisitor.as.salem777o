from setuptools import setup
import os
from glob import glob

package_name = "stalion_bringup"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Stalion Research",
    maintainer_email="research@stalion.local",
    description="Minimal ROS2 bringup for Stalion ethical cognitive core",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "pneuma_node = stalion_bringup.pneuma_node:main",
            "ethics_veto_node = stalion_bringup.ethics_veto_node:main",
            "diff_drive_controller = stalion_bringup.diff_drive_controller:main",
        ],
    },
)

