import { HugeiconsIcon } from "@hugeicons/react";
import { Loading03Icon } from "@hugeicons/core-free-icons";

export function PendingJob() {
  return (
    <div className="flex items-center gap-3 rounded-2xl border border-neutral-200 bg-white px-4 py-3">
      <HugeiconsIcon
        icon={Loading03Icon}
        size={18}
        strokeWidth={1.5}
        className="animate-spin text-black"
      />
      <p className="text-sm text-neutral-500 lowercase">waiting to start</p>
    </div>
  );
}
