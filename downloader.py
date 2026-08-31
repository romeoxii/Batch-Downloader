import requests
from pathlib import Path
import time
from urllib.parse import urlparse



# construct progress bar
def progress_bar(ptage):
    bar_length = 20
    filled = int(ptage / 100 * bar_length)
    empty = bar_length - filled
    bar = "█" * filled + "░" * empty

    return bar

# convert file size to mb
def to_mb(s): return s / (1024 * 1024)

# format file size
def format_file_size(t_size, t_downloaded):
    t_mb = to_mb(t_size)
    d_mb = to_mb(t_downloaded)

    return t_mb, d_mb

# calculate speed
def calc_speed(d_mb, e_time):
    speed = d_mb / e_time

    return speed

# calculate ETA
def calc_eta(d_mb, t_mb, speed):

    remaining_mb = t_mb - d_mb

    eta = remaining_mb / speed

    minutes, seconds = divmod(int(eta), 60)

    return minutes, seconds


# get content length
def get_con_length(cl):
    if cl:
        t_size = int(cl)
    else:
        t_size = None

    return t_size

# progress and progress bar calculator
def show_progress(d_loaded, t_size, e_time):
    if t_size:
        percentage = d_loaded / t_size * 100
        bar = progress_bar(percentage)
        t_mb, d_mb = format_file_size(t_size, d_loaded)
        speed = calc_speed(d_mb, e_time)
        return speed, percentage, bar, t_mb, d_mb
    else:
        d_mb_2 = to_mb(d_loaded)
        speed = calc_speed(d_mb_2, e_time)
        return speed, d_mb_2

def check_response(res):
    try:
        res.raise_for_status()
        return True
    except requests.HTTPError:
        return False

# ceck if file path exists (for dowload resumption)   
def check_part(t_path):
    
    if t_path.exists():
        downloaded = t_path.stat().st_size
        return downloaded
    else:
        downloaded = 0
        return downloaded

# settingrange for content range
def get_range(d):
    if d > 0:
        return {"Range": f"bytes={d}-"}
    
    else:
        return None


def download(url, fp, sesh):
    # try getting response
    temp_path = fp.with_suffix(fp.suffix + '.part')

    
    
    try: 
        downloaded = check_part(temp_path)
        headers = get_range(downloaded)
        print(headers)
        response = sesh.get(url, stream=True, timeout=30, headers=headers)

        if not check_response(response):
            print("Download failed")
            return False

        total_size = 0
        
        content_length = response.headers.get("Content-Length")
        content_range = response.headers.get("Content-Range")
        

        if content_range:
            content_range = content_range.split('/')
            cr = content_range[1] 
            total_size = get_con_length(cr)
        else:
            total_size = get_con_length(content_length)
        
        
    
        start_time = time.time()
        with open(temp_path, 'ab' if downloaded > 0 else 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

                    downloaded += len(chunk)
                    elapsed_time = time.time() - start_time

                    if total_size:
                        speed, percentage, bar, t_mb, d_mb = show_progress(downloaded, total_size, elapsed_time)
                        
                        minutes, seconds = calc_eta(d_mb, t_mb, speed)
                
                        print(f"\rDownloading:[{bar}] {percentage:.1f}% {d_mb:.1f} MB / {t_mb:.1f} MB | {speed:.2f} MB/s | ETA: {minutes:02d}:{seconds:02d}", end="")
                        
                    else:
                        speed, d_mb_2 = show_progress(downloaded, total_size, elapsed_time)
                        print(f"\rDownloading: {d_mb_2:.1f} MB | {speed:.2f} MB/s", end="")
            

        print(f"\nDownloading {fp} complete.")
        temp_path.rename(fp)
        return True
    
    except requests.RequestException as error:
        print(f"\nDownload failed: {error}")
        print(f"Partial file saved at: {temp_path}")
        return False
    
    except KeyboardInterrupt as error:
        print(f"\nDownload interrupted: {error}")
        print(f"Partial file saved at: {temp_path}")
        return False

    except Exception as error:
        print(f"\nUnexpected error: {error}")
        return False

# check uf a url is valid
def is_valid_url(url):
    parsed_url = urlparse(url)

    return parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)

# extracting filename from url
def get_filename(url):
    parsed_url = urlparse(url)
    
    filename = Path(parsed_url.path).name

    if not filename:
        filename = "downloaded_file"

    return filename

# fetching urls from user inputs
def get_urls():
    urls = []
    while True:
        url = input("Enter a valid URL (type 'done' to start download process): ")
        if url == "":
            print("Please enter a URL")
            continue
        
        if url.lower() == "done":
            break

        
        if is_valid_url(url):
            if url in urls:
                print("URL already added")
                continue

            urls.append(url)
        else:
            print("Invalid URL")
    return urls


