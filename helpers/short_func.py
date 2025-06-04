from typing import List, Dict


def combine_hours(hours: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Combine a list of dicts with keys 'opening_time', 'closing_time', 'weekday'
    into a list of dicts with keys 'opening_time', 'closing_time', 'first_day', 'last_day',
    grouping consecutive weekdays that share the same times.
    """
    # Define weekday order
    weekdays_order = [
        'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday',
        'sunday'
    ]

    # Sort input by weekday order
    sorted_hours = sorted(
        hours,
        key=lambda x: weekdays_order.index(x['weekday'])
    )

    combined = []
    # Initialize with the first day
    first = sorted_hours[0]
    current = {
        'opening_time': first['opening_time'].strftime("%H:%M"),
        'closing_time': first['closing_time'].strftime("%H:%M"),
        'first_day': str.title(first['weekday']),
        'last_day': str.title(first['weekday'])
    }

    # Iterate through the rest
    for entry in sorted_hours[1:]:
        if (entry['opening_time'].strftime("%H:%M") == current['opening_time']
                and entry['closing_time'].strftime("%H:%M") == current['closing_time']):
            # Extend the current range

            current['last_day'] = str.title(entry['weekday'])
        else:
            # Save the finished range and start a new one
            combined.append(current)
            current = {
                'opening_time': entry['opening_time'].strftime("%H:%M"),
                'closing_time': entry['closing_time'].strftime("%H:%M"),
                'first_day': str.title(entry['weekday']),
                'last_day': str.title(entry['weekday'])
            }
    # Don't forget to append the final range
    combined.append(current)
    return combined


def format_ranges(ranges: List[Dict[str, str]]) -> List[str]:
    """
    Given the combined ranges, return strings like
    "09:00 - 17:00 (Monday - Friday)".
    """
    formatted = []
    for r in ranges:
        start, end = r['first_day'], r['last_day']
        day_part = f"{start.title()}" if start == end else f"{start.title()} - {end.title()}"
        formatted.append(f"{r['opening_time'].strftime("%H:%M")} - {r['closing_time'].strftime("%H:%M")} ({day_part})")
    return formatted


def nested_getattr(obj, *attrs):
    for attr in attrs:
        obj = getattr(obj, attr, None)
    return obj


def crud(model_name: str, c: bool = True, r: bool = True, u: bool = True, d: bool = True):
    perms = []
    if c: perms.append(f'add_{model_name}')
    if r: perms.append(f'view_{model_name}')
    if u: perms.append(f'change_{model_name}')
    if d: perms.append(f'delete_{model_name}')
    return perms
