from setuptools import setup, find_packages

setup(
    name="aclimate_v3_orm",
    version='v0.0.4',
    author="santiago123x",
    author_email="s.calderon@cgiar.com",
    description="ORM para la base de datos de AClimate y sus metodos",
    url="https://github.com/CIAT-DAPA/aclimate_v3_orm",
    download_url="https://github.com/CIAT-DAPA/aclimate_v3_orm",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "sqlalchemy==2.0.40",
        "psycopg2==2.9.10",
        "python-dotenv==1.1.0",
        "typing_extensions==4.13.2",
        "pydantic==2.11.4"
    ]
)