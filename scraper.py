from selenium import webdriver
import zipfile
import os
import time

# Function to download a file given its URL
def download_file(link_element, directory):
    local_filename = os.path.join(directory, link_element.text + '.zip')
    print(link_element)
    link_element.click()
    return local_filename

# # Function to unzip a file
# def unzip_file(file_path, extract_directory):
#     with zipfile.ZipFile(file_path, 'r') as zip_ref:
#         zip_ref.extractall(extract_directory)


def get_data(download_directory)->None:
    base_url = 'https://www.nsf.gov/awardsearch/download'  
    
    ''' change the download directory to your desired directory '''
    
    # Create the specified directory if it doesn't exist
    os.makedirs(download_directory, exist_ok=True)

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,  # Disable prompt for download
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Loop through years from 2024 to 1958
    for year in range(2024, 1958, -1):
        url = f"{base_url}?DownloadFileName={year}&All=true"
        driver.get(url)
        print(f"Downloading {year}.zip...")

        try:
            download_link = driver.find_element_by_tag_name('a')
            print(download_link)
            download_file(download_link, download_directory)
            print("Downloaded successfully!")
        except Exception as e:
            print(f"Failed to download {year}.zip: {e}")

    # Close the WebDriver session
    driver.quit()

def unzip(download_directory, delete_zip_files=True)->None:
    # Create the specified directory if it doesn't exist
    os.makedirs(download_directory, exist_ok=True)
    for filename in os.listdir(download_directory):
        if filename.endswith('.zip'):
            file_path = os.path.join(download_directory, filename)
            print(f"Unzipping {filename}...")
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(download_directory)
                print("Unzipped successfully!")
                if delete_zip_files:
                    os.remove(file_path)  # Delete the original ZIP file
                    print(f"Deleted {filename}.")
            except Exception as e:
                print(f"Failed to unzip {filename}: {e}")


# Main function to download files from 2024 to 1959
def main()->None:
    # change the desired download directory 
    down_load_directory = "/home/notorious/Documents/VirtuosoResearch/generating-novel-contents/data"
    get_data(down_load_directory)
    # set delete_zip_files to False if you want to keep the zip files
    # unzip(down_load_directory, delete_zip_files=True)

    main()

