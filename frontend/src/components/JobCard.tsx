import { Job } from "../types/download";
import { CompletedJob } from "./CompletedJob";
import { DownloadingJob } from "./DownloadingJob";
import { PendingJob } from "./PendingJob";
import { FailedJob } from "./FailedJob";

export function JobCard({ job }: { job: Job }) {
  // Pending state
  if (job.status === "pending") {
    return <PendingJob />;
  }
  //   Downloading
  if (job.status === "downloading") {
    return <DownloadingJob job={job} />;
  }
  // Completed state
  if (job.status === "completed") {
    return <CompletedJob job={job} />;
  }
  // Failed state
  if (job.status === "failed") {
    return <FailedJob job={job} />;
  }
}
