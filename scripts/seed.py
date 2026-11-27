import json
import urllib.request

API = "http://localhost:8000/recommendation/"

# (title, category, status, note, added_on)
SAMPLES = [
    # Books
    ("Cosmos", "Book", "Done", "Carl Sagan", "2026-08-09"),
    ("The Structure of Scientific Revolutions", "Book", "ToTry", "Thomas Kuhn", "2026-09-08"),
    ("A Brief History of Time", "Book", "Dropped", "Stephen Hawking", "2026-10-15"),
    # Articles
    ("Attention Is All You Need", "Article", "Done", "Vaswani et al., 2017", "2026-09-14"),
    ("A Mathematical Theory of Communication", "Article", "Done", "Claude Shannon, 1948", "2026-09-21"),
    ("Why Most Published Research Findings Are False", "Article", "Done", "John Ioannidis, 2005", "2026-09-28"),
    ("Computing Machinery and Intelligence", "Article", "Done", "Alan Turing, 1950", "2026-10-05"),
    ("Judgment under Uncertainty: Heuristics and Biases", "Article", "Done", "Tversky and Kahneman, 1974", "2026-10-12"),
    ("The Tragedy of the Commons", "Article", "ToTry", "Garrett Hardin, 1968", "2026-10-19"),
    # Other
    ("Khan Academy", "Other", "Done", "Free courses in mathematics and science", "2026-10-10"),
    # Podcasts
    ("Nature Podcast", "Podcast", "ToTry", "Weekly research news", "2026-08-14"),
    ("Science Magazine Podcast", "Podcast", "Done", "", "2026-10-30"),
    # Places
    ("CERN Science Gateway", "Place", "ToTry", "Exhibitions and visitor tours", "2026-10-06"),
    ("Natural History Museum, London", "Place", "Done", "", "2026-10-15"),
    # Apps
    ("Duolingo", "App", "Done", "Language learning", "2026-09-28"),
    # Recipes
    ("Palak paneer", "Recipe", "Done", "Indian spinach and cheese curry", "2026-10-13"),
    ("Okonomiyaki", "Recipe", "ToTry", "Japanese savoury pancake", "2026-10-15"),
    # Restaurants
    ("Mosconi", "Restaurant", "Done", "Luxembourg City", "2026-09-04"),
    ("Clairefontaine", "Restaurant", "ToTry", "Luxembourg City", "2026-09-17"),
    ("Osteria Francescana", "Restaurant", "ToTry", "Modena", "2026-10-10"),
    # Film
    ("Hidden Figures", "Film", "Done", "", "2026-10-07"),
    # Apps
    ("Notion", "App", "ToTry", "Notes and planning", "2026-10-16"),
    # Books
    ("Thinking, Fast and Slow", "Book", "Done", "Daniel Kahneman", "2026-10-21"),
    # Podcasts
    ("In Our Time", "Podcast", "ToTry", "BBC, history of ideas and science", "2026-11-08"),
    # Product
    ("Kindle Paperwhite", "Product", "ToTry", "E-reader for books and papers", "2026-11-19"),
    # Places
    ("Deutsches Museum, Munich", "Place", "ToTry", "", "2026-11-25"),
]

for title, category, status, note, added_on in SAMPLES:
    body = {"title": title, "category": category, "status": status,
            "added_on": added_on}
    if note:
        body["note"] = note
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(resp.status, title)
    except Exception as exc:
        print("FAILED", title, exc)