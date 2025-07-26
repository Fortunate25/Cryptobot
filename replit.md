# Crypto News Bot

## Overview

This is a Telegram bot that monitors multiple cryptocurrency channels, filters messages based on specific keywords, and forwards relevant content to a target channel. The bot is designed to aggregate crypto-related news and signals from various sources into a single channel while cleaning up unwanted content like unauthorized links and handles.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple single-threaded architecture with two main components:

1. **Keep-alive Service**: A Flask web server that runs in a separate thread to maintain the application's uptime (commonly used for hosting platforms like Replit)
2. **Telegram Bot**: The main application logic using the Telethon library to interact with Telegram's API

## Key Components

### Keep-alive Service (`keep_alive.py`)
- **Purpose**: Maintains application uptime by providing a simple HTTP endpoint
- **Technology**: Flask web framework
- **Architecture**: Runs on a separate thread to avoid blocking the main application
- **Endpoint**: Single route `/` that returns a status message

### Main Bot Logic (`main.py`)
- **Purpose**: Core Telegram bot functionality for monitoring and forwarding messages
- **Technology**: Telethon (Telegram client library)
- **Configuration**: Environment variables for API credentials
- **Session Management**: Persistent session storage using Telethon's session system

### Message Processing
- **Filtering**: Keyword-based filtering system with predefined crypto-related terms
- **Content Cleaning**: Regular expression-based removal of unwanted links and Telegram handles
- **Domain Whitelisting**: Selective preservation of links from approved domains

## Data Flow

1. Bot connects to Telegram using API credentials
2. Monitors specified source channels for new messages
3. Applies keyword filtering to identify relevant content
4. Cleans message content by removing unauthorized links and handles
5. Forwards processed messages to the target channel

## External Dependencies

### Core Libraries
- **Telethon**: Telegram client library for bot functionality
- **Flask**: Web framework for the keep-alive service
- **python-dotenv**: Environment variable management
- **threading**: Built-in Python module for concurrent execution

### Telegram API
- Requires API ID and API Hash from Telegram
- Uses session-based authentication for persistent connections

## Deployment Strategy

### Environment Configuration
- API credentials stored in `.env` file
- Session data persisted locally for authentication
- Host configuration set for external access (0.0.0.0:8080)

### Runtime Architecture
- Multi-threaded execution with Flask server running alongside the main bot
- Designed for cloud hosting platforms that require HTTP endpoints for uptime monitoring
- No database dependencies - all configuration is code-based

### Monitoring Channels
- **Source Channels**: 5 predefined crypto news/signal channels
- **Target Channel**: Single destination channel for aggregated content
- **Content Filtering**: 25+ cryptocurrency-related keywords for relevance filtering

The architecture prioritizes simplicity and reliability, using established libraries and patterns for Telegram bot development while maintaining platform compatibility through the keep-alive mechanism.