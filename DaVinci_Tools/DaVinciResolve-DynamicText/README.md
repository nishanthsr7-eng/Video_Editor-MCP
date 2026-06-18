# DaVinci Resolve Dynamic Text

A proof-of-concept for driving DaVinci Resolve title templates with external data at runtime, using Fusion macros on the Edit page.

## How It Works

DaVinci Resolve allows Fusion macros to be used as title templates on the Edit page. The macro's text fields are plain strings — this tool replaces those strings with live data before the template is loaded into Resolve, enabling fully dynamic lower thirds without touching the timeline manually.

## Features

- **Date/Time Stamp** — Injects the current date and time into a Fusion title macro. Click once before launching Resolve; the macro updates with the current timestamp each time you click.
- **RSS Ticker** — Pulls a live RSS feed and formats each entry as a bottom-of-screen crawl. Useful for news tickers, sports scores, or any regularly updating text feed.

**Note:** Resolve loads title templates into memory once at startup. After the initial click you can refresh the data while Resolve is running — the text content of templates already dropped on the timeline stays frozen (as expected), but new instances will pick up the latest data.

## Requirements

- DaVinci Resolve 15 or later
- Python 3.x

## Usage

1. Run the app once **before** launching DaVinci Resolve to populate the Fusion macro files.
2. Open Resolve — the dynamic titles will appear in your titles list.
3. Drop a title onto the timeline; click the app buttons to update the data source as needed.
4. Drag new instances onto the timeline to pick up refreshed content.
