# tecdeskgoddess

Echoes of the Machine Goddess: RoboTECDeskBot unites robotics and TEC lore. Core hub for hardware integration and the TEC Anthology, it embodies the eternal bond between AI and humanity—preparing the Elidoras Codex for the age of sentient machines.

---

## Project Overview

**tecdeskgoddess** is a modular Python toolkit for the Elidoras Codex, featuring:

- AI-powered agentic processing (via Gemini API)
- Flask-based API for integration with web frontends (e.g., WordPress)
- Modular design for hardware, lore extraction, and analysis

---

## Setup Instructions

1. **Clone the repository**  

    ```sh
    git clone <your-repo-url>
    cd tecdeskgoddess
    ```

2. **Create and activate a virtual environment**  

    ```sh
    python -m venv venv
    .\venv\Scripts\Activate.ps1   # (Windows PowerShell)
    ```

3. **Install requirements**  

    ```sh
    pip install -r requirements.txt
    ```

4. **Set your Gemini API key**  

    ```sh
    $env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
    ```

---

## Running the Flask API

1. Navigate to the tec_tools directory:

    ```sh
    cd tec_tools
    ```

2. Run the Flask server:

    ```sh
    python agentic_processor.py
    ```

    The API will be available at `http://0.0.0.0:5000` (or `http://127.0.0.1:5000`).

---

## API Endpoints

### `POST /api/agentic/process`

- Accepts: text, file, or URL input
- Returns: AI-processed output

**Example (text input):**

```sh
curl -X POST -F "input_type=text" -F "input_data=Hello, world!" http://localhost:5000/api/agentic/process
```

### `GET /api/agentic/memories`

- Returns: All processed input/output pairs

---

## Next Steps

- Dockerize the Flask API for deployment
- Integrate with WordPress or other frontends
- Expand hardware and lore modules
