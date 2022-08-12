import setuptools

setuptools.setup(
    name="contacts",
    version="1.0",
    license="MIT",
    description="Phone contacts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['myLogger'],
    python_requires='>=3.6',
)