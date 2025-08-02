# Research Paper Notes App

A companion app for reading research papers that automatically captures highlights and generates explanations using local AI models.

## Project Overview

This app creates a small window that sits alongside your research paper reader, allowing you to:
- Start reading new papers with automatic Notion page creation
- Continue reading existing papers from a selectable list
- Auto-capture copied text as highlights
- Generate AI explanations for copied content using Ollama
- Organize everything in Notion with structured subpages

## Tech Stack

- **UI Framework**: Pygame (for simplicity and small window management)
- **Notion Integration**: Notion API
- **Local AI**: Ollama for text explanations
- **Clipboard Monitoring**: pyperclip
- **Language**: Python

## 4-Phase Development Plan

### Phase 1: Core UI and Basic Structure (Week 1)
**Goal**: Get a working pygame window with basic navigation

**Deliverables**:
- ✅ Pygame window that stays on top
- ✅ Main menu with "Start New Paper" and "Continue Reading" buttons
- ✅ Input dialog for paper name
- ✅ Basic state management (menu → reading mode)
- ✅ Stop button functionality

**Key Files**:
```
src/
├── main.py           # Entry point
├── ui/
│   ├── window.py     # Main pygame window
│   ├── menus.py      # Menu screens
│   └── dialogs.py    # Input dialogs
└── core/
    └── app_state.py  # State management
```

**Success Criteria**: 
- Window opens and displays correctly
- Can navigate between screens
- Can input paper names
- Reading mode shows paper name and stop button

---

### Phase 2: Notion Integration (Week 2)
**Goal**: Connect to Notion API and create structured pages

**Deliverables**:
- ✅ Notion API integration
- ✅ Create parent page structure
- ✅ Auto-create paper pages with "Highlights" and "Notes" subpages
- ✅ List existing papers for "Continue Reading"
- ✅ Paper selection interface

**Key Files**:
```
src/
├── notion/
│   ├── client.py     # Notion API wrapper
│   ├── pages.py      # Page creation/management
│   └── config.py     # API configuration
└── config.py         # App configuration
```

**Success Criteria**:
- Can create new Notion pages with proper structure
- Can retrieve list of existing papers
- Can select papers from scrollable list
- Proper error handling for API failures

---

### Phase 3: Clipboard Monitoring and Highlights (Week 3)
**Goal**: Capture copied text and save to Notion highlights

**Deliverables**:
- ✅ Clipboard monitoring system
- ✅ Auto-save copied text to Highlights page
- ✅ Timestamp and organize highlights
- ✅ Background processing without blocking UI
- ✅ Visual feedback for successful captures

**Key Files**:
```
src/
├── clipboard/
│   ├── monitor.py    # Clipboard watching
│   └── processor.py  # Text processing
└── notion/
    └── highlights.py # Highlights management
```

**Success Criteria**:
- Clipboard monitoring works reliably
- Highlights appear in Notion immediately
- UI remains responsive during captures
- Clear visual feedback for user

---

### Phase 4: AI Integration and Notes Generation (Week 4)
**Goal**: Generate explanations using Ollama and save to Notes page

**Deliverables**:
- ✅ Ollama integration and model management
- ✅ Generate explanations from highlighted text
- ✅ Save AI-generated notes to Notes subpage
- ✅ Error handling and retry logic
- ✅ Settings for model selection and prompts

**Key Files**:
```
src/
├── ai/
│   ├── ollama_client.py  # Ollama integration
│   ├── prompts.py        # Explanation prompts
│   └── processor.py      # AI processing logic
└── notion/
    └── notes.py          # Notes management
```

**Success Criteria**:
- AI explanations generate reliably
- Notes are properly formatted in Notion
- Good error handling for AI failures
- Configurable AI behavior

## Installation & Setup

### Prerequisites
```bash
# Install Python dependencies
pip install pygame notion-client pyperclip requests

# Install and start Ollama
# Visit: https://ollama.ai
ollama pull llama2  # or your preferred model
```

### Configuration
1. Create a Notion integration at https://developers.notion.com
2. Copy your integration token
3. Share your parent Notion page with the integration
4. Create `config.py`:

```python
NOTION_TOKEN = "your_notion_integration_token"
NOTION_PARENT_PAGE_ID = "your_parent_page_id"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama2"
```

### Running
```bash
python src/main.py
```

## Project Structure
```
research-notes-app/
├── README.md
├── requirements.txt
├── config.py
├── src/
│   ├── main.py
│   ├── ui/
│   ├── notion/
│   ├── clipboard/
│   ├── ai/
│   └── core/
├── tests/
└── docs/
```

## Development Guidelines

### Code Style
- Use Python type hints
- Follow PEP 8 naming conventions
- Add docstrings for all functions
- Keep functions small and focused

### Error Handling
- Graceful API failure handling
- User-friendly error messages
- Retry logic for network operations
- Logging for debugging

### Testing Strategy
- Unit tests for core logic
- Integration tests for API connections
- Manual testing for UI interactions
- Test with various clipboard content types

## Future Enhancements (Post-MVP)

- **PDF Integration**: Direct PDF highlighting support
- **Search Functionality**: Search across all notes and highlights
- **Export Options**: Export to markdown, PDF
- **Sync Indicators**: Show sync status with Notion
- **Keyboard Shortcuts**: Quick actions without mouse
- **Multiple Models**: Switch between different AI models
- **Custom Prompts**: User-defined explanation templates
- **Dark Mode**: Theme options for the UI

## Troubleshooting

### Common Issues
1. **Pygame window not appearing**: Check display settings
2. **Notion API errors**: Verify token and page permissions
3. **Clipboard not monitoring**: Check permissions on macOS/Linux
4. **Ollama connection failed**: Ensure Ollama is running locally

### Debug Mode
Set `DEBUG=True` in config.py for verbose logging.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the coding guidelines
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

## Quick Start Checklist

- [ ] Phase 1: Basic UI working
- [ ] Phase 2: Notion pages creating
- [ ] Phase 3: Clipboard capturing highlights
- [ ] Phase 4: AI generating explanations
- [ ] Full integration testing
- [ ] Documentation complete
- [ ] Ready for daily use!