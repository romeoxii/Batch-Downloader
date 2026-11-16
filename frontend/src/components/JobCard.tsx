import { Job } from "../types/download";
import { CompletedJob } from "./CompletedJob";
import { DownloadingJob } from "./DownloadingJob";
import { PendingJob } from "./PendingJob";
import { FailedJob } from "./FailedJob";
import { AlreadyExists } from "./AlreadyExistJob";
import { CancelledJob } from "./CancelledCard";

export function JobCard({
  job,
  onRetry,
}: {
  job: Job;
  onRetry: (url: string) => Promise<boolean>;
}) {
  // Already exist state
  if (job.status === "exists") {
    return <AlreadyExists job={job} />;
  }
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
  // Cancelled state
  if (job.status === "cancelled") {
    return <CancelledJob job={job} onRetry={onRetry} />;
  }
  // Failed state
  if (job.status === "failed") {
    return <FailedJob job={job} onRetry={onRetry} />;
  }
}
