import "./App.css";
import { useState, useEffect } from "react";
import axios from "axios";
import { Job } from "./types/download";
import { JobCard } from "./components/JobCard";

function App() {
  const [url, setUrl] = useState("");
  const [jobs, setJob] = useState<Job[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async () => {
    setError(null);
    try {
      const res = await axios.post<Job[]>("http://localhost:8000/download", {
        url,
      });
      setJob((currentJobs) => currentJobs.concat(res.data));
      setUrl("");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setError(error.response?.data?.detail || "Something went wrong");
      }
    }
  };

  useEffect(() => {
    const intervals: ReturnType<typeof setInterval>[] = [];
    console.log("effect ran", jobs);
    if (jobs.length > 0) {
      jobs.forEach((job) => {
        const id = job.id;
        const getJob = async () => {
          const res = await axios.get<Job>(
            `http://localhost:8000/downloads/${id}`,
          );
          console.log(res.data);
          setJob((currentJobs) =>
            currentJobs.map((job) => (job.id === res.data.id ? res.data : job)),
          );
        };

        if (job.status === "completed" || job.status === "failed") {
          console.log(`Job ${job.status}`);
          return;
        }

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

  return (
    <>
      <section id="center">
        <input
          className="p-1.5 rounded-md w-64 mx-auto ring-1 ring-neutral-700 text-sm"
          placeholder="enter a url.."
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button
          className="bg-neutral-200 ring-1 ring-neutral-300 p-2 rounded-md"
          onClick={() => handleDownload()}
        >
          Submit
        </button>
        {error && <p>{error}</p>}
        {jobs.length > 0 ? (
          jobs.map((job) => <JobCard key={job.id} job={job} />)
        ) : (
          <p>No job</p>
        )}
      </section>
    </>
  );
}

export default App;
