# 🇧🇩 BD Travel Bot

A modern AI-powered travel guide chatbot for Bangladesh, built with Streamlit and LangGraph.

## ✨ Features

- 🤖 **AI-Powered**: Uses Google Gemini and vector search for accurate travel information
- 💬 **Interactive Chat**: Beautiful streaming chat interface with real-time responses
- 🌐 **Bilingual Support**: Responds in Bengali and English
- 🎨 **Modern UI**: Sleek design with animations and responsive layout
- 📊 **Smart Search**: Vector-based knowledge retrieval from travel database
- 🏖️ **Comprehensive Coverage**: Beaches, historical sites, nature spots, cuisine, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Required API keys (see Environment Setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd bd-travel-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   NVIDIA_API_KEY=your_nvidia_api_key
   DB_URI=your_database_connection_string
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```
   
   Or use the helper script:
   ```bash
   python run_app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: LangGraph, LangChain, Google Gemini
- **Database**: PostgreSQL with PGVector
- **Embeddings**: NVIDIA BGE-M3
- **Styling**: Custom CSS with Google Fonts

## 📁 Project Structure

```
bd-travel-bot/
├── agent.py              # LangGraph agent configuration
├── streamlit_app.py      # Main Streamlit application
├── tools.py              # Knowledge retrieval tools
├── utils.py              # LLM and embedding utilities
├── dataloader.py         # Data loading utilities
├── requirements.txt      # Python dependencies
├── run_app.py           # Helper script to run the app
└── README.md            # This file
```

## 💡 Usage

1. **Start a conversation** by typing in the chat input
2. **Ask about destinations** in Bengali or English
3. **Get detailed information** about:
   - 🏖️ Beaches and coastal areas
   - 🏛️ Historical monuments
   - 🏞️ Natural attractions
   - 🍽️ Local cuisine
   - 🏨 Accommodation options
   - 🚗 Transportation details

## 🔧 Configuration

The bot is configured to:
- Respond in Bengali by default
- Provide detailed answers (max 10 sentences)
- Use vector search for relevant information
- Stream responses in real-time

## 📝 Example Queries

- "কুয়াকাটা সমুদ্র সৈকত সম্পর্কে বলুন"
- "Tell me about Cox's Bazar"
- "বাংলাদেশের ঐতিহাসিক স্থানগুলো জানতে চাই"
- "What are the best places to visit in Sylhet?"

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ for Bangladesh** | Powered by AI & Streamlit
