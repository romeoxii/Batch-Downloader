from downloader import Downloader
from concurrent.futures import ThreadPoolExecutor
from threading import Event


class BatchDownloader:
    def __init__(self):
        self.jobs = {}
        self.cancel_events = {}

    def download_job(self, job):

        def callback(progress):
            job["progress"] = progress

        cancel_event = Event()
        self.cancel_events[job["id"]] = cancel_event

        with Downloader() as downloader:
            # Only mark as downloading when actually starting the download
            job["status"] = "downloading"
            res = downloader.download(job["url"], callback, job["name"], cancel_event)
        status, code, reason, file_name, file_type = res

        if status == "exists":
            job["status"] = "exists"
            job["name"] = file_name
            job["filetype"] = file_type

        elif status == "completed":
            job["status"] = "completed"
            job["name"] = file_name
            job["filetype"] = file_type

        elif status == "cancelled":
            job["status"] = "cancelled"
            job["name"] = file_name
            job["filetype"] = file_type

        elif status == "failed":
            job["error"] = str(reason)
            job["status"] = "failed"
        else:
            job["error"] = str(reason)
            job["status"] = "failed"


    def receive_files(self):

        pending_jobs = [job for job in self.jobs.values() if job["status"] == "pending"]

        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.download_job, pending_jobs)


    def cancel_job(self, job_id):
        job = self.jobs.get(job_id)

        if job is None:
            return False

        self.cancel_events[job_id].set()
        return True