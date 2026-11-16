import { Job } from "../types/download";
import { HugeiconsIcon } from "@hugeicons/react";
import { CancelCircleIcon } from "@hugeicons/core-free-icons";

export function CancelledJob({
  job,
  onRetry,
}: {
  job: Job;
  onRetry: (url: string) => Promise<boolean>;
}) {
  return (
    <div className="flex flex-col items-center gap-1.5 rounded-2xl border border-neutral-200 bg-white p-4 text-center">
      <HugeiconsIcon
        icon={CancelCircleIcon}
        size={24}
        strokeWidth={1.5}
        className="text-neutral-400"
      />
      <p className="text-sm text-black lowercase">download cancelled</p>
      <p className="text-xs text-neutral-500">{job.name} was cancelled.</p>
      <button
        type="button"
        className="mt-1 rounded-full border border-neutral-200 px-4 py-1.5 text-xs font-medium text-black transition hover:bg-neutral-50"
        onClick={() => onRetry(job.url)}
      >
        retry
      </button>
    </div>
  );
}
