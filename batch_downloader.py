from downloader import Downloader
import uuid

class BatchDownloader:
    def __init__(self):
        self.jobs = {}
        self.downloader = Downloader()

    
    

    def receive_files(self):
        for id, job in self.jobs.items():
            if job["status"] != "pending":
                continue
            
            def callback(progress):
                job["progress"] = progress
            job["status"] = "downloading"
            res = self.downloader.download(job["url"], callback, job["name"])
            success, code, reason, file_name, file_type = res
            if success:
                job["status"] = "completed"
                job["name"] = file_name
                job["filetype"] = file_type
            else:
                job["error"] = str(reason)
                job["status"] = "failed"