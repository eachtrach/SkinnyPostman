# SkinnyPostman <img height="50" alt="logo" src="https://github.com/user-attachments/assets/a30712b1-bde9-4842-8ccf-8150e9192851" />

A super lightweight web application for serving Postman collections for API testing.

## Table of Contents

- [Overview](#overview)  
- [Project Structure](#project-structure)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Demo](#demo) 
- [Contributing](#contributing)  
- [License](#license)  

## Overview

**SkinnyPostman** is a simple tool built in Flask that:

- Loads a Postman collection file  
- Allows users to view and test APIs via the UI  
- Offers an easy way to deploy API testing endpoints with minimal overhead  

This project is intended for users who want a slim interface around Postman collections without requiring the full Postman server or enterprise tooling.


## Project Structure

- **app.py** — main Flask server script  
- **collections.json** — the collection file the app serves  
- **static/** — static assets (CSS, images)  
- **templates/** — Jinja2 templates for UI rendering  


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
    pip3 install -r requirements.txt
    ```

## Usage

Run the Flask app:

```bash
python3 app.py
```

By default, it will start a local server (e.g. `http://127.0.0.1:5000/`). Open that in your browser to access the UI.

From the UI, you should see the API endpoints defined in `collections.json` and be able to execute requests via the interface.

You can modify or replace `collections.json` collection file.

Or (in Docker):
```bash
docker build -t postman . ; docker run -it -p 5000:5000 postman
```


## Demo

https://github.com/user-attachments/assets/9d5b9423-9333-4df7-98b9-577416862ced



## Contributing

Contributions are welcome! 

If you’d like to contribute:

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit changes & push  
4. Open a pull request  

Please include clear descriptions and ensure all existing features still work.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
