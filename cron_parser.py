import sys

def expand_range(value, min_value, max_value):
    # Handle the '*' which means "all values"
    if value == '*':
        return list(range(min_value, max_value + 1))
    
    result = []
    
    # Handle step values like */15
    if value.startswith("*/"):
        step = int(value[2:])
        result = list(range(min_value, max_value + 1, step))
    
    # Handle ranges and lists like 1-5, 3
    elif "," in value or "-" in value:
        parts = value.split(',')
        for part in parts:
            if '-' in part:
                start, end = part.split('-')
                result += list(range(int(start), int(end) + 1))
            else:
                result.append(int(part))
    # Handle single numbers like 0
    else:
        result = [int(value)]
    
    return sorted(result)

def parse_cron_expression(cron_expression):
    # returns a dictionary with the parsed cron expression
    fields = cron_expression.split()
    
    if len(fields) < 6:
        raise ValueError("Invalid cron expression, expected 5 time fields and 1 command")

    minute = expand_range(fields[0], 0, 59)
    hour = expand_range(fields[1], 0, 23)
    day_of_month = expand_range(fields[2], 1, 31)
    month = expand_range(fields[3], 1, 12)
    day_of_week = expand_range(fields[4], 0, 6)
    command = fields[5]
    
    return {
        'minute': minute,
        'hour': hour,
        'day of month': day_of_month,
        'month': month,
        'day of week': day_of_week,
        'command': command
    }

def format_output(parsed_cron):
    # build table with 14 character width for each field
    print(f"{'minute':<14}{' '.join(map(str, parsed_cron['minute']))}")
    print(f"{'hour':<14}{' '.join(map(str, parsed_cron['hour']))}")
    print(f"{'day of month':<14}{' '.join(map(str, parsed_cron['day of month']))}")
    print(f"{'month':<14}{' '.join(map(str, parsed_cron['month']))}")
    print(f"{'day of week':<14}{' '.join(map(str, parsed_cron['day of week']))}")
    print(f"{'command':<14}{parsed_cron['command']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Need a cron expression as an argument")
    
    cron_expression = sys.argv[1]
    try:
        parsed_cron = parse_cron_expression(cron_expression)
        format_output(parsed_cron)
    except ValueError as e:
        print(f"Error parsing cron expression: {e}")