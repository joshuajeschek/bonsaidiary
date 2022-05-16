import setuptools

setuptools.setup(
    name='bonsaidiary',
    version='1.0',
    scripts=['./scripts/bonsaidiary'],
    author='Me',
    description='Access your plant based diary',
    packages=['bonsaidiary'],
    install_requires=[
        'setuptools'
        ],
    python_requires='>=3.10'
)
