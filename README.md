# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/molodsom/docx-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                  |    Stmts |     Miss |   Cover |   Missing |
|---------------------- | -------: | -------: | ------: | --------: |
| main.py               |       62 |        0 |    100% |           |
| models.py             |       19 |        0 |    100% |           |
| schemas.py            |       17 |        0 |    100% |           |
| settings.py           |       18 |        3 |     83% |     17-20 |
| tests/\_\_init\_\_.py |        0 |        0 |    100% |           |
| tests/test\_main.py   |       88 |        1 |     99% |       119 |
| utils.py              |       51 |        7 |     86% |47-48, 54-55, 59-61 |
|             **TOTAL** |  **255** |   **11** | **96%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/molodsom/docx-generator/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/molodsom/docx-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/molodsom/docx-generator/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/molodsom/docx-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fmolodsom%2Fdocx-generator%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/molodsom/docx-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.