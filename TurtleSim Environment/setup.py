from setuptools import find_packages, setup

package_name = 'turtle_room_env'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ROS 2 Student',
    maintainer_description='Multi-room environment for ROS 2',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'room_simulator = turtle_room_env.room_simulator_node:main',
        ],
    },
)