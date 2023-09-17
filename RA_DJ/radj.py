#!/usr/bin/env python3
import time
import requests
import json
import argparse
import csv

# Constants for the request
URL = 'https://ra.co/graphql'
HEADERS = {
    'Content-Type': 'application/json',
    'Referer' : 'https://www.google.com',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

# Load the GraphQL query from a file
def load_query(filename):
    with open(filename, 'r') as file:
        return file.read()

# Load the list of artists from a file
def load_artist_list(filename):
    with open(filename, 'r') as file:
        return [str(line.strip()) for line in file if line.strip()]

# Class to fetch events based on location, date and artists
class EventFetcher:

    # Initialize the object with given parameters
    def __init__(self, area, start, end, artist_list=None):
        self.area = area
        self.start = start
        self.end = end
        self.artist_list = artist_list
        self.payload = self.generate_payload(area, start, end, artist_list)
        self.events = {}

    # Generate the payload for the GraphQL request based on the given criteria
    @staticmethod
    def generate_payload(area, start, end, artist_list):
        if artist_list == None:
            query = load_query("query_date.graphql")
            payload = {
                "operationName" : "GET_DATES",
                "variables" : {
                    "filters" : {
                        "areas" : {"eq" : 34},
                        "listingDate": {
                            "gte" : start,
                            "lte" : end 
                        }
                    },
                    "pageSize" : 20,
                    "page" : 1
                },
                "query" : query
            }
        else:
            query = load_query("query_artist.graphql")
            daterange = "{\"gte\":\"" + start + "\"}"
            payload = {
                "operationName" : "GET_ARTIST",
                "variables" : {
                    "id" : artist_list[0],
                    "daterange" : daterange,
                    "pageSize" : 20,
                    "page" : 1
                },
                "query" : query
            }
        return payload

    # Get events on a particular page and possibly for a particular artist
    def get_events(self, page, artist_id=None):

        self.payload["variables"]["page"] = page
        if artist_id: self.payload["variables"]["id"] = artist_id

        response = requests.post(URL, headers=HEADERS, json=self.payload)

        try:
            response.raise_for_status()
            data = response.json()
        except (requests.exceptions.RequestException, ValueError):
            print(f"Error: {response.status_code}")
            print(response.text)
            return []


        if self.artist_list: 
            return data["data"]["listing"]
        else:
            return data["data"]["eventListings"]

    # Fetch all events that match the criteria
    def fetch_all_events(self):
        first_page = self.get_events(1)

        with open("response.json", "w") as outfile:
            json.dump(first_page, outfile, indent=4)

        total_results = first_page["totalResults"]
        all_events = first_page["data"]
        page = 1
        while page*20 < total_results:
            page += 1
            all_events.extend(self.get_events(page)["data"])
            time.sleep(1)
        for event in all_events:
            if self.artist_list: 
                if event["startTime"] <= self.end:
                    self.events[event["id"]] = event
            else:
                self.events[event["event"]["id"]] = event["event"]

    # Fetch events for each artist or all events if no artists given
    def fetch_all_artists(self):
        all_events = {}
        if self.artist_list:
            for artist_id in self.artist_list:
                self.payload["variables"]["id"] = artist_id
                artist_events = self.fetch_all_events()
        else:
            self.fetch_all_events()

    # Print the events to the terminal.
    def print_events(self):
        for id, event in (item for item in sorted(self.events.items(), key=lambda item: item[1]["startTime"]) if item[1]["area"]["id"] == str(self.area)):
            print (f"{event['startTime']}...{event['endTime']} ------------------- {event['title']} @@@@@@@@@@@@@@@@@@@@@@@@@ {event['venue']['name']}..........................ra.co{event['contentUrl']}")

            

def main():
    """
    Example arguments:
    start = "2023-09-15T00:00:00.000Z"
    end = "2023-09-16T23:59:59.999Z"
    area = 34
    artist_list = ["17916", "51198", "67103"]
    """

    # Argument Parsing
    parser = argparse.ArgumentParser(description="Fetch events based on given criteria.")
    parser.add_argument('--start', required=True, help="Start time in format 'YYYY-MM-DDTHH:MM:SS.SSSZ'")
    parser.add_argument('--end', required=True, help="End time in format 'YYYY-MM-DDTHH:MM:SS.SSSZ'")
    parser.add_argument('--area', type=int, required=True, help="Area code as integer")
    parser.add_argument('--artist-file', default=None, help="File containing list of artist IDs, one per line")
    
    args = parser.parse_args()
    
    # Get arguments
    start = args.start
    end = args.end
    area = args.area
    artist_list = None

    # If artist file is provided, load it
    if args.artist_file:
        artist_list = load_artist_list(args.artist_file)

    # Main logic
    event_fetcher = EventFetcher(area, start, end, artist_list) 
    event_fetcher.fetch_all_artists()

    with open("response.json", "w") as outfile:
        json.dump(sorted(event_fetcher.events.items()), outfile, indent=4)

    event_fetcher.print_events()

if __name__ == "__main__":
    main()

