# LangGraph Chat Application

A chat application built with LangGraph, FastAPI, and Google's Gemini model.

## Features
- Real-time chat with Gemini AI model
- Conversation history tracking
- Session management
- Memory-efficient state management
- FastAPI-based REST API

## Setup

1. Clone the repository:
```bash
git clone https://github.com/bluemohawk/morning-live.ai.git
cd YOUR_REPO_NAME
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the environment:
```bash
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up your environment variables in `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

6. Run the application:
```bash
python -m src.main
```

## API Usage

### Send a message
```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"message": "Hello, how are you?", "session_id": "conversation1"}'
```

## Project Structure
```
├── src/
│   ├── __init__.py
│   ├── api.py        # FastAPI routes
│   ├── chat.py       # Chat logic and graph
│   ├── config.py     # Configuration
│   ├── llm.py        # LLM setup
│   ├── main.py       # Application entry point
│   └── models.py     # Data models
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
# morning-live.ai
# morning-live.ai
