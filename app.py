from flask import Flask, request, render_template, redirect, session, flash, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import random
import bcrypt

db = SQLAlchemy

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y"
    
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jtorr:JT@localhost/poke_roulette_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_DEBUG'] = True


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

def get_user_id_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.user_id
    return None

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def catch_pokemon(user_id, pokemon_name):
    captured_pokemon = CapturedPokemon(user_id=user_id, pokemon_name=pokemon_name, pokemon_artwork=pokemon_artwork)
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

@app.route("/")
def home():
    total_pokemon_count = get_total_pokemon()
    random_index = generate_random_index(total_pokemon_count)
    random_pokemon_data = get_random_pokemon_data(random_index)

    return render_template("home.html", random_pokemon=random_pokemon_data)

@app.route("/generate-pokemon", methods=["GET"])
def generate_random_pokemon():
    total_pokemon_count = get_total_pokemon()
    random_index = generate_random_index(total_pokemon_count)
    random_pokemon_data = get_random_pokemon_data(random_index)

    return jsonify(random_pokemon_data)

@app.route("/login", methods=["GET" ,"POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and verify_password(password, user.password):
            session['username'] = username

        return redirect('/profile')
        
    return "Invalid Username or Password"

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = hash_password(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    
    return render_template('signup.html')

@app.route('/my-profile')
def profile():
    return render_template('profile.html')

@app.route('/list-of-pokemon')
def list_of_pokemon():
    available_pokemon = get_all_pokemon()
    return render_template('list-of-pokemon.html', available_pokemon=available_pokemon)

@app.route('/save-pokemon', methods=['POST'])
def save_pokemon():
    if 'username' in session:
        username = session['username']
        pokemon_name = request.form.get('pokemon_name')

        user_id = get_user_id_by_username(username)
        if user_id is not None:
            catch_pokemon(user_id, pokemon_name)
            return jsonify({'status': 'success', 'pokemon_name': pokemon_name})
        return redirect('/profile')
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)