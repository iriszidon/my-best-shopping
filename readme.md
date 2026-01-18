## Setup instructions
1. install dependencies
    ```aiignore
    pip install -r requirements.txt
   or just install one by one
    playwrite install
    pip install pytest
    pip install pytest-playwright
    pip install allure-pytest
    pip install pytest-xdist
   ```
2. Go to the test folder    
   ```aiignore
       cd <root folder>\my-best-shopping\pythonProject\python_tool_shop\tests
   ```
3. run tests by typing to the command line
   ```aiignore
    pytest -m ness_task
   ```
4. generate report by typing this line command line, hit the TAB key to select the directory
   ```aiignore
    allure serve allure-results 
   ```
    for example: 
    ```aiignore
    allure serve .\allure-results-20260117_215958\
    ```
5. To change the browser, go to pytest.ini and update: 
```aiignore
    BROWSER_NAME=firefox
 ```
to be:
```aiignore
    BROWSER_NAME=webkit 
    BROWSER_NAME=chrome
 ```
6. To enable Aerokube-Moon support, go to file pytest.ini
and uncomment lines:
```aiignore
    # BROWSER_NAME=auto
    # MOON_URL=http://moon.aerokube.local
```






   