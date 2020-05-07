# RS forums dumper

Archive your favourite RSForums threads

## Installation

Clone the project, go to the project root directory and run
```
pip install .
```

## Usage
```bash
$rsforumsdump --help
usage: rsforumsdump [-h] [-q] [-o OUTFILE] [-w WORKERS] thread

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
```

## Output
```json
{
  "thread": "https://secure.runescape.com/m=forum/forums?181,182,686,66098403",
  "qfc": "181-182-686-66098403",
  "pagecount": 6,
  "postcount": 55,
  "posts": [
    {
      "id": 0,
      "page": 1,
      "poster": "Chief%A0Elf",
      "message": "Post your favourite moderator responses!\n\nModerators include Forum, Jagex and Local Mods.\n\nFound a funny, witty, clever, inspiring, mind-blowing, meaningful, awesome or a post that made you feel all warm and fuzzy inside? Share it with us!",
      "created": "2019-05-01T20:11:18",
      "lastedited": null
    },
    ...
  ]
}
```

Enjoy!
