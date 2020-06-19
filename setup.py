from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ouroboros',
    version='1.1.0',
    description='My take on the snake game.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='pygame snake',
    author='John Chase',
    author_email='ratteal@gmail.com',
    python_requires='>=3.6',
    url='https://github.com/RatJuggler/ouroboros',
    project_urls={
        "Documentation": "https://github.com/RatJuggler/ouroboros",
        "Code": "https://github.com/RatJuggler/ouroboros",
        "Issue tracker": "https://github.com/RatJuggler/ouroboros/issues",
    },
    packages=find_packages(exclude=['tests']),
    package_data={
        'ouroboros': [
            'ouroboros.png',
            'sprite_images.json',
            'rainyhearts.ttf',
            'died.wav',
            'eat.wav',
            'menu_music.mp3',
            'game_music.mp3'
        ],
    },
    entry_points={
        'console_scripts': [
            'ouroboros = ouroboros.__main__:main',
        ]
    },
    install_requires=[
        'pygame~=1.9.6',
        'click~=7.1.1'
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
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Topic:: Games / Entertainment:: Arcade'
    ]
)