# Downloader class
class Downloader:
    # attributes initialization
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.folder = Path("downloads")
        self.successful = 0
        self.skipped = 0
        self.failed = 0

    def __enter__(self):
        return self

    # method for check uf a url is valid
    @staticmethod
    def is_valid_url(url):
        parsed_url = urlparse(url)
        
        return parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)

    # method fornfetching urls from user inputs
    def get_urls(self):
        while True:
            url = input("Enter a valid URL (type 'done' to start download process): ")
            if url == "":
                print("Please enter a URL")
                continue
            
            if url.lower() == "done":
                break
    
            
            if self.is_valid_url(url):
                if url in self.urls:
                    print("URL already added")
                    continue
    
                self.urls.append(url)
            else:
                print("Invalid URL")
        return self.urls

    # method to for extracting filename from url
    @staticmethod
    def get_filename(url):
        parsed_url = urlparse(url)
        filename = Path(parsed_url.path).name

        if not filename:
            filename = "downloaded_file"

        return filename

    # method to process downloads
    def process_downloads(self):
        # check if there are urls in urls array
            if not self.urls:
                # if empty
                print("No URLs were added!!")
                return
        

            for url in self.urls:
                filename = get_filename(url)
                file_path = self.folder / filename
    
                if file_path.exists():
                    print(f"{filename} exists")
                    self.skipped += 1
                    continue
                
                result = self.download(url, file_path)

                if result:
                    self.successful += 1
                else:
                    self.failed += 1
                    print('download failed')
        
            print("Download Summary:\n")
            print("----------------")
            print(f"Successful: {self.successful}")
            print(f"Skipped: {self.skipped}")
            print(f"Failed: {self.failed}")

    # method to prepare file for download
    def prepare_download(self, url, fp):
        temp_path = fp.with_suffix(fp.suffix + '.part')
            
        downloaded = check_part(temp_path)
        headers = get_range(downloaded)
        response = self.session.get(url, stream=True, timeout=30, headers=headers)

        total_size = 0
        
        content_length = response.headers.get("Content-Length")
        content_range = response.headers.get("Content-Range")
        

        if content_range:
            content_range = content_range.split('/')
            cr = content_range[1] 
            total_size = get_con_length(cr)
        else:
            total_size = get_con_length(content_length)

        if check_response(response):
            return temp_path, downloaded, response, total_size
        else:
            return None

    # method for downloading files in chunks instead of loading all into memory
    def download_chunks(self, temp_path, file_path, downloaded, res, total_size):
        # Time download started
        start_time = time.time()
        with open(temp_path, 'ab' if downloaded > 0 else 'wb') as file:
            # break file into chunks
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

                    downloaded += len(chunk)
                    elapsed_time = time.time() - start_time

                    if total_size:
                        speed, percentage, bar, t_mb, d_mb = show_progress(downloaded, total_size, elapsed_time)
                        
                        minutes, seconds = calc_eta(d_mb, t_mb, speed)
                
                        print(f"\rDownloading:[{bar}] {percentage:.1f}% {d_mb:.1f} MB / {t_mb:.1f} MB | {speed:.2f} MB/s | ETA: {minutes:02d}:{seconds:02d}", end="")
                        
                    else:
                        speed, d_mb_2 = show_progress(downloaded, total_size, elapsed_time)
                        print(f"\rDownloading: {d_mb_2:.1f} MB | {speed:.2f} MB/s", end="")

            
        print(f"\nDownloading {file_path} complete.")
        temp_path.rename(file_path)
        return True
        
    # method for downloading
    def download(self, url, file_path):
        # store results
        result = self.prepare_download(url, file_path)

        if result is None:
            return False
        else:
            temp_path, downloaded, response, total_size = result
                
        try:
            res =  self.download_chunks(temp_path, file_path, downloaded, response, total_size)
            return res
            
        
        except requests.RequestException as error:
            print(f"\nDownload failed: {error}")
            print(f"Partial file saved at: {temp_path}")
            return False
        
        except KeyboardInterrupt:
            print(f"\nDownload interrupted")
            print(f"Partial file saved at: {temp_path}")
            return False
    
        except Exception as error:
            print(f"\nUnexpected error: {error}")
            return False

    def __exit__(self, exc_type, exc, tb):
        self.session.close()

def main():

    with Downloader() as downloader:
        # get urls
        downloader.get_urls()

        # process downloads
        downloader.process_downloads()


if __name__=="__main__":
    main()