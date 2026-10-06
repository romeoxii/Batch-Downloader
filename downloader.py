import requests
from pathlib import Path
import time
from urllib.parse import urlparse
import hashlib


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

    return minutes, seconds, eta


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
        downloaded_mb_2 = to_mb(d_loaded)
        speed = calc_speed(downloaded_mb_2, e_time)
        return speed, downloaded_mb_2


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
        self.session = requests.Session()
        self.folder = Path("downloads")

    def __enter__(self):
        return self

    def get_temp_path(self, url):
        temp_path = hashlib.sha256(url.encode()).hexdigest()

        temp_path = temp_path + ".part"
        temp_path = self.folder / temp_path
        
        return temp_path


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

    @staticmethod
    def return_filename(cntnt_disposition):
        if cntnt_disposition is None:
            return None


        res = cntnt_disposition.split(";")
        for x in res:
            x.strip(' ')
            if x.startswith("filename"):
                x = x.split('=')
                filename = x[1].strip(' "')
                return filename
        return None

    # Prepare the HTTP response and download metadata
    def prepare_download(self, url, filename=None):
        temp_path = self.get_temp_path(url)

        downloaded = check_part(temp_path)
        headers = get_range(downloaded)
        response = self.session.get(
            url,
            stream=True,
            timeout=30,
            headers=headers
        )

        code, reason = check_response(response)

        print(f"CL: {response.headers.get("Content-Length")}")
        print(f"CR: {response.headers.get("Content-Range")}")
        print(f"CD: {response.headers.get("Content-Disposition")}")
        print(f"final url: {url}")

        if not code == 200 and not code == 206:
            print(f"Preparing the download failed.: {reason}")
            return False, code, reason, None, None, None, None, None
        
        print(f"Can Download?: {reason}")

        downloaded = self.handle_resume(downloaded, code)

        content_length = response.headers.get("Content-Length")
        content_range = response.headers.get("Content-Range")
        content_disposition = response.headers.get("Content-Disposition")
        filetype = response.headers.get("Content-Type")

        total_size = self.get_total_size(code, content_length, content_range)

        if filename is None:
            derived_filename = self.return_filename(content_disposition)
            if derived_filename is None:
                derived_filename = get_filename(url)
            filename = derived_filename

        final_path = self.folder / filename
        
        return True, temp_path, final_path, downloaded, response, total_size, filename, filetype


    @staticmethod
    def show_download_progress(downloaded, total_size, elapsed_time):
        if total_size:
            speed, percentage, bar, t_mb, d_mb = show_progress(downloaded, total_size, elapsed_time)
            
            minutes, seconds, eta = calc_eta(d_mb, t_mb, speed)
            
            # print(f"\rDownloading:[{bar}] {percentage:.1f}% {d_mb:.1f} MB / {t_mb:.1f} MB | {speed:.2f} MB/s | ETA: {minutes:02d}:{seconds:02d} ", end="")
            return {"speed": speed, "percentage": percentage, "downloaded":downloaded, "total_size": total_size, "eta_minutes":minutes, "eta_seconds":seconds}
        else:
            speed, downloaded_mb_2 = show_progress(downloaded, total_size, elapsed_time)
            # print(f"\rDownloading: {downloaded_mb_2:.1f} MB | {speed:.2f} MB/s", end="")
            return {"speed": speed, "downloaded":downloaded_mb_2}


    # Download the file in chunks to avoid loading it into memory
    def download_chunks(self, temp_path, final_path, downloaded, res, total_size, progress_callback):
        start_time = time.time()
        with open(temp_path, 'ab' if downloaded > 0 else 'wb') as file:
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

                    # raise Exception("Test download failure")
                    downloaded += len(chunk)
                    elapsed_time = time.time() - start_time
                    progress = self.show_download_progress(downloaded, total_size, elapsed_time)
                    progress_callback(progress)
                
        print(f"\nDownloading {final_path} complete.")
        temp_path.rename(final_path)
        return True


    # Coordinate the download process and handle errors
    def download(self, url, progress_callback, filename=None):
            
            try:
                result = self.prepare_download(url, filename)

                success, temp_path,final_path, downloaded, response, total_size, file_name, file_type = result
                if not success:
                    code = temp_path
                    reason = downloaded
                    return False, code, reason, None, None
    
                res = self.download_chunks(temp_path, final_path,  downloaded, response, total_size, progress_callback)
                return True, None, None, file_name, file_type
                
            
            except requests.RequestException as error:
                print(f"\nDownload failed: {error}")
                return False, None, error, None, None
            
            except KeyboardInterrupt:
                print(f"\nDownload interrupted")
                return False, None, "Download interrupted", None, None
        
            except Exception as error:
                print(f"\nUnexpected error: {error}")
                return False, None, error, None, None


    # Close the HTTP session
    def __exit__(self, exc_type, exc, tb):
        self.session.close()
