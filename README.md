# SkinnyPostman

A lightweight Flask‑based web application for serving Postman collections for API testing.

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Project Structure](#project-structure)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Configuration](#configuration)  
- [Adding / Updating Collections](#adding-and-updating-collections)
- [Demo](#demo) 
- [Contributing](#contributing)  
- [License](#license)  

## Overview

**SkinnyPostman** is a simple tool built with Flask that:

- Serves static HTML/UI components (`static/`)  
- Renders templates (`templates/`)  
- Loads a Postman collection file (e.g. `collections.json`)  
- Allows users to view and test APIs via the UI  
- Offers an easy way to deploy API testing endpoints with minimal overhead  

This project is intended for users who want a slim interface around Postman collections without requiring the full Postman server or enterprise tooling.

## Features

- Lightweight Flask app  
- Minimal dependencies  
- Self-contained collection file support  
- Simple UI for API navigation and request execution  
- Easy to extend with custom features  

## Project Structure

```
SkinnyPostman/
├── app.py
├── collections.json
├── static/
│   └── … (CSS, images)
└── templates/
    └── … (HTML templates)
```

- **app.py** — main Flask server script  
- **collections.json** — the collection file the app serves  
- **static/** — static assets (CSS, images)  
- **templates/** — Jinja2 templates for UI rendering  

## Requirements

- Python 3.7+  
- (Optional) Virtual environment
- requirements.txt

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/eachtrach/SkinnyPostman.git
    cd SkinnyPostman
    ```

2. (Optional) Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
   
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the Flask app:

```bash
python app.py
```

By default, it will start a local server (e.g. `http://127.0.0.1:5000/`). Open that in your browser to access the UI.

From the UI, you should see the API endpoints defined in `collections.json` and be able to execute requests via the interface.

You can modify or replace `collections.json` collection file.

## Configuration

You might want to configure:

- Host / port binding  
- Debug mode  
- Collection file path  
- UI theming or custom templates  
- Authentication headers or tokens  

You can extend `app.py` to accept environment variables or command‑line arguments (e.g. `--port`, `--collection-file`) to make it more flexible.

## Adding and Updating Collections

To update or add an API collection:

1. Replace or modify `collections.json` with your new Postman collection JSON (exported from Postman).  
2. Ensure the structure is valid JSON and matches Postman’s collection schema.  
3. Reload / restart the server (if already running).  
4. Visit the UI and verify the new endpoints appear.

## Demo



https://github.com/user-attachments/assets/9d5b9423-9333-4df7-98b9-577416862ced



## Contributing

Contributions are welcome! 

If you’d like to contribute:

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit changes & push  
4. Open a pull request  

Please include clear descriptions, tests (if applicable), and ensure existing features still work.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

