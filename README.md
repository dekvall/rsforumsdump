# RS forums dumper

Archive your favourite RSForums threads

## Installation

Clone the project, go to the project root directory and run
```
pip install .
```

## Usage
```
$rsforumsdump --help
usage: rsforumsdump [-h] [-q] [-o OUTFILE] [-w WORKERS] [-i INDENT] thread

dump an RSforums thread to json

positional arguments:
  thread                the forums url or qfc to dump

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           do not display output
  -o OUTFILE, --output-file OUTFILE
                        output result to a file
  -w WORKERS, --workers WORKERS
                        set the amount of workers to fetch webpages
  -i INDENT, --indent INDENT
                        set the indentation of the json output
```

## Output
```json
{
  "thread": "https://secure.runescape.com/m=forum/forums?14,15,732,66161086",
  "qfc": "14-15-732-66161086",
  "pagecount": 1,
  "postcount": 5,
  "posts": [
    {
      "id": 0,
      "page": 1,
      "poster": "I%A0IS%A0SPAEROR",
      "message": "Simple question, though less simple to answer. Does anyone know how big the RuneScape map is on a human scale?\n\nI find the idea of invasions taking ages kind of humorous just because the map itself seems like it's no bigger than the city of Washington, DC or so. But what are your thoughts? I don't really know how to accurately test this.",
      "created": "2020-05-19T19:17:15",
      "lastedited": null
    },
    {
      "id": 1,
      "page": 1,
      "poster": "Tuffty",
      "message": "If you look at the whole map and split into 1 inch squares.\n\nThen find something you might know the size of and see if it fits into the square then you can work out how big that 1 inch square is and then count them all up and you have a rough size.\n\nGood luck though.",
      "created": "2020-05-19T19:21:40",
      "lastedited": null
    },
    {
      "id": 2,
      "page": 1,
      "poster": "Kings%A0Abbot",
      "message": "Every game tile is a square meter (if I recall correctly).\nThis page shows how big a tile is compared to the coordinate system, and shows how big the map is approximately using the coordinate system: https://runescape.wiki/w/Treasure_Trails/Guide/Coordinates\n\nSome simple math will show the answer.\nIt's gonna be small.\nThis theory covers the difference between the \"lore\" and what the game shows: https://runescape.wiki/w/Scale_theory",
      "created": "2020-05-19T19:47:24",
      "lastedited": null
    },
    {
      "id": 3,
      "page": 1,
      "poster": "I%A0IS%A0SPAEROR",
      "message": "Kings\u00a0Abbot said:\nEvery game tile is a square meter (if I recall correctly).\nThis page shows how big a tile is compared to the coordinate system, and shows how big the map is approximately using the coordinate system: https://runescape.wiki/w/Treasure_Trails/Guide/Coordinates\n\nSome simple math will show the answer.\nIt's gonna be small.\nThis theory covers the difference between the \"lore\" and what the game shows: https://runescape.wiki/w/Scale_theory\n\nThat scale theory page is really interesting!\n\nI'll calculate how big the map is in literal terms though and come back to let you guys know.",
      "created": "2020-05-20T22:12:40",
      "lastedited": null
    },
    {
      "id": 4,
      "page": 1,
      "poster": "I%A0IS%A0SPAEROR",
      "message": "Alright guys, so I did calculations assuming every square is 1 square meter. Not including anachronia, the map from 10 degrees W (western edge of Tirannwn) to 40 degrees E (eastern edge of morytania) is 5.625 kilometers (using the American decimal system). From north (wilderness) to south (southern edge of menaphos) the continent is 4.8375 kilometers. This means the square that encompasses all these dimensions is 27.21 square kilometers. Add another 10 or so square kilometers for Anachronia, and another 10 or so for Great Kourend (if we're including OSRS).\n\nSo in total, the map is about 47 square kilometers, or about a third of DC.\n\nFor comparison, google maps seems to suggest that Washington, DC is about 160 square kilometers. 10x10 square miles. (edit: wikipedia said 3,644.2 for some reason? I think it was extending way beyond the district) The state of maryland is 25,314 square kilometers, meaning the map of RS is 1/539th of the size of maryland.\n\nSo we're definitely gonna have to be pulling some serious scale theory to get the lore to work, but the map is still pretty sizeable. I'd say about a week to invade in real life if taken literally, maybe a month to secure all dissension given the widespread diversity of ideologies, inhabitants, and obstacles.",
      "created": "2020-05-21T03:35:08",
      "lastedited": "2020-05-21T03:54:39"
    }
  ]
}

```

Enjoy!
