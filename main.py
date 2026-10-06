from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from downloader import Downloader
from batch_downloader import BatchDownloader
from folder_lister import FolderLister
import uuid
from url_checker import is_file_or_folder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DownloadRequest(BaseModel):
    url: str


batch = BatchDownloader()

@app.post("/download")
def download_file(request: DownloadRequest, background_task: BackgroundTasks):

	source_type = is_file_or_folder(request.url)
	downloads = []

	if source_type == "file":
		job_id = 'job' + '-' + str(uuid.uuid4())
		batch.jobs[job_id] = {"id": job_id, "url": request.url, "status": "pending", "name": None, "filetype": None, "progress": None, "error": None}
		downloads.append(batch.jobs[job_id])
		background_task.add_task(batch.receive_files)
		return downloads
	elif source_type == "folder":
		folder_lister = FolderLister(request.url)
		try:
			files_to_download = folder_lister.list_files()
			
		except KeyError:
			return downloads
	
		if files_to_download:
			for file in files_to_download:
				job_id = 'job' + '-' + str(uuid.uuid4())
				batch.jobs[job_id] = {"id": job_id, "url": file["url"], "status": "pending", "name": file["name"], "filetype": None, "progress": None, "error": None}
				downloads.append(batch.jobs[job_id])
			background_task.add_task(batch.receive_files)
			return downloads
		else:
			return None
	else:
		
		raise HTTPException(status_code=404, detail="Url Invalid")
	
			

@app.get('/downloads/{job_id}')
def get_job(job_id):
	if job_id not in batch.jobs:
		raise HTTPException(status_code=404, detail="Item not found")

	job_found = batch.jobs[job_id]
	return job_found
