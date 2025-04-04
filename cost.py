import datetime


def sum_recent_costs(filename, days=30):
    total_cost = 0.0

    # Use UTC-aware current time
    now = datetime.datetime.now(datetime.timezone.utc)
    # Compute threshold: 30 days ago from now
    threshold = now - datetime.timedelta(days=days)

    # Open the file and process each line
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            # The line is assumed to have a datetime string and a cost separated by whitespace
            try:
                dt_str, cost_str = line.split()
            except ValueError:
                print(f"Skipping malformed line: {line}")
                continue

            # Parse datetime string; the format assumes the "Z" which means UTC.
            try:
                dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
                # Mark the datetime as UTC
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            except ValueError as ve:
                print(f"Error parsing date {dt_str}: {ve}")
                continue

            # Check if this date is within the last 30 days.
            if dt >= threshold:
                try:
                    cost = float(cost_str)
                    total_cost += cost
                except ValueError:
                    print(f"Invalid cost value on line: {line}")
                    continue

    return total_cost


if __name__ == "__main__":
    filename = "../consultant-users/420736452265-cost.txt"
    total = sum_recent_costs(filename, 1)
    print("Total cost from the last 30 days:", total)
