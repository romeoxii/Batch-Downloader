import requests
from urllib.parse import urlparse, urljoin


class FolderLister:
    def __init__(self, folder_url):
        self.folder_url = folder_url


    def return_origin(self, url):
        parsed_url = urlparse(url)
        
        return parsed_url.scheme + '://' + parsed_url.netloc

    def list_files(self):
        print("FolderLister started")
        response = requests.post(self.folder_url, timeout=30,json={"id": "","type": "folder","password": "","page_token": "","page_index": 0})
        print("FolderLister got response")
        origin = self.return_origin(self.folder_url)
        data = response.json()
        files = data["data"]["files"]
        files_to_download = []
        for file in files:
            file_link = origin + file["link"]
            files_to_download.append({"name": file["name"], "url": file_link})
        return files_to_download
