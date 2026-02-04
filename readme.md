## Setup instructions
1. install dependencies
    ```bash
    pip install -r requirements.txt
    playwrite install

## Set PYTHONPATH env var
    set it to be 
    C:\Playwright\AviCherni\my-best-shopping;C:\Playwright\AviCherni\my-best-shopping\python_tool_shop;C:\Playwright\AviCherni\my-best-shopping\python_tool_shop\tests
    
    echo %PYTHONPATH% 
    echo $PYTHONPATH
  
## Run tests by
    pytest -k "test_par"
