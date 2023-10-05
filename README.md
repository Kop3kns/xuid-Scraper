# Xuid Scraper

## Overview
The Xuid Scraper is designed to search and iterate over XUIDs (Xbox User IDs). The program will continuously run until manually terminated.

**Note**: Due to debugging print statements, it's recommended to use a terminal that automatically clears text to prevent excessive memory consumption. Recent testing has shown the script can scrape approximately 4.3 million XUIDs in one hour.

For more detailed documentation, refer to the official [Microsoft GDK Documentation](https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/reference/live/gc-reference-live-toc).

## Token Retrieval

### Prerequisites
1. Install [Fiddler Classic](https://www.telerik.com/download/fiddler).
2. Set up Fiddler to decrypt HTTPS traffic:

   - Exclude all apps from the app container.
   - Turn on HTTPS decryption in settings.

### Steps
1. Launch the Xbox app.
2. Set Fiddler's capture location to the Xbox app window.
3. Open your Xbox profile within the app.
4. Once the network packets have been transmitted, inspect the request headers in Fiddler.
5. Locate the "Authorization" header. Your token will appear to its right. It will start with "XBL3.0" ensure you copy that prefix as well.
