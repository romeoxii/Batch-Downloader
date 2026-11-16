import { Job } from "../types/download";
import { cancelJob } from "../utilities/CancelJob";
import { HugeiconsIcon } from "@hugeicons/react";
import { Cancel01Icon, Loading03Icon } from "@hugeicons/core-free-icons";

export function DownloadingJob({ job }: { job: Job }) {
  return (
    <div className="relative flex flex-col gap-3 rounded-2xl border border-neutral-200 bg-white px-4 py-3">
      <div className="flex w-full items-center justify-between gap-3">
        <p className="truncate text-sm font-medium text-black">
          {job.name ? job.name : "file"}
        </p>
        <HugeiconsIcon
          icon={Loading03Icon}
          size={20}
          strokeWidth={1.5}
          className="animate-spin shrink-0 text-black"
        />
      </div>

      <div className="flex flex-col gap-1.5">
        <div className="flex items-center justify-between text-xs">
          <span className="text-neutral-500 lowercase">downloading</span>
          <span className="tabular-nums text-neutral-500">
            {job.progress?.percentage.toFixed(2) || "0.00"}%
          </span>
        </div>
        <div className="h-1 w-full overflow-hidden rounded-full bg-neutral-200">
          <div
            className="h-full rounded-full bg-black transition-[width] duration-300"
            style={{
              width: job.progress
                ? `${job.progress.percentage.toFixed(2)}%`
                : "0%",
            }}
          />
        </div>
      </div>

      <div className="flex w-full items-center justify-between gap-1 text-xs text-neutral-500">
        <p className="tabular-nums">
          {job.progress ? job.progress.speed.toFixed(2) : "0"} mb/s
        </p>
        <p className="tabular-nums">
          {job.progress ? job.progress.eta_minutes : "0"}:
          {job.progress
            ? job.progress.eta_seconds.toString().padStart(2, "0")
            : "00"}{" "}
          remaining
        </p>
      </div>

      <button
        type="button"
        aria-label="cancel download"
        className="absolute -right-2 -top-2 rounded-full border border-neutral-200 bg-white p-1.5 text-neutral-400 transition hover:border-black hover:text-black"
        onClick={() => cancelJob(job.id)}
      >
        <HugeiconsIcon icon={Cancel01Icon} size={14} strokeWidth={2} />
      </button>
    </div>
  );
}
