# Resume Generator and PDF Extractor

This Python script(s) allows you to generate multiple resume combinations using a
template and a list of project descriptions. Additionally, it provides
functionality to convert these generated resume html files into PDF files.

## Usage

### Resume Generation

```python
from itertools import combinations
import os

# ... (Your code for the `generate_combos` function, header, string_list, and footer)

# Example usage
generate_combos(header, string_list, footer)
```

This function (`generate_combos`) takes a header, a list of project
descriptions (`string_list`), and a footer to create multiple HTML resumes with
different combinations of projects. The resumes are then saved in both HTML and
text formats.

### PDF Extraction

```python
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# ... (Your code for the `get_pdf_from_web` function)

# run python -m http.server in combos folder
url_to_scrape = "http://127.0.0.1:8000/resume_1.html"
geckodriver_path = "../geckodriver"

get_pdf_from_web(url_to_scrape, geckodriver_path)
```

This function (`get_pdf_from_web`) uses Selenium with a headless Firefox
browser to navigate to a given URL (resume in HTML format) and save it as a
PDF. Adjust the `url_to_scrape` variable with the URL of the HTML resume you
want to convert.

## Requirements

- Python 3.x
- Selenium

```bash
pip install -r requirements.txt
```

## Configuration

- Ensure the `geckodriver` executable is available in the specified path
  (`geckodriver_path`) or update the path accordingly.

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details.

## Acknowledgments

- [Selenium](https://www.selenium.dev/)
