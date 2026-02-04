## Setup instructions
1. install dependencies
    ```bash
    pip install -r requirements.txt
    playwrite install

## Set PYTHONPATH env var
2.  set it to be 
    C:\Playwright\AviCherni\my-best-shopping;C:\Playwright\AviCherni\my-best-shopping\python_tool_shop;C:\Playwright\AviCherni\my-best-shopping\python_tool_shop\tests
    ```bash
    echo %PYTHONPATH% 
    echo $PYTHONPATH
  
## Run tests by
3.  pytest -k "test_par"
