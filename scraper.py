# Import libraries
from bs4 import BeautifulSoup
import requests
import re
import os
#%%

# Function for getting the text data from a website url
def get_data(url):
 r = requests.get(url)
 return r.text

# get links of the website
def get_links(website_link):
    html_data = get_data(website_link)
    soup = BeautifulSoup(html_data, "html.parser")
    list_links = []
    for link in soup.find_all("a", href=True):
        list_links.append(link["href"])
    return list_links

# Add base path to all links
def add_base_path(website_link, list_links):
    list_links_with_base_path = []

    for link in list_links:

        if link.startswith('/docs'):
            continue

        elif link.startswith('/'):
            link_with_base_path = website_link + link
            list_links_with_base_path.append(link_with_base_path)

  # if link.startswith('https://') dont add base path
        elif link.startswith('http://') or link.startswith('https://'):
            list_links_with_base_path.append(link)

        elif link.startswith('#'):
            link_with_base_path = website_link + '/' + link
            list_links_with_base_path.append(link_with_base_path)

    return list_links_with_base_path

def save_content(link_list):
    for i, link in enumerate(link_list):
        html_data = get_data(link)
        soup = BeautifulSoup(html_data, "html.parser")
        text = soup.get_text()

        # Remove the first 835 lines
        lines = text.splitlines()
        cleaned_text = "\n".join(lines[835:])

        # Get the first 3 words in the cleaned text
        words = cleaned_text.split()[:3]
        file_name_prefix = "_".join(words)

        # Replace special characters and spaces with an underscore
        file_name_prefix = re.sub(r"[^a-zA-Z0-9]+", "_", file_name_prefix)

        # Get the current working directory
        current_dir = os.getcwd()

        # Move up one level to the parent directory
        parent_dir = os.path.dirname(current_dir)
        assert False

        # Set the path to the data folder
        data_folder = os.path.join(parent_dir, "data/langchain_doc")

        # Create the data folder if it doesn't exist
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Set the path to the output file
        output_file = os.path.join(data_folder, f"{i}_{file_name_prefix}.txt")

        # Save the cleaned content to the output file
        with open(output_file, "w") as f:
            f.write(cleaned_text)

homepage = 'https://python.langchain.com/docs/get_started/introduction'
sub_links = get_links(f'{homepage}/index.html')
link_list = add_base_path(homepage, sub_links)
print(sub_links)
print(link_list)
assert False
# save_content(link_list)
