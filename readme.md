## Setup instructions
1. install dependencies
    ```bash
    pip install -r requirements.txt
    playwrite install

## set PYTHONPATH env var
```bash
    echo %PYTHONPATH% 
    set it to be 
    C:\Playwright\AviCherni\my-best-shopping;C:\Playwright\AviCherni\my-best-shopping\python_tool_shop;C:\Playwright\AviCherni\my-best-shopping\python_tool_shop\tests

## run tests by
```bash
    pytest -k "test_par"
