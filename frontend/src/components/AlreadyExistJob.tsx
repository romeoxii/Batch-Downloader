import { Job } from "../types/download";
import { HugeiconsIcon } from "@hugeicons/react";
import { File02Icon } from "@hugeicons/core-free-icons";

export function AlreadyExists({ job }: { job: Job }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-2xl border border-neutral-200 bg-white px-4 py-3">
      <p className="truncate text-sm text-black">
        {job.name} <span className="text-neutral-500">already exists.</span>
      </p>
      <HugeiconsIcon
        icon={File02Icon}
        size={20}
        strokeWidth={1.5}
        className="shrink-0 text-black"
      />
    </div>
  );
}
