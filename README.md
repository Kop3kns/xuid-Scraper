# Xuid Scraper
Scrapes xuids though group posts, searches scraped xuids for friend xuids, add function is now fully functional (maximum friends on xbox is 1000).

if you want to remove this repo go report it to github not me, i dont have an email at the moment 

due to debugging print statements this program will use high ammounts of memory if you dont use a terminal that clears text

after testing the scraper with no api request limit, you can expect a 500k XUID database within 4 hours. There are many uses for this data such as visualization of the types of games certain groups play. If you want the docs for the use cases it will be included here https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/reference/live/gc-reference-live-toc

# Out of service
Upon trying to grab my xbox live token it seems they have patched the method of capturing the XBL3.0 token using fiddler. The xbox app stops incoming and outcoming packets from being sent with this new method (This may be why they depriciated the console companion app). I do have an idea on how to grab the token, but until I find a viable workaround to the problem, the tool will not work.

# Potential fix
Looking at another repository, there seems to be a way to grab the xbl3.0 token through hex by reading through the memory of the xbox app. Due to this, it may require me to completely change the programming language the scraper is written in. I will see if hxd works, and may change the program so it works without the group post scrape.
