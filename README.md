# IOTLab-Virtualization
 
Steps to setup the front-end
1. download the project and cd into smart-farm
2. in the terminal run 'npm install'
3. run 'ng serve' to see the front end locally

Steps to setup the backend
1. download the project, and cd into the backend
2. option: make an environment to seperate the dependencies
3. make sure a new verson of python and pip are available using 'python -v' and 'pip --version'
4. in the terminal run the following pip commands to get all of the dependencies
    1. pip install flask
    2. pip install Flask-Cors
    3. pip install requests
    4. pip install mysql.connector
5. These should cover the dependencies, if not, they are listed as imports at the top and should be simple to include
6. To run the server, in the terminal, run 'python serverSide.py'
7. Option: set up testing with Pytest
8. in the terminal run 'pip install -U pytest'
9. to run the tests in the terminal run 'pytest sample_test.py'

Steps to setup database

Steps to setup network
