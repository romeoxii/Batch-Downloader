import requests
from pathlib import Path
import time
from urllib.parse import urlparse


# Build a progress bar
def progress_bar(percentage):
    bar_length = 20
    filled = int(percentage / 100 * bar_length)
    empty = bar_length - filled
    bar = "█" * filled + "░" * empty

    return bar


# Convert bytes to megabytes
def to_mb(s): return s / (1024 * 1024)


# Convert total and downloaded file sizes to megabytes
def format_file_size(t_size, t_downloaded):
    total_mb = to_mb(t_size)
    downloaded_mb = to_mb(t_downloaded)

    return total_mb, downloaded_mb


# Calculate download speed in MB/s
def calc_speed(d_mb, e_time):
    if e_time > 0:
        speed = d_mb / e_time
        return speed
    else:
        speed = 0
        return speed


# Calculate estimated time remaining
def calc_eta(d_mb, t_mb, speed):

    remaining_mb = t_mb - d_mb

    if speed > 0:
        eta = remaining_mb / speed
    else:
        eta = 0

    minutes, seconds = divmod(int(eta), 60)

    return minutes, seconds


# Convert a Content-Length value to an integer
def get_con_length(cl):
    if cl:
        t_size = int(cl)
    else:
        t_size = None

    return t_size


# Calculate download progress and statistics
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


# Validate a URL
def is_valid_url(url):
    parsed_url = urlparse(url)
    
    return parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)
    

# Extract a filename from a URL
def get_filename(url):
    parsed_url = urlparse(url)
    filename = Path(parsed_url.path).name

    if not filename:
        filename = "downloaded_file"

    return filename


# Get the HTTP status code and reason
def check_response(res):
    code, reason = res.status_code, res.reason
    return code, reason


# Check for an existing partial download
def check_part(temp_path):
    
    if temp_path.exists():
        downloaded = temp_path.stat().st_size
        return downloaded
    else:
        downloaded = 0
        return downloaded


# Build a Range header for resuming a download
def get_range(d):
    if d > 0:
        return {"Range": f"bytes={d}-"}
    
    else:
        return None


class Downloader:

    # Initialize downloader state and HTTP session
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.folder = Path("downloads")
        self.successful = 0
        self.skipped = 0
        self.failed = 0

    def __enter__(self):
        return self


    # Check whether the destination file already exists
    def check_existing_file(self, file_path):
        if file_path.exists():
            print(f"{file_path.name} exists")
            self.skipped += 1
            return True
        return False


    # Process all queued downloads
    def process_downloads(self):
        if not self.urls:
            print("No URLs were added!!")
            return

        for url in self.urls:
            filename = get_filename(url)
            file_path = self.folder / filename

            if self.check_existing_file(file_path):
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


    # Determine whether a partial download can be resumed
    def handle_resume(self, downloaded, status_code):
        if downloaded > 0:
            if status_code == 200:
                downloaded = 0
        return downloaded


    @staticmethod
    def get_total_size(status_code, content_length, content_range):
        total_size = None
        if status_code == 206:
            if content_range is not None:
                parts = content_range.split('/')
                if len(parts) == 2:
                    cr = parts[1]
                    total_size = get_con_length(cr)
                else:
                    total_size = None     
            else:
                total_size = None
        elif status_code == 200:
            total_size = get_con_length(content_length)
        return total_size


    # Prepare the HTTP response and download metadata
    def prepare_download(self, url, file_path):
        temp_path = file_path.with_suffix(file_path.suffix + '.part')

        downloaded = check_part(temp_path)
        headers = get_range(downloaded)
        response = self.session.get(
            url,
            stream=True,
            timeout=30,
            headers=headers
        )

        code, reason = check_response(response)

        if not code == 200 and not code == 206:
            print(f"Preparing the download failed.: {reason}")
            return None
        
        print(f"Can Download?: {reason}")

        downloaded = self.handle_resume(downloaded, code)

        content_length = response.headers.get("Content-Length")
        content_range = response.headers.get("Content-Range")

        total_size = self.get_total_size(code, content_length, content_range)
        
        return temp_path, downloaded, response, total_size


    @staticmethod
    def show_download_progress(downloaded, total_size, elapsed_time):
        if total_size:
            speed, percentage, bar, t_mb, d_mb = show_progress(downloaded, total_size, elapsed_time)
            
            minutes, seconds = calc_eta(d_mb, t_mb, speed)
            
            print(f"\rDownloading:[{bar}] {percentage:.1f}% {d_mb:.1f} MB / {t_mb:.1f} MB | {speed:.2f} MB/s | ETA: {minutes:02d}:{seconds:02d} ", end="")
            
        else:
            speed, d_mb_2 = show_progress(downloaded, total_size, elapsed_time)
            print(f"\rDownloading: {d_mb_2:.1f} MB | {speed:.2f} MB/s", end="")


    # Download the file in chunks to avoid loading it into memory
    def download_chunks(self, temp_path, file_path, downloaded, res, total_size):
        start_time = time.time()
        with open(temp_path, 'ab' if downloaded > 0 else 'wb') as file:
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

                    downloaded += len(chunk)
                    elapsed_time = time.time() - start_time
                    self.show_download_progress(downloaded, total_size, elapsed_time)
                        
        print(f"\nDownloading {file_path} complete.")
        temp_path.rename(file_path)
        return True


    # Coordinate the download process and handle errors
    def download(self, url, file_path):
                    
            try:
                result = self.prepare_download(url, file_path)
    
                if result is None:
                    return False
    
                temp_path, downloaded, response, total_size = result
                res = self.download_chunks(temp_path, file_path, downloaded, response, total_size)
                return res
                
            
            except requests.RequestException as error:
                print(f"\nDownload failed: {error}")
                print(f"Partial file saved at: {temp_path}")
                return False
            
            except KeyboardInterrupt:
                print(f"\nDownload interrupted")
                if temp_path:
                    print(f"Partial file saved at: {temp_path}")
                return False
        
            except Exception as error:
                print(f"\nUnexpected error: {error}")
                return False


    # Close the HTTP session
    def __exit__(self, exc_type, exc, tb):
        self.session.close()


def main():

    with Downloader() as downloader:
        downloader.get_urls()
        downloader.process_downloads()


if __name__=="__main__":
    main()