import sys

def process_log_file(log_file_path):
    sessions = {}
    min_start_time = None
    max_end_time = None

    with open(log_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 4:
                continue  # Skip invalid lines
            timestamp, username, action = parts[:3]
            if action == 'Start':
                sessions[username] = sessions.get(username, [])
                sessions[username].append([timestamp, None])
            elif action == 'End':
                if username in sessions and sessions[username]:
                    sessions[username][-1][1] = timestamp

            # Update min_start_time and max_end_time
            if min_start_time is None or timestamp < min_start_time:
                min_start_time = timestamp
            if max_end_time is None or timestamp > max_end_time:
                max_end_time = timestamp

    # Set start time for sessions with no matching End
    for username in sessions:
        for session in sessions[username]:
            if session[1] is None:
                session[1] = max_end_time

    # Set end time for sessions with no matching Start
    for username in sessions:
        for session in sessions[username]:
            if session[0] is None:
                session[0] = min_start_time

    # Calculate total duration for each user
    user_sessions = {}
    for username in sessions:
        total_duration = 0
        for session in sessions[username]:
            start_time = session[0]
            end_time = session[1]
            start_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(':'))))
            end_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(end_time.split(':'))))
            total_duration += end_seconds - start_seconds
        user_sessions[username] = total_duration

    # Print report
    for username, total_duration in user_sessions.items():
        num_sessions = len(sessions[username])
        print(f"{username} {num_sessions} {total_duration}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    log_file_path = sys.argv[1]
    process_log_file(log_file_path)
