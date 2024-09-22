# Cron Expression Parser

This Python script parses a cron expression, expanding the various time fields (minute, hour, day of the month, month, and day of the week) into their corresponding ranges of values. It also prints the parsed values in a formatted table and includes error handling to ensure valid cron expressions.

## Features
- Parses a cron expression into its time fields.
- Expands ranges, steps, and lists in each time field (e.g., `*/15`, `1-5`, and `1,3`).
- Prints the parsed values in a formatted output.
- Validates the input to ensure the cron expression has the correct number of fields.
- Command field is displayed as the last field in the output.

## Files
- `cron_parser.py`: The main script that processes and prints the cron expression.

## Prerequisites
- Python 3.x

## Usage

You can run the script by passing a cron expression as a command-line argument.

```bash
python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```

If no argument is passed, the script raises an error:
ValueError: Need a cron expression as an argument

### Example:
```bash
python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find" 
```

### Output:
```
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

### Running the Tests

```bash
python -m unittest discover
```