# ANONY

ANONY is a collection of tools for working with Anonfiles, a file-hosting platform. This repository provides functionality to generate random codes, check the validity of codes, and scrape codes from the internet.

<img width="960" alt="Capture d'écran 2023-06-20 034307" src="https://github.com/Sla0ui/ANONY/assets/136838832/f2680608-6a24-42f9-9112-05282cd4bec7">


## Tools Included

### `generate_codes(num_codes)`

This function generates a specified number of random codes and saves them to a file named `generated_codes.txt`.

### `check_codes(file_path)`

This function checks the validity of codes stored in a file. It reads the codes from the specified file, checks their status on Anonfiles, and saves the valid codes to a file named `good_output.txt`.

### `scrape_links_with_domain(url, domain, num_pages)`

This function scrapes codes from the internet using the Wayback Machine archive of Anonfiles. It retrieves links from multiple pages and filters out the valid codes. The scraped codes are saved to a file named `anony_output.txt`.

## Dependencies

The following dependencies are required to run the code:

- `requests`: HTTP library for making requests to web servers.
- `colorama`: Library for printing colored text in the console.
- `lxml`: Library for processing HTML and XML.
- `selenium`: Python bindings for the Selenium WebDriver.
- `progress`: Library for creating progress bars.

Make sure to install these dependencies before running the code.

## Usage

To use the ANONY tools, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Run the Python script `anony.py`.
3. Choose one of the following options from the menu:
   - [1] Generate random codes
   - [2] Check codes
   - [3] Scrape codes from the internet
   - [4] Exit

Note: For the scraping option ([3]), the script uses the Wayback Machine archive of Anonfiles. You can modify the `url`, `domain`, and `num_pages` variables in the script to customize the scraping process.

Enjoy using ANONY and explore the capabilities of Anonfiles!

Author: Sla0ui
