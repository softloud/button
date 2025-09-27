"""
Press A Button Now - Complete Documentation
===========================================

A satirical text-based adventure game exploring the lived experience of working in data science.

## Overview

Press A Button Now is a Python-based interactive narrative game that takes players through
the typical data science workflow while highlighting the frustrations, uncertainty, and
cyclical nature of real data work. The game uses Google Sheets as a dynamic content
management system, allowing for easy narrative updates without code changes.

## Architecture

### Core Components

1. **ButtonDf** (`classes/button_df.py`)
   - Google Sheets connector with exponential backoff retry logic
   - Handles rate limiting and network failures gracefully
   - Environment-specific .env configuration loading

2. **ButtonDat** (`classes/button_dat.py`) 
   - Multi-source data aggregator combining edges, nodes, and text
   - Comprehensive validation with detailed error reporting
   - High-level query interface for game logic

3. **NodeEngine** (`classes/node_engine.py`)
   - Individual node execution and user interaction handling
   - Edge selector logic (auto, random, choice, start, end)
   - Developer mode debugging capabilities

4. **ButtonGame** (`classes/button_game.py`)
   - Main game loop orchestration and state management
   - Journey tracking and summary generation
   - Production vs developer mode coordination

5. **StoryGraph** (`classes/story_graph.py`)
   - NetworkX-based narrative flow visualization
   - Professional "murky chic" styling with color-coded node types
   - Multiple layout algorithms for different presentation needs

### Data Structure

The game uses three primary data sources from Google Sheets:

#### Edges Dataset
- `source`: Origin node identifier
- `target`: Destination node identifier  
- `outro_text`: Narrative text shown during transition
- `desired`: Boolean indicating optimal (TRUE) vs problematic (FALSE) paths

#### Nodes Dataset
- `node`: Unique node identifier
- `edge_selector`: Transition logic type (auto, random, choice, start, end)
- `title_text`: Node title displayed to player
- `intro_text`: Opening narrative text
- `event_text`: Action/event description
- `pbn`: Node-specific call-to-action text

#### Text Dataset
- `id_text`: Unique text identifier
- `text_type`: Category of text content
- `text_context`: Usage context description
- `text`: Actual text content

## Game Mechanics

### Edge Selector Types

- **auto**: Automatic progression to first available connection
- **random**: Random selection from available connections with outcome feedback
- **choice**: Player selection between multiple options (future feature)
- **start**: Initial game entry point
- **end**: Terminal state with no further progression

### Random Edge Feedback

When nodes have `random` edge selectors, the game provides contextual feedback:
- **edge_good**: Positive outcome text for desired=TRUE transitions
- **edge_bad**: Problematic outcome text for desired=FALSE transitions

This creates narrative variety while reflecting the uncertainty of real data science work.

### Text Formatting and Display

The game implements consistent text wrapping for improved readability:
- **Console Width**: All narrative text is wrapped to 80 characters
- **Journey Summary**: Outro text is properly indented with "� " prefix
- **Consistent Spacing**: Proper spacing between intro, prompt, and outro sections
- **Responsive Layout**: Text adapts to different content lengths automatically

### Game Modes

1. **Production Mode**: Clean gameplay experience without technical details
2. **Developer Mode**: Full debug information including:
   - Current node and edge selector type
   - Available connections and chosen path
   - Desired status of selected transitions
   - Technical debugging information

3. **Single Node Mode**: Development tool for testing individual nodes

## Installation & Setup

### Prerequisites
- Python 3.8+
- uv package manager (recommended) or pip
- Google Sheets API access

### Environment Configuration
Create a `.env` file in the `button_1/` directory with:

```
BUTTON_SHEET_ID=your_google_sheets_id
BUTTON_SHEET_EDGES_GID=edges_tab_gid
BUTTON_SHEET_NODES_GID=nodes_tab_gid  
BUTTON_SHEET_TEXT_GID=text_tab_gid
BUTTON_SHEET_TITLES_GID=titles_tab_gid
```

### Running the Game
```bash
# With uv (recommended)
uv run python -m button_1

# With pip
python -m button_1
```

## Development

### Project Structure
```
button_1/
├── __init__.py              # Main entry point with menu system
├── __main__.py              # Module execution handler
├── classes/                 # Core game components
│   ├── __init__.py         # Package exports
│   ├── button_df.py        # Google Sheets connector
│   ├── button_dat.py       # Data aggregation
│   ├── node_engine.py      # Game logic engine
│   ├── button_game.py      # Main game controller
│   └── story_graph.py      # Visualization system
└── tests/                   # Comprehensive test suite
    ├── __init__.py         # Test package documentation
    ├── test_button_df.py   # Data connector tests
    ├── test_button_dat.py  # Data validation tests
    ├── test_node_engine.py # Game logic tests
    └── test_story_graph.py # Visualization tests
```

### Testing
```bash
# Run all tests
pytest button_1/tests/

# Run specific test file
pytest button_1/tests/test_button_dat.py

# Run with verbose output
pytest button_1/tests/ -v
```

### Adding Content

1. **New Nodes**: Add entries to the nodes Google Sheets tab
2. **New Transitions**: Add entries to the edges Google Sheets tab  
3. **New Text**: Add reusable text to the text Google Sheets tab
4. **No code changes required** - content is loaded dynamically

### Code Style

The codebase follows these principles:
- Comprehensive docstrings for all classes and methods
- Type hints where appropriate
- Descriptive variable and method names
- Separation of concerns between data, logic, and presentation
- Robust error handling with user-friendly messages

## Game Content

### Narrative Theme
The game satirically explores common data science experiences:
- Endless data sourcing and cleaning cycles
- Stakeholder scope creep and changing requirements
- The uncertainty of analytical outcomes
- The frustration of "pressing buttons" without agency

### Current Story Flow
1. **Start Game**: Introduction to the data science world
2. **Welcome**: First day at TechCo as a data scientist
3. **Onboarding**: Corporate introduction and role definition
4. **Initiate Project**: Stakeholder question definition
5. **Source Data**: Data acquisition and preparation
6. **Transform Data**: Data cleaning and preparation
7. **Analyse Data**: Statistical analysis and modeling
8. **Report Analytics**: Results presentation and stakeholder feedback
9. **Decision Maker**: Final review and next steps determination

The narrative includes several potential loops reflecting real data science work:
- Analysis revealing data quality issues requiring transformation rework
- Stakeholder feedback requiring additional data sourcing
- Decision maker scope changes requiring project restart

## Future Enhancements

### Planned Features
1. **Choice Nodes**: Player decision points with multiple options
2. **Conditional Logic**: Branch based on previous choices or random outcomes
3. **Character Variations**: Different job titles and department contexts
4. **Extended Narrative**: Additional story branches and endings
5. **Save/Load**: Game state persistence across sessions

### Technical Improvements
1. **Real Arrow Key Input**: Direct keypress handling without Enter
2. **Rich Text Formatting**: Enhanced display with colors and formatting
3. **Sound Effects**: Audio feedback for transitions and outcomes
4. **Web Interface**: Browser-based gameplay option

## Contributing

The game is designed for easy content contribution:
1. Fork the repository
2. Update Google Sheets content for narrative changes
3. Modify code for new features or bug fixes
4. Add comprehensive tests for any code changes
5. Submit pull requests with clear descriptions

## License

MIT License - feel free to adapt and extend for your own projects.

## Support

For questions, issues, or feature requests, please use the GitHub issue tracker
or contact the development team directly.
"""