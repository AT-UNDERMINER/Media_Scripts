"""
TV Show Folder Structure Creator for Plex
"""

import os


def main():
    """Create a TV show folder with season subfolders in a user-specified location."""
    print("TV Show Folder Creator for Plex")

    base_directory = input("Enter the full path where you want the show folder created: ").strip()
    show_name = input("Enter the TV show name (e.g., NCIS): ").strip()
    show_year = input("Enter the show start year (e.g., 2003): ").strip()

    # Create the main show folder, e.g., "NCIS (2003)"
    show_folder_name = f"{show_name} ({show_year})"
    show_folder_path = os.path.join(base_directory, show_folder_name)

    try:
        os.makedirs(show_folder_path, exist_ok=True)
        print(f"Created show folder: {show_folder_path}")
    except OSError as error:
        print(f"Error creating show folder: {error}")
        return

    # Get season range
    start_season, end_season = get_season_range()

    digit_count = max(len(str(start_season)), len(str(end_season)))

    for season in range(start_season, end_season + 1):
        season_folder_name = f"Season {season:0{digit_count}}"
        season_folder_path = os.path.join(show_folder_path, season_folder_name)
        try:
            os.makedirs(season_folder_path, exist_ok=True)
            print(f"  Created season folder: {season_folder_path}")
        except OSError as error:
            print(f"  Error creating season folder '{season_folder_name}': {error}")


def get_season_range():
    """Prompt the user for a valid season range and return it as two integers."""
    while True:
        season_range_input = input("Enter the season range (e.g., 3-13): ").strip()
        try:
            parts = season_range_input.split('-')
            if len(parts) != 2:
                raise ValueError("Please use the format start-end, e.g., 1-5.")
            start = int(parts[0])
            end = int(parts[1])
            if start <= 0 or end <= 0 or start > end:
                raise ValueError("Invalid range. Start must be <= end, and both > 0.")
            return start, end
        except ValueError as e:
            print(f"Invalid input: {e}")


main()
