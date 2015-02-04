import setuptools


setuptools.setup(
    name="salvitobot",
    version="0.1.0",
    url="https://github.com/aniversarioperu/salvitobot",

    author="AniversarioPeru",
    author_email="aniversarioperu1@gmail.com", maintainer="AniversarioPeru",
    maintainer_email="aniversarioperu1@gmail.com",

    description="avisa sismos y tsunamis",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',

        'Programming Language :: Python :: 3.4',
    ],
)
