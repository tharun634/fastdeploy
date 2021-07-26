from setuptools import find_packages, setup

setup(
    name='fastdeploy',
    version='0.1.0',
    description='Quickly deploy your code onto vercel using FastAPI',
    author='Tharun K',
    license='MIT',
    packages=['fastdeploy','fastdeploy/cli'],
    install_requires=['click']
)
