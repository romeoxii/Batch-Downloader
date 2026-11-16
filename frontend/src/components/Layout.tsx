import { Link, NavLink, Outlet } from "react-router-dom";
import { HugeiconsIcon } from "@hugeicons/react";
import { GithubIcon } from "@hugeicons/core-free-icons";

// Update this if the repository URL changes.
const GITHUB_URL = "https://github.com/romeoxii/Batch-Downloader";

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `rounded-full px-3 py-1.5 text-sm transition ${
    isActive
      ? "font-medium text-black"
      : "text-neutral-500 hover:text-black"
  }`;

export function Layout() {
  return (
    <div className="flex min-h-screen flex-col bg-white text-black">
      <header className="sticky top-0 z-20 border-b border-neutral-200 bg-white/90 backdrop-blur-sm">
        <nav className="mx-auto flex h-14 w-full max-w-5xl items-center justify-between px-4 sm:px-6">
          <Link to="/" className="flex items-center gap-2">
            <img
              src="/image.png"
              alt=""
              className="h-7 w-7 rounded-lg object-cover"
            />
            <span className="text-sm font-semibold tracking-tight lowercase">
              fetchflow
            </span>
          </Link>

          <div className="flex items-center gap-1">
            <NavLink to="/" end className={navLinkClass}>
              home
            </NavLink>
            <NavLink to="/downloader" className={navLinkClass}>
              downloader
            </NavLink>
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              aria-label="GitHub"
              className="ml-1 flex items-center gap-2 rounded-full px-3 py-1.5 text-sm text-neutral-500 transition hover:text-black"
            >
              <HugeiconsIcon icon={GithubIcon} size={16} strokeWidth={1.5} />
            </a>
          </div>
        </nav>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-neutral-200">
        <div className="mx-auto flex w-full max-w-5xl flex-col items-center justify-between gap-2 px-4 py-6 text-xs text-neutral-500 sm:flex-row sm:px-6">
          <p className="lowercase">built by romeoxii</p>
          <p className="lowercase">react · typescript · fastapi · tailwind css</p>
        </div>
      </footer>
    </div>
  );
}
