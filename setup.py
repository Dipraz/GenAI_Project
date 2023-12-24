from setuptools import find_packages, setup

def get_requirements(file_path: str):
    '''
    Function to retrieve dependencies from requirements.txt
    '''
    with open(file_path) as f:
        requirements = [line.strip() for line in f if not line.startswith('-e')]
    return requirements

# Add your long description here, enclosed with triple quotes
long_description = '''
Life Data Lab is an application that combines AI image analysis and a chatbot functionality to provide analysis and engage in conversation.
'''

setup(
    name='Life-Data-Lab',
    version='0.0.1',
    author='Dipraj Howlader',
    author_email='dip07.raz@gmail.com',
    description='Life Data Lab - AI Image Analysis and Chatbot Application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dipraz/GenAI_Project/tree/main',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3.10',
        # Add more classifiers as needed
    ],
    license='MIT',
)
