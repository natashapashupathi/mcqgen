from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Natasha Pashupathi',
    author_email='natasha.pashu@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)