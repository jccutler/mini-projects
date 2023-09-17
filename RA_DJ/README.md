# EventFetcher for RA.co

EventFetcher is a Python script designed to fetch events from RA.co based on given criteria, such as date range, area, and artist list. The script interacts with the RA.co GraphQL API to retrieve the relevant event information and provides users with detailed listings.

## Features

- **Area-based Event Retrieval**: Fetch events from specific areas during a defined date range.
- **Artist-focused Event Retrieval**: Target events featuring specific artists using their artist IDs.
- **Flexible Output**: Current output is provided in a readable text format, with each event's start and end times, title, venue, and content URL.

## Usage

To fetch events, use the following command format:

python radj.py --start START_DATE --end END_DATE --area AREA_CODE [--artist-file ARTIST_FILE]

Replace `START_DATE`, `END_DATE`, and `AREA_CODE` with your desired criteria. If you have a list of artist IDs, specify the file path with `--artist-file`.

For more details on arguments, run:

python radj.py --help

## Planned Additional Features

- **Improved Output Formatting**: In future iterations, the script will output an HTML file that offers a more visually appealing display of event details. Each event listing will also have clickable links for ease of access.
  
- **Artist ID Helper Script**: A supplementary script will be added to scrape artist IDs directly from their RA.co pages, eliminating the need for users to manually source these IDs.
