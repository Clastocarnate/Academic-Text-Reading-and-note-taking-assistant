# Research Paper Notes App - Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Phase 1: Core UI and Basic Structure](#phase-1-core-ui-and-basic-structure)
3. [Phase 2: Notion Integration](#phase-2-notion-integration)
4. [Phase 3: Clipboard Monitoring and Highlights](#phase-3-clipboard-monitoring-and-highlights)
5. [Phase 4: AI Integration and Notes Generation](#phase-4-ai-integration-and-notes-generation)
6. [Data Flow Diagrams](#data-flow-diagrams)
7. [Error Handling Strategy](#error-handling-strategy)
8. [Performance Considerations](#performance-considerations)
9. [Security Guidelines](#security-guidelines)

---

## Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Pygame UI    │    │  Notion API     │    │   Ollama AI     │
│   (Frontend)    │────│  (Backend)      │    │   (Local AI)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Clipboard       │
                    │ Monitor         │
                    │ (System)        │
                    └─────────────────┘
```

### Core Components
- **UI Layer**: Pygame-based interface for user interactions
- **State Management**: Centralized application state handling
- **API Layer**: Notion and Ollama API integrations
- **Background Services**: Clipboard monitoring and AI processing
- **Configuration**: Centralized settings and API credentials

---

## Phase 1: Core UI and Basic Structure

### 1.1 Main Application Entry Point

**File**: `src/main.py`

```python
"""
Main application entry point.
Initializes pygame, creates the main window, and starts the event loop.
"""

import pygame
import sys
from typing import Optional
from ui.window import MainWindow
from core.app_state import AppState
from core.config import Config

class Application:
    """Main application class handling initialization and lifecycle."""
    
    def __init__(self):
        self.config = Config()
        self.app_state = AppState()
        self.window: Optional[MainWindow] = None
        self._running = False
    
    def initialize(self) -> bool:
        """Initialize pygame and create main window."""
        try:
            pygame.init()
            self.window = MainWindow(self.config, self.app_state)
            self._running = True
            return True
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False
    
    def run(self) -> None:
        """Main application loop."""
        if not self.initialize():
            return
        
        clock = pygame.time.Clock()
        
        while self._running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                else:
                    self.window.handle_event(event)
            
            # Update application state
            self.window.update()
            
            # Render
            self.window.render()
            
            # Maintain 60 FPS
            clock.tick(60)
        
        self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources before exit."""
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Application()
    app.run()
```

### 1.2 Main Window Management

**File**: `src/ui/window.py`

```python
"""
Main window class handling pygame window creation and management.
"""

import pygame
from typing import Tuple, Optional
from enum import Enum
from core.app_state import AppState, AppScreen
from core.config import Config
from ui.menus import MainMenu, ReadingScreen
from ui.dialogs import InputDialog

class WindowFlags:
    """Window configuration flags."""
    STAY_ON_TOP = pygame.HWSURFACE | pygame.DOUBLEBUF
    RESIZABLE = pygame.RESIZABLE

class MainWindow:
    """Main application window managing all UI screens."""
    
    def __init__(self, config: Config, app_state: AppState):
        self.config = config
        self.app_state = app_state
        self.size = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # Initialize pygame window
        self.screen = pygame.display.set_mode(
            self.size, 
            WindowFlags.STAY_ON_TOP
        )
        pygame.display.set_caption("Research Notes")
        
        # Initialize UI components
        self.main_menu = MainMenu(self.screen, self.app_state)
        self.reading_screen = ReadingScreen(self.screen, self.app_state)
        self.input_dialog: Optional[InputDialog] = None
        
        # Colors
        self.bg_color = (40, 40, 40)
        self.text_color = (255, 255, 255)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events and route to appropriate screen."""
        current_screen = self.app_state.current_screen
        
        # Handle input dialog events first
        if self.input_dialog and self.input_dialog.active:
            result = self.input_dialog.handle_event(event)
            if result is not None:
                self._handle_dialog_result(result)
                self.input_dialog = None
            return
        
        # Route events to current screen
        if current_screen == AppScreen.MAIN_MENU:
            self._handle_main_menu_event(event)
        elif current_screen == AppScreen.READING:
            self._handle_reading_event(event)
        elif current_screen == AppScreen.PAPER_SELECTION:
            self._handle_paper_selection_event(event)
    
    def _handle_main_menu_event(self, event: pygame.event.Event) -> None:
        """Handle main menu events."""
        action = self.main_menu.handle_event(event)
        
        if action == "start_new":
            self.input_dialog = InputDialog(
                self.screen, 
                "Enter paper name:",
                callback_data="new_paper"
            )
        elif action == "continue_reading":
            self.app_state.set_screen(AppScreen.PAPER_SELECTION)
    
    def _handle_reading_event(self, event: pygame.event.Event) -> None:
        """Handle reading screen events."""
        action = self.reading_screen.handle_event(event)
        
        if action == "stop":
            self.app_state.stop_reading()
            self.app_state.set_screen(AppScreen.MAIN_MENU)
    
    def _handle_paper_selection_event(self, event: pygame.event.Event) -> None:
        """Handle paper selection screen events."""
        # TODO: Implement in Phase 2
        pass
    
    def _handle_dialog_result(self, result: str) -> None:
        """Handle input dialog results."""
        if result and result.strip():
            paper_name = result.strip()
            self.app_state.start_new_paper(paper_name)
            self.app_state.set_screen(AppScreen.READING)
    
    def update(self) -> None:
        """Update window state and components."""
        # Update components based on current screen
        current_screen = self.app_state.current_screen
        
        if current_screen == AppScreen.MAIN_MENU:
            self.main_menu.update()
        elif current_screen == AppScreen.READING:
            self.reading_screen.update()
    
    def render(self) -> None:
        """Render the current screen."""
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Render current screen
        current_screen = self.app_state.current_screen
        
        if current_screen == AppScreen.MAIN_MENU:
            self.main_menu.render()
        elif current_screen == AppScreen.READING:
            self.reading_screen.render()
        elif current_screen == AppScreen.PAPER_SELECTION:
            self._render_paper_selection()
        
        # Render dialog on top if active
        if self.input_dialog and self.input_dialog.active:
            self.input_dialog.render()
        
        # Update display
        pygame.display.flip()
    
    def _render_paper_selection(self) -> None:
        """Render paper selection screen."""
        # TODO: Implement in Phase 2
        font = pygame.font.Font(None, 36)
        text = font.render("Paper Selection - Coming Soon", True, self.text_color)
        rect = text.get_rect(center=(self.size[0]//2, self.size[1]//2))
        self.screen.blit(text, rect)
```

### 1.3 Menu System

**File**: `src/ui/menus.py`

```python
"""
UI menu components for different application screens.
"""

import pygame
from typing import Optional, List, Tuple
from core.app_state import AppState

class Button:
    """Simple button component."""
    
    def __init__(self, rect: pygame.Rect, text: str, font_size: int = 24):
        self.rect = rect
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False
        
        # Colors
        self.normal_color = (70, 70, 70)
        self.hover_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle button events. Returns True if clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the button."""
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class MainMenu:
    """Main menu screen with Start New and Continue Reading options."""
    
    def __init__(self, screen: pygame.Surface, app_state: AppState):
        self.screen = screen
        self.app_state = app_state
        self.screen_size = screen.get_size()
        
        # Create buttons
        button_width, button_height = 200, 50
        center_x = self.screen_size[0] // 2
        
        self.start_button = Button(
            pygame.Rect(center_x - button_width//2, 150, button_width, button_height),
            "Start New Paper"
        )
        
        self.continue_button = Button(
            pygame.Rect(center_x - button_width//2, 220, button_width, button_height),
            "Continue Reading"
        )
        
        # Title font
        self.title_font = pygame.font.Font(None, 48)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle menu events. Returns action string or None."""
        if self.start_button.handle_event(event):
            return "start_new"
        elif self.continue_button.handle_event(event):
            return "continue_reading"
        return None
    
    def update(self) -> None:
        """Update menu state."""
        pass
    
    def render(self) -> None:
        """Render the main menu."""
        # Render title
        title = self.title_font.render("Research Notes", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_size[0]//2, 80))
        self.screen.blit(title, title_rect)
        
        # Render buttons
        self.start_button.render(self.screen)
        self.continue_button.render(self.screen)

class ReadingScreen:
    """Reading mode screen showing current paper and stop button."""
    
    def __init__(self, screen: pygame.Surface, app_state: AppState):
        self.screen = screen
        self.app_state = app_state
        self.screen_size = screen.get_size()
        
        # Create stop button
        button_width, button_height = 100, 40
        self.stop_button = Button(
            pygame.Rect(self.screen_size[0]//2 - button_width//2, 200, 
                       button_width, button_height),
            "Stop",
            font_size=20
        )
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.paper_font = pygame.font.Font(None, 28)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle reading screen events."""
        if self.stop_button.handle_event(event):
            return "stop"
        return None
    
    def update(self) -> None:
        """Update reading screen."""
        pass
    
    def render(self) -> None:
        """Render the reading screen."""
        center_x = self.screen_size[0] // 2
        
        # Render "Reading:" label
        reading_text = self.title_font.render("Reading:", True, (255, 255, 255))
        reading_rect = reading_text.get_rect(center=(center_x, 100))
        self.screen.blit(reading_text, reading_rect)
        
        # Render paper name
        paper_name = self.app_state.current_paper or "Unknown Paper"
        paper_text = self.paper_font.render(paper_name, True, (200, 200, 255))
        paper_rect = paper_text.get_rect(center=(center_x, 140))
        self.screen.blit(paper_text, paper_rect)
        
        # Render stop button
        self.stop_button.render(self.screen)
        
        # Render status indicators
        self._render_status_indicators()
    
    def _render_status_indicators(self) -> None:
        """Render reading status indicators."""
        font = pygame.font.Font(None, 20)
        
        # Clipboard monitoring status
        clipboard_status = "Monitoring clipboard..." if self.app_state.is_reading else "Stopped"
        status_color = (0, 255, 0) if self.app_state.is_reading else (255, 0, 0)
        
        status_text = font.render(clipboard_status, True, status_color)
        self.screen.blit(status_text, (10, self.screen_size[1] - 30))
```

### 1.4 Input Dialog System

**File**: `src/ui/dialogs.py`

```python
"""
Dialog components for user input.
"""

import pygame
from typing import Optional

class InputDialog:
    """Modal input dialog for text entry."""
    
    def __init__(self, screen: pygame.Surface, prompt: str, callback_data: str = ""):
        self.screen = screen
        self.prompt = prompt
        self.callback_data = callback_data
        self.active = True
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # Dialog dimensions
        self.width = 400
        self.height = 150
        screen_size = screen.get_size()
        self.x = (screen_size[0] - self.width) // 2
        self.y = (screen_size[1] - self.height) // 2
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Input field
        self.input_rect = pygame.Rect(self.x + 20, self.y + 60, self.width - 40, 30)
        
        # Fonts
        self.prompt_font = pygame.font.Font(None, 24)
        self.input_font = pygame.font.Font(None, 20)
        
        # Colors
        self.bg_color = (60, 60, 60)
        self.border_color = (150, 150, 150)
        self.input_bg_color = (80, 80, 80)
        self.text_color = (255, 255, 255)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle dialog events. Returns input text when submitted, None when cancelled."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
                return self.text
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                return None
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Add character to text
                if event.unicode.isprintable() and len(self.text) < 50:
                    self.text += event.unicode
        
        return None
    
    def update(self) -> None:
        """Update dialog state."""
        # Update cursor blink
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  # Blink every 30 frames (0.5 seconds at 60 FPS)
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def render(self) -> None:
        """Render the input dialog."""
        if not self.active:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw dialog background
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2)
        
        # Draw prompt text
        prompt_surface = self.prompt_font.render(self.prompt, True, self.text_color)
        prompt_rect = prompt_surface.get_rect(center=(self.x + self.width//2, self.y + 30))
        self.screen.blit(prompt_surface, prompt_rect)
        
        # Draw input field
        pygame.draw.rect(self.screen, self.input_bg_color, self.input_rect)
        pygame.draw.rect(self.screen, self.border_color, self.input_rect, 1)
        
        # Draw input text
        if self.text:
            text_surface = self.input_font.render(self.text, True, self.text_color)
            text_y = self.input_rect.y + (self.input_rect.height - text_surface.get_height()) // 2
            self.screen.blit(text_surface, (self.input_rect.x + 5, text_y))
        
        # Draw cursor
        if self.cursor_visible:
            text_width = self.input_font.size(self.text)[0]
            cursor_x = self.input_rect.x + 5 + text_width
            cursor_y = self.input_rect.y + 5
            pygame.draw.line(self.screen, self.text_color, 
                           (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + 20), 1)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 18)
        instruction_text = instruction_font.render("Press Enter to confirm, Escape to cancel", 
                                                 True, (180, 180, 180))
        instruction_rect = instruction_text.get_rect(center=(self.x + self.width//2, self.y + 120))
        self.screen.blit(instruction_text, instruction_rect)
```

### 1.5 Application State Management

**File**: `src/core/app_state.py`

```python
"""
Centralized application state management.
"""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass
import threading

class AppScreen(Enum):
    """Application screen states."""
    MAIN_MENU = "main_menu"
    READING = "reading"
    PAPER_SELECTION = "paper_selection"

@dataclass
class PaperInfo:
    """Information about a research paper."""
    name: str
    notion_page_id: Optional[str] = None
    highlights_page_id: Optional[str] = None
    notes_page_id: Optional[str] = None
    created_at: Optional[str] = None

class AppState:
    """Central application state manager."""
    
    def __init__(self):
        self.current_screen = AppScreen.MAIN_MENU
        self.current_paper: Optional[str] = None
        self.current_paper_info: Optional[PaperInfo] = None
        self.is_reading = False
        self.available_papers: List[PaperInfo] = []
        
        # Threading lock for state changes
        self._lock = threading.Lock()
        
        # Status tracking
        self.last_highlight_time: Optional[float] = None
        self.highlight_count = 0
        self.note_count = 0
    
    def set_screen(self, screen: AppScreen) -> None:
        """Change the current screen."""
        with self._lock:
            self.current_screen = screen
    
    def start_new_paper(self, paper_name: str) -> None:
        """Start reading a new paper."""
        with self._lock:
            self.current_paper = paper_name
            self.current_paper_info = PaperInfo(name=paper_name)
            self.is_reading = True
            self.highlight_count = 0
            self.note_count = 0
    
    def start_existing_paper(self, paper_info: PaperInfo) -> None:
        """Start reading an existing paper."""
        with self._lock:
            self.current_paper = paper_info.name
            self.current_paper_info = paper_info
            self.is_reading = True
    
    def stop_reading(self) -> None:
        """Stop the current reading session."""
        with self._lock:
            self.is_reading = False
    
    def add_available_paper(self, paper_info: PaperInfo) -> None:
        """Add a paper to the available papers list."""
        with self._lock:
            self.available_papers.append(paper_info)
    
    def update_paper_info(self, paper_info: PaperInfo) -> None:
        """Update current paper information."""
        with self._lock:
            self.current_paper_info = paper_info
    
    def increment_highlight_count(self) -> None:
        """Increment the highlight counter."""
        with self._lock:
            self.highlight_count += 1
            self.last_highlight_time = time.time()
    
    def increment_note_count(self) -> None:
        """Increment the note counter."""
        with self._lock:
            self.note_count += 1
    
    def get_status_summary(self) -> dict:
        """Get current status summary."""
        with self._lock:
            return {
                "current_paper": self.current_paper,
                "is_reading": self.is_reading,
                "highlight_count": self.highlight_count,
                "note_count": self.note_count,
                "screen": self.current_screen.value
            }
```

### 1.6 Configuration Management

**File**: `src/core/config.py`

```python
"""
Application configuration management.
"""

import os
from typing import Optional

class Config:
    """Application configuration settings."""
    
    def __init__(self):
        # Window settings
        self.WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "500"))
        self.WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "350"))
        self.WINDOW_TITLE = "Research Notes"
        
        # API Configuration (to be used in Phase 2)
        self.NOTION_TOKEN: Optional[str] = os.getenv("NOTION_TOKEN")
        self.NOTION_PARENT_PAGE_ID: Optional[str] = os.getenv("NOTION_PARENT_PAGE_ID")
        
        # Ollama Configuration (to be used in Phase 4)
        self.OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
        
        # Clipboard settings (to be used in Phase 3)
        self.CLIPBOARD_CHECK_INTERVAL = float(os.getenv("CLIPBOARD_CHECK_INTERVAL", "0.5"))
        self.MIN_HIGHLIGHT_LENGTH = int(os.getenv("MIN_HIGHLIGHT_LENGTH", "10"))
        
        # Debug settings
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Phase 2 validation
        if not self.NOTION_TOKEN:
            errors.append("NOTION_TOKEN not set")
        
        if not self.NOTION_PARENT_PAGE_ID:
            errors.append("NOTION_PARENT_PAGE_ID not set")
        
        return errors
    
    def is_valid_for_phase(self, phase: int) -> bool:
        """Check if configuration is valid for a specific phase."""
        if phase == 1:
            return True  # Phase 1 only needs basic settings
        elif phase == 2:
            return bool(self.NOTION_TOKEN and self.NOTION_PARENT_PAGE_ID)
        elif phase == 3:
            return bool(self.NOTION_TOKEN and self.NOTION_PARENT_PAGE_ID)
        elif phase == 4:
            return bool(self.NOTION_TOKEN and self.NOTION_PARENT_PAGE_ID)
        
        return False
```

---

## Phase 2: Notion Integration

### 2.1 Notion API Client

**File**: `src/notion/client.py`

```python
"""
Notion API client for managing pages and content.
"""

import requests
from typing import Dict, List, Optional, Any
import json
import time
from datetime import datetime
from core.config import Config

class NotionAPIError(Exception):
    """Custom exception for Notion API errors."""
    pass

class NotionClient:
    """Client for interacting with Notion API."""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {config.NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     retries: int = 3) -> Dict[str, Any]:
        """Make HTTP request to Notion API with retry logic."""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                if method.upper() == "GET":
                    response = self.session.get(url, params=data)
                elif method.upper() == "POST":
                    response = self.session.post(url, json=data)
                elif method.upper() == "PATCH":
                    response = self.session.patch(url, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise NotionAPIError(f"API request failed after {retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise NotionAPIError("Request failed unexpectedly")
    
    def create_page(self, parent_id: str, title: str, properties: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new page in Notion."""
        data = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            }
        }
        
        if properties:
            data["properties"].update(properties)
        
        return self._make_request("POST", "/pages", data)
    
    def get_page_children(self, page_id: str) -> List[Dict[str, Any]]:
        """Get all child pages of a page."""
        children = []
        start_cursor = None
        
        while True:
            params = {}
            if start_cursor:
                params["start_cursor"] = start_cursor
            
            response = self._make_request("GET", f"/blocks/{page_id}/children", params)
            children.extend(response.get("results", []))
            
            if not response.get("has_more", False):
                break
            
            start_cursor = response.get("next_cursor")
        
        return children
    
    def search_pages(self, query: str = "", parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for pages in Notion."""
        data = {
            "query": query,
            "filter": {
                "value": "page",
                "property": "object"
            }
        }
        
        if parent_id:
            data["filter"]["parent"] = {"page_id": parent_id}
        
        response = self._make_request("POST", "/search", data)
        return response.get("results", [])
    
    def append_block_children(self, page_id: str, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Append blocks to a page."""
        data = {
            "children": blocks
        }
        
        return self._make_request("PATCH", f"/blocks/{page_id}/children", data)
    
    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get page information."""
        return self._make_request("GET", f"/pages/{page_id}")
    
    def update_page(self, page_id: str, properties: Dict[str