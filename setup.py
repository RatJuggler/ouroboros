from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ouroboros',
    version='0.0.8',
    description='My take on the snake game.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='pygame snake',
    author='John Chase',
    author_email='ratteal@gmail.com',
    python_requires='>=3.5',
    url='https://github.com/RatJuggler/ouroboros',
    project_urls={
        "Documentation": "https://github.com/RatJuggler/ouroboros",
        "Code": "https://github.com/RatJuggler/ouroboros",
        "Issue tracker": "https://github.com/RatJuggler/ouroboros/issues",
    },
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'ouroboros = ouroboros.__main__:main',
        ]
    },
    install_requires=[
        'pygame',
        'click'
    ],
    test_suite='tests',
    tests_require=[
        'coverage',
        'flake8',
        'testfixtures',
        'tox'
    ],
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
        'Topic:: Games / Entertainment:: Arcade'
    ]
)
