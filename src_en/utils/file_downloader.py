# I import the library to perform HTTP checks
import requests


# The function for downloading the file according to the specified URL and save it to the disk.
def download_file(url, destination):

    # Send the GET request to the server with the specified URL and the transmission of the stream = true flag for the gradual download of the file
    response = requests.get(url, stream=True)

    # Check, whether the request is successful (the answer code 200 means success)
    if response.status_code == 200:
        # Open a file for recording in binary mode (WB)
        with open(destination, 'wb') as file:
            # Download the file in parts (1024 bytes) to avoid memory problems with large files
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)  # Record each part to the file
        print("Файл успешно загружен!")  # We report on successful loading
    else:
        # If the answer code is not 200, we display an error message
        print("Ошибка загрузки файла!")


# Example of using the function: download the file by URL
file_url = 'https://toscrape.com//path/to/file.txt'  # URL File for downloading
save_as = 'downloaded_file.txt'  # The name of the file under which it will be saved on the disk
download_file(file_url, save_as)  # Calling the file downloading function
