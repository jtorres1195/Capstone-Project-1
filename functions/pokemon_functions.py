import requests
import random

def get_total_pokemon():
    pokemon_species_count = requests.get("https://pokeapi.co/api/v2/pokemon-species/")
    if pokemon_species_count.status_code == 200:
        total_pokemon_count = pokemon_species_count.json()["count"]
        return total_pokemon_count
    return 0 # Return a default error in case of an error

def generate_random_index(total_count):
    return random.randint(1, total_count)

def get_random_pokemon_data(random_index):
    random_pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{random_index}/"
    api_response = requests.get(random_pokemon_url)
    if api_response.status_code == 200:
        random_pokemon_data = api_response.json()
        return random_pokemon_data
    return None # Return none in case of error

def catch_pokemon(user_id, pokemon_name, sprite_url):
    captured_pokemon = CapturedPokemon(
        user_id=user_id,
        pokemon_name=pokemon_name,
        pokemon_artwork=sprite_url  # Use the sprite URL here
    )
    db.session.add(captured_pokemon)
    db.session.commit()

def get_captured_pokemon(user_id):
    captured_pokemon = CapturedPokemon.query.filter_by(user_id=user_id).all()
    return captured_pokemon

def get_all_pokemon():
    all_pokemon = []
    offset = 0
    limit = 1200

    while True:
        url = f"https://pokeapi.co/api/v2/pokemon/?offset={offset}&limit={limit}"
        apiResponse = requests.get(url)
        pokedata = apiResponse.json()

        results = pokedata.get('results', [])
        all_pokemon.extend(pokemon['name'].capitalize() for pokemon in results)

        if not results:
            break

        offset += limit

    return all_pokemon

def fetch_pokemon_data(start_idx, end_idx):
    api_url = f"https://pokeapi.co/api/v2/pokemon/?limit={end_idx}&offset={start_idx}"
    api_response = requests.get(api_url)

    if api_response.status_code == 200:
        api_data = api_response.json()
        pokemon_list = api_data['results']
        pokemon_data = []

        for pokemon in pokemon_list:
            pokemon_name = pokemon['name']
            sprite_url = fetch_sprite_urls(pokemon_name)
            pokemon_data.append({'name': pokemon_name, 'sprite_url':sprite_url})

        return pokemon_data
    else:
        return []
    
def fetch_sprite_urls(pokemon_name):
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    api_response = requests.get(api_url)

    if api_response.status_code == 200:
        pokemon_data = api_response.json()
        sprite_url = pokemon_data['sprites']['front_default']
        return sprite_url
    else:
        return None