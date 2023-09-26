import requests
import argparse
import json

def get_pokemon_name(pokemon_id):
    """Query the endpoint and retrieve the pokemon name for the given Pokémon ID."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)

    # Ensure successful response
    if response.status_code != 200:
        print(f"Failed to retrieve data for Pokémon ID: {pokemon_id}")
        return None

    data = response.json()
    return data["name"]

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Retrieve Pokémon ability names by ID from a file.')
    parser.add_argument('file_path', type=str, help='Path to the text file with Pokémon ID numbers, one per line.')

    args = parser.parse_args()

    # Read the file and process each Pokémon ID
    with open(args.file_path, 'r') as file:
        for line in file:
            pokemon_id = line.strip()
            name = get_pokemon_name(pokemon_id)
            if name:
                print(f"{pokemon_id}, {name}")

if __name__ == "__main__":
    main()
