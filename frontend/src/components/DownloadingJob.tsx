import { Job } from "../types/download";

export function DownloadingJob({ job }: { job: Job }) {
  return (
    <div className="max-w-md mx-auto flex flex-col justify-between bg-yellow-800/10 ring-1 ring-yellow-800/90 rounded-md px-2 py-1 space-y-3">
      <div className="w-full flex items-center justify-between gap-2">
        <p className="text-yellow-900 text-sm">
          {job.name ? job.name : "File"}
        </p>
        <span className="text-2xl text-yellow-800">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="1em"
            height="1em"
            viewBox="0 0 24 24"
          >
            <path d="M0 0h24v24H0z" fill="none" />
            <g
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
            >
              <path
                stroke-dasharray="32"
                d="M12 21c-4.97 0 -9 -4.03 -9 -9c0 -4.97 4.03 -9 9 -9"
              >
                <animate
                  fill="freeze"
                  attributeName="stroke-dashoffset"
                  dur="0.6s"
                  values="32;0"
                />
              </path>
              <path
                stroke-dasharray="2 4"
                stroke-dashoffset="6"
                d="M12 3c4.97 0 9 4.03 9 9c0 4.97 -4.03 9 -9 9"
                opacity="0"
              >
                <set
                  fill="freeze"
                  attributeName="opacity"
                  begin="0.45s"
                  to="1"
                />
                <animateTransform
                  fill="freeze"
                  attributeName="transform"
                  begin="0.45s"
                  dur="0.6s"
                  type="rotate"
                  values="-180 12 12;0 12 12"
                />
                <animate
                  attributeName="stroke-dashoffset"
                  begin="0.85s"
                  dur="0.6s"
                  repeatCount="indefinite"
                  to="0"
                />
              </path>
              <path stroke-dasharray="10" stroke-dashoffset="10" d="M12 8v7.5">
                <animate
                  fill="freeze"
                  attributeName="stroke-dashoffset"
                  begin="0.85s"
                  dur="0.2s"
                  to="0"
                />
              </path>
              <path
                stroke-dasharray="8"
                stroke-dashoffset="8"
                d="M12 15.5l3.5 -3.5M12 15.5l-3.5 -3.5"
              >
                <animate
                  fill="freeze"
                  attributeName="stroke-dashoffset"
                  begin="1.05s"
                  dur="0.2s"
                  to="0"
                />
              </path>
            </g>
          </svg>
        </span>
      </div>
      <div className="flex flex-col items-start">
        <p className="text-yellow-800 text-xs">Downloading</p>
        <div className="w-full flex items-center gap-3">
          <div className="h-1 flex-1 rounded-xl bg-yellow-800/30">
            <div
              className="h-1 rounded-xl bg-yellow-600"
              style={{
                width: job.progress
                  ? `${job.progress.percentage.toFixed(2)}%`
                  : "0%",
              }}
            />
          </div>

          <p className="text-[10px] text-yellow-700">
            {job.progress?.percentage.toFixed(2) || "0.00"}%
          </p>
        </div>
      </div>
      <div className="w-full flex items-center justify-between gap-1 ">
        <p className="text-yellow-700 text-xs">
          {job.progress ? job.progress.speed.toFixed(2) : `0`} MB/s
        </p>
        <div className="flex items-center gap-2">
          <div className="flex items-center text-yellow-700 text-xs">
            <p>{job.progress ? job.progress.eta_minutes : `0`}</p>:
            <p>
              {job.progress
                ? job.progress.eta_seconds.toString().padStart(2, "0")
                : `00`}{" "}
              remaining
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
