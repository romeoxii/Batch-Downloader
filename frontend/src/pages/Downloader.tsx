import { useState, useEffect } from "react";
import axios from "axios";
import { Job } from "../types/download";
import { JobCard } from "../components/JobCard";
import { HugeiconsIcon } from "@hugeicons/react";
import { AlertCircleIcon, Download04Icon, ClockIcon, ArrowDown01Icon } from "@hugeicons/core-free-icons";

export function Downloader() {
  const [link, setUrl] = useState("");
  const [jobs, setJob] = useState<Job[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);

  const handleDownload = async (url: string) => {
    setError(null);
    try {
      const res = await axios.post<Job[]>("http://localhost:8000/download", {
        url,
      });
      setJob((currentJobs) => {
        let exists;
        let existsIndex = 0;

        for (let i = 0; i < currentJobs.length; i++) {
          if (
            currentJobs[i]["url"] === url &&
            currentJobs[i]["status"] === "cancelled"
          ) {
            exists = currentJobs[i];
            existsIndex = i;
            break;
          }
        }
        if (exists) {
          const newArr = [...currentJobs];
          newArr[existsIndex] = res.data[0];
          return newArr;
        }
        // Add every job returned — folder URLs return many jobs, single files return one
        return currentJobs.concat(res.data);
      });
      return true;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setError(error.response?.data?.detail || "Something went wrong");
      }
      return false;
    }
  };

  const handleSubmit = async () => {
    try {
      const res = await handleDownload(link);
      if (res) {
        setUrl("");
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const intervals: ReturnType<typeof setInterval>[] = [];
    if (jobs.length > 0) {
      jobs.forEach((job) => {
        if (job.status === "cancelled") {
          return;
        }

        if (job.status === "completed" || job.status === "failed") {
          return;
        }

        const id = job.id;
        const getJob = async () => {
          const res = await axios.get<Job>(
            `http://localhost:8000/downloads/${id}`,
          );
          setJob((currentJobs) =>
            currentJobs.map((job) => (job.id === res.data.id ? res.data : job)),
          );
        };

        const interval = setInterval(() => {
          getJob();
        }, 1000);
        intervals.push(interval);
      });
      return () => {
        intervals.forEach((int) => {
          clearInterval(int);
        });
      };
    }
  }, [jobs]);

  // Split jobs by status
  const activeJobs = jobs.filter((j) => j.status === "downloading");
  const pendingJobs = jobs.filter((j) => j.status === "pending");
  const historyJobs = jobs.filter(
    (j) => j.status === "completed" || j.status === "failed" || j.status === "cancelled" || j.status === "exists"
  );

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8 sm:px-6 sm:py-12">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight text-black lowercase sm:text-3xl">
          downloader
        </h1>
        <p className="mt-2 max-w-xl text-sm text-neutral-500">
          paste a direct file url or a folder url to queue one or many
          downloads.
        </p>
      </header>

      <div className="flex flex-col gap-3">
        <div className="flex w-full items-center gap-3 rounded-full border border-neutral-200 bg-white p-1.5 pl-5 transition focus-within:border-black">
          <input
            className="min-w-0 flex-1 bg-transparent text-sm text-black placeholder:text-neutral-400 focus:outline-none"
            placeholder="https://example.com/files/document.pdf"
            type="text"
            value={link}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button
            type="button"
            className="shrink-0 rounded-full bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-neutral-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-black/40 disabled:cursor-not-allowed disabled:bg-neutral-300"
            disabled={!link.trim()}
            onClick={handleSubmit}
          >
            download
          </button>
        </div>

        {error && (
          <p className="flex items-center gap-1.5 text-sm text-black">
            <HugeiconsIcon icon={AlertCircleIcon} size={16} strokeWidth={1.5} />
            {error}
          </p>
        )}
      </div>

      {/* Active Downloads */}
      {activeJobs.length > 0 && (
        <section className="space-y-3">
          <h2 className="flex items-center gap-2 text-xs font-medium text-neutral-500 uppercase tracking-wider">
            <HugeiconsIcon icon={ArrowDown01Icon} size={14} strokeWidth={2} />
            downloading ({activeJobs.length})
          </h2>
          <div className="flex flex-col gap-3">
            {activeJobs.map((job) => (
              <JobCard key={job.id} job={job} onRetry={handleDownload} />
            ))}
          </div>
        </section>
      )}

      {/* Pending Queue */}
      {pendingJobs.length > 0 && (
        <section className="space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="flex items-center gap-2 text-xs font-medium text-neutral-500 uppercase tracking-wider">
              <HugeiconsIcon icon={ClockIcon} size={14} strokeWidth={1.5} />
              queued ({pendingJobs.length})
            </h2>
          </div>
          <div className="max-h-48 overflow-y-auto space-y-2 border border-neutral-200 rounded-2xl p-3">
            {pendingJobs.map((job) => (
              <div
                key={job.id}
                className="flex items-center justify-between gap-3 rounded-xl border border-neutral-200 bg-white px-3 py-2.5 transition hover:border-neutral-300"
              >
                <div className="flex items-center gap-2 min-w-0 flex-1">
                  <HugeiconsIcon
                    icon={Download04Icon}
                    size={16}
                    strokeWidth={1.5}
                    className="text-neutral-400 shrink-0"
                  />
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-black truncate">
                      {job.name || "File"}
                    </p>
                    <p className="text-xs text-neutral-500 truncate">{job.url}</p>
                  </div>
                </div>
                <span className="shrink-0 text-xs text-neutral-500 uppercase">pending</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* History (Completed/Failed/Cancelled) */}
      {historyJobs.length > 0 && (
        <section className="space-y-2">
          <button
            type="button"
            className="flex items-center justify-between w-full text-xs font-medium text-neutral-500 uppercase tracking-wider hover:text-black"
            onClick={() => setShowHistory(!showHistory)}
          >
            <span className="flex items-center gap-2">
              <HugeiconsIcon
                icon={Download04Icon}
                size={14}
                strokeWidth={1.5}
              />
              history ({historyJobs.length})
            </span>
            <HugeiconsIcon
              icon={ArrowDown01Icon}
              size={14}
              strokeWidth={2}
              className={`transition-transform ${showHistory ? "rotate-180" : ""}`}
            />
          </button>
          {showHistory && (
            <div className="max-h-64 overflow-y-auto space-y-2 border border-neutral-200 rounded-2xl p-3">
              {historyJobs.map((job) => (
                <JobCard key={job.id} job={job} onRetry={handleDownload} />
              ))}
            </div>
          )}
        </section>
      )}

      {/* Empty State */}
      {jobs.length === 0 && (
        <div className="flex flex-col items-center gap-3 rounded-2xl border border-dashed border-neutral-200 bg-white px-6 py-14 text-center">
          <HugeiconsIcon
            icon={Download04Icon}
            size={24}
            strokeWidth={1.5}
            className="text-neutral-400"
          />
          <div>
            <p className="text-sm text-black">no downloads in the queue</p>
            <p className="mt-1 text-sm text-neutral-500">
              paste a url above to get started.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}