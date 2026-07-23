# Tech Stack Recommendations

Based on the architecture described in `architecture.md`, here is a breakdown of the recommended libraries for the Frontend and Backend, utilizing Python for the backend for simplicity and given its robust AI ecosystem.

## Backend Stack (Python)

*This stack leverages Python's dominance in the AI space while perfectly fulfilling the architecture's requirements for Controllers, DTOs, interfaces, and automated documentation.*

### Core Framework & Server
- **Web Framework:** `fastapi` (Acts as the `RuleExtractorController`, handles routing, and provides the required out-of-the-box Swagger documentation API).
- **Server:** `uvicorn` (ASGI web server to run the FastAPI application).
- **DTOs & Validation:** `pydantic` (To define the `RulesResponseDTO` and validate input data structurally).
- **Security:** FastAPI's built-in `fastapi.security` module combined with `python-jose` and `passlib` (For the authentication and authorization layer, ensuring only authorized POST requests are allowed).

### Services & Engines
- **LLM Engine (Gemini):** `google-generativeai` (Google's official Python SDK to implement the `LLMEngine` interface).
- **Document Handling (File Uploads):** `python-multipart` (Required by FastAPI to parse and receive document files via the POST endpoint).
- **Document Engine (PDF):** `pdfplumber` or `pypdf` (For the Chain of Responsibility implementation to extract text from `.pdf` files).
- **Document Engine (DOCX):** `python-docx` (For extracting text from `.docx` files).
- **Document Engine (TXT):** Standard Python `open()` (No external library needed to handle `.txt` files).

## Frontend Stack

### Core Technologies
- **Framework:** React (via Vite) or Next.js (for building the Single Page Application).
- **Language:** TypeScript (To ensure end-to-end type safety when handling the `RulesResponseDTO` and managing state).
- **Styling:** Vanilla CSS or CSS Modules (for maximum flexibility and control).

### Required Libraries
- **State Management (State Service):** `zustand` (A lightweight, highly performant state management tool to act as the single source of truth for the rule extractor page).
- **API Requests (API Service):** `axios` or native `fetch` (For managing asynchronous HTTP requests to the backend).
- **Document Input / File Upload:** `react-dropzone` (To handle document drag-and-drop or file selection smoothly).
- **Dynamic Forms / Rule Editing:** `react-hook-form` (For efficiently managing the dynamic generation of filled rules input fields, allowing manual rule addition, editing, and removal).
- **Icons:** `lucide-react` (Provides clean, modern icons for intuitive UI actions like edit, remove, and add rule).
