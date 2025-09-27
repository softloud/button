# 🎮 Press A Button Now - Docker Setup

Run the satirical data science adventure game in a containerized environment for easy setup and collaboration.

## 🚀 Quick Start

### Prerequisites
- Docker installed on your system ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose (usually comes with Docker Desktop)
- Google Sheets API credentials (see setup below)

### 1. Get the Game Files
```bash
git clone <repository-url>
cd button
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root with your Google Sheets credentials:

```env
BUTTON_SHEET_ID=your_google_sheets_document_id
BUTTON_SHEET_EDGES_GID=edges_sheet_tab_gid
BUTTON_SHEET_NODES_GID=nodes_sheet_tab_gid
BUTTON_SHEET_TEXT_GID=text_sheet_tab_gid
BUTTON_SHEET_TITLES_GID=titles_sheet_tab_gid
```

### 3. Run the Game

#### Option A: Using the Quick Start Script
**Linux/macOS:**
```bash
./run-docker.sh
```

**Windows:**
```cmd
run-docker.bat
```

#### Option B: Using Docker Compose
```bash
docker-compose up --build
```

#### Option C: Using Docker Directly
```bash
# Build the image
docker build -t press-a-button-now .

# Run the game
docker run --rm -it --env-file .env press-a-button-now
```

## 🎯 Game Controls

- **Arrow Keys**: Navigate through the game
- **Right Arrow (→)**: Progress to next node
- **Ctrl+C**: Exit the game

## 🏗️ Development Setup

### Running Tests in Docker
```bash
# Build and run tests
docker run --rm --env-file .env press-a-button-now python -m pytest button_1/tests/ -v
```

### Development Mode
```bash
# Run with developer mode enabled
docker run --rm -it --env-file .env press-a-button-now python -c "from button_1 import ButtonGame; ButtonGame(developer_mode=True).play_full_game()"
```

### Access Container Shell
```bash
docker run --rm -it --env-file .env --entrypoint /bin/bash press-a-button-now
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BUTTON_SHEET_ID` | Google Sheets document ID | ✅ Yes |
| `BUTTON_SHEET_EDGES_GID` | Sheet tab ID for edges data | ✅ Yes |
| `BUTTON_SHEET_NODES_GID` | Sheet tab ID for nodes data | ✅ Yes |
| `BUTTON_SHEET_TEXT_GID` | Sheet tab ID for text data | ✅ Yes |
| `BUTTON_SHEET_TITLES_GID` | Sheet tab ID for titles data | ✅ Yes |

### Getting Google Sheets Credentials

1. Open your Google Sheets document
2. Copy the document ID from the URL: `https://docs.google.com/spreadsheets/d/{DOCUMENT_ID}/edit`
3. For each sheet tab, get the GID from the URL when viewing that tab: `#gid={SHEET_GID}`

## 🐳 Docker Details

### Image Information
- **Base Image**: `python:3.12-slim`
- **Size**: ~200MB (optimized for size)
- **User**: Runs as non-root user `gameuser` for security
- **Dependencies**: All Python packages pre-installed

### Container Features
- ✅ Interactive terminal support (TTY)
- ✅ Environment variable configuration
- ✅ Volume support for persistent data
- ✅ Non-root user for security
- ✅ Optimized layer caching for fast rebuilds

### Volume Mounts
```bash
# Optional: Mount local directory for development
docker run --rm -it \
    --env-file .env \
    -v $(pwd)/button_1:/app/button_1 \
    press-a-button-now
```

## 🤝 For Collaborators

### Simple Setup
1. Make sure Docker is installed
2. Get the `.env` file with credentials (ask maintainer)
3. Run: `./run-docker.sh` (Linux/Mac) or `run-docker.bat` (Windows)
4. Enjoy the game! 🎮

### No Python Installation Required
The Docker container includes everything needed:
- Python 3.12
- All game dependencies
- System libraries (graphviz, etc.)
- Pre-configured environment

## 🐛 Troubleshooting

### Common Issues

**"docker: command not found"**
- Install Docker from [docker.com](https://docs.docker.com/get-docker/)

**"Permission denied" on Linux**
- Add your user to docker group: `sudo usermod -aG docker $USER`
- Log out and back in

**"Cannot connect to Google Sheets"**
- Check your `.env` file has correct credentials
- Ensure the Google Sheet is publicly readable or you have API access

**"Game controls not responding"**
- Make sure you're running with `-it` flags for interactive mode
- Try using Docker Desktop terminal instead of WSL on Windows

### Getting Help
- Check container logs: `docker logs button-game-session`
- Run container shell: `docker run --rm -it --entrypoint /bin/bash press-a-button-now`
- Test connection: `docker run --rm --env-file .env press-a-button-now python -c "from button_1.classes.button_df import ButtonDf; print('✅ Connection works!')"`

---

**Happy Gaming!** 🎮✨