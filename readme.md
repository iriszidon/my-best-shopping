## Setup instructions
1. install dependencies
    ```bash
    pip install -r requirements.txt
   or just install one by one
    playwrite install
    pip install pytest
    pip install pytest-playwright
    pip install allure-pytest
    pip install pytest-xdist
   ```
2. Go to the test folder    
   ```bash
       cd <root folder>\my-best-shopping\pythonProject\python_tool_shop\tests
   ```
3. run tests by typing to the command line
   ```bash
    pytest -m ness_task
   ```
4. generate report by typing this line command line, hit the TAB key to select the directory
   ```bash
    allure serve allure-results 
   ```
    for example: 
    ```bash
    allure serve .\allure-results-20260117_215958\
    ```
5. To change the browser, go to pytest.ini and update: 
```bash
    BROWSER_NAME=firefox
 ```
to be:
```bash
    BROWSER_NAME=webkit 
    BROWSER_NAME=chrome
 ```






   