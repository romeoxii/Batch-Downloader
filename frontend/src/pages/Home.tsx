import { Link } from "react-router-dom";
import { HugeiconsIcon } from "@hugeicons/react";
import {
  ArrowDown01Icon,
  Download04Icon,
  FlashIcon,
  Folder01Icon,
  Activity03Icon,
} from "@hugeicons/core-free-icons";

const features = [
  {
    title: "streaming downloads",
    description:
      "files are written chunk by chunk, so even large downloads stay light on memory.",
    icon: FlashIcon,
  },
  {
    title: "batch folder support",
    description:
      "paste a folder url and every file it contains is queued automatically.",
    icon: Folder01Icon,
  },
  {
    title: "live progress",
    description: "speed, percentage, and time remaining update in real time.",
    icon: Activity03Icon,
  },
  {
    title: "retry & cancel",
    description:
      "cancel a running download or retry a failed one without starting over.",
    icon: Download04Icon,
  },
];

export function Home() {
  return (
    <>
      <section className="mx-auto flex w-full max-w-5xl flex-col items-center px-4 pb-16 pt-24 text-center sm:px-6 sm:pt-32">
        <h1 className="text-5xl font-semibold tracking-tight text-black sm:text-6xl">
          fetchflow
        </h1>

        <p className="mt-4 max-w-md text-base text-neutral-500 sm:text-lg">
          a batch downloader that just downloads.
        </p>

        <div className="mt-8 flex items-center gap-5">
          <Link
            to="/downloader"
            className="inline-flex items-center gap-2 rounded-full bg-black px-6 py-3 text-sm font-medium text-white transition hover:bg-neutral-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-black/40"
          >
            start downloading
            <HugeiconsIcon icon={ArrowDown01Icon} size={16} strokeWidth={2} />
          </Link>
          <a
            href="#features"
            className="text-sm text-neutral-500 underline-offset-4 transition hover:text-black hover:underline"
          >
            see features
          </a>
        </div>

        {/* Preview card */}
        <div className="mt-16 w-full max-w-md rounded-2xl border border-neutral-200 bg-white p-4 text-left">
          <div className="flex items-center justify-between gap-3">
            <span className="truncate text-sm text-black">
              sample-video.mp4
            </span>
            <span className="shrink-0 text-xs text-neutral-500 lowercase">
              downloading
            </span>
          </div>
          <div className="mt-3 h-1 w-full overflow-hidden rounded-full bg-neutral-200">
            <div className="h-full w-2/3 rounded-full bg-black" />
          </div>
          <div className="mt-2 flex items-center justify-between text-xs text-neutral-500">
            <span>12.4 mb/s</span>
            <span className="tabular-nums">67% · 00:42 remaining</span>
          </div>
        </div>
      </section>

      <section
        id="features"
        className="mx-auto w-full max-w-5xl scroll-mt-20 px-4 pb-24 sm:px-6"
      >
        <div className="grid gap-4 sm:grid-cols-2">
          {features.map((feature) => (
            <article
              key={feature.title}
              className="rounded-2xl border border-neutral-200 bg-white p-5 transition hover:border-neutral-300"
            >
              <HugeiconsIcon
                icon={feature.icon}
                size={20}
                strokeWidth={1.5}
                color="currentColor"
                className="text-black"
              />
              <h2 className="mt-4 text-sm font-medium text-black lowercase">
                {feature.title}
              </h2>
              <p className="mt-1.5 text-sm leading-relaxed text-neutral-500">
                {feature.description}
              </p>
            </article>
          ))}
        </div>

        <p className="mt-12 text-center text-xs text-neutral-400 lowercase">
          react · typescript · fastapi · tailwind css · python
        </p>
      </section>
    </>
  );
}
