# Multi-Agent AI Assistant

A sophisticated multi-agent AI system built with Pydantic AI and Streamlit, designed to accomplish complex tasks through agent collaboration.

## Project Overview

This project implements a multi-agent architecture where different specialized AI agents work together to solve problems. The system features:

- Multiple specialized agents with different capabilities
- A coordinator that manages task delegation and agent communication
- A Streamlit-based UI for interacting with the system
- Pydantic models for structured data handling

## Project Structure

```
multi-agent-assistant/
├── .cursor/           # Cursor AI IDE configuration
├── agents/            # Individual agent implementations
│   ├── __init__.py
│   ├── base.py        # Base agent class
│   └── specialized/   # Specialized agent implementations
├── coordinator/       # Agent coordination logic
│   ├── __init__.py
│   └── orchestrator.py
├── models/            # Pydantic data models
│   ├── __init__.py
│   └── messages.py    # Message schemas
├── app/                # Streamlit UI components
│   └── app.py         # Main Streamlit application
├── utils/             # Utility functions
├── pyproject.toml     # Project dependencies
└── README.md          # This file
```

## Development Roadmap

1. **Phase 1: Foundation**
   - Set up project structure
   - Define core agent interfaces
   - Implement basic message passing

2. **Phase 2: Agent Implementation**
   - Develop specialized agents
   - Create the coordinator system
   - Implement agent communication protocols

3. **Phase 3: UI Development**
   - Build Streamlit interface
   - Implement visualization of agent activities
   - Create user input handling

4. **Phase 4: Testing & Refinement**
   - Test agent interactions
   - Optimize performance
   - Add advanced features

## Getting Started

1. Clone this repository
2. Run `uv init` to initialize the project
3. Install dependencies with `uv sync`
4. Run the application with `uv run streamlit run ui/app.py`
