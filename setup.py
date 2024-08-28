from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_nav_to_pose'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools', 'nav2-simple-commander',],
    zip_safe=True,
    maintainer='CROHIN',
    maintainer_email='Guillaume.Crohin@ulb.be',
    description='Package for custom navigation to pose functionality',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
	    'control_husky = my_nav_to_pose.control_husky:main',
        'husky_nav_to_pose = my_nav_to_pose.husky_nav_to_pose:main',
        ],
    },
)
