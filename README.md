# Batch Downloader

A Python-based batch file downloader built as a learning project while studying Python, HTTP requests, file handling, error handling, and application structure.

The goal of this project is not just to build a downloader, but to use a real project to progressively learn Python concepts and apply them in practice.

## Current Features

- Download files from URLs
- Save downloaded files locally
- Stream file content instead of loading the entire file into memory
- Display download progress
- Handle HTTP responses
- Save files with appropriate filenames
- Ignore incomplete `.part` files
- Keep downloaded files and the Python virtual environment out of Git

## What I Have Learned

While building this project, I have been learning and applying several Python concepts, including:

### Python Fundamentals

- Variables and data types
- Functions
- Conditional statements
- Loops
- Lists and dictionaries
- Exception handling
- Working with modules and packages

### HTTP & Requests

I learned how HTTP works from the perspective of a Python application, including:

- URLs and HTTP requests
- HTTP response status codes
- Request headers
- Streaming responses
- Downloading data in chunks
- Handling failed HTTP requests

### File Handling

The downloader also gave me practical experience with:

- Opening and writing files
- Binary file operations
- Writing data incrementally
- File paths
- Filenames and extensions
- Handling partial downloads

### Python Environment & Dependencies

I also learned how to:

- Create and use a Python virtual environment
- Install third-party packages
- Manage dependencies with `requirements.txt`
- Use `.gitignore` correctly

### Git & GitHub

The project has also been used to practice Git:

- Initializing a repository
- Creating commits
- Creating and switching branches
- Connecting a local repository to GitHub
- Pushing code to GitHub
- Managing files that should and shouldn't be tracked

## What's Coming

This project is being developed progressively as I continue learning Python.

Planned improvements include:

- Refactoring the current code into cleaner functions
- Better error handling
- Improved download validation
- More robust filename handling
- Multiple file downloads
- Better logging
- Object-oriented design with Python classes
- Configuration and reusable components
- Further improvements to the project structure
- Building an API around the downloader using FastAPI

The eventual goal is to turn this from a simple Python downloader script into a more structured application with a proper backend/API.

## Project Status

**Work in Progress**

This repository represents my progress while learning Python through a practical project. The code and architecture will evolve as I learn more.

## Tech Stack

- Python
- Requests
- Git
- GitHub
- FastAPI _(planned)_

## Author

**romeoxii**

Built as part of my Python learning journey.
