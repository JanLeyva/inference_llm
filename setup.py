from setuptools import setup, find_packages

setup(
    name='inference_llm',
    version='0.1',
    package_dir={"": "src"},
    packages=find_packages("src"),
    description='',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='Jan Leyva',
    author_email='janleyvamassague@gmail.com',
    url='https://https://github.com/JanLeyva/inference-llm',
    license='MIT',
    install_requires=[
        # List of dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
