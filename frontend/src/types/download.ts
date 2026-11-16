export interface Progress {
  speed: number;
  percentage: number;
  downloaded: number;
  total_size: number;
  eta_minutes: number;
  eta_seconds: number;
}

export type JobStatus =
  | "exists"
  | "pending"
  | "downloading"
  | "completed"
  | "failed"
  | "cancelled";

export interface Job {
  id: string;
  url: string;
  status: JobStatus;
  name: string | null;
  filetype: string | null;
  progress: Progress | null;
  error: string | null;
  cancel_event: Function;
}
