from flask import Flask, request, render_template, redirect, session, flash, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from functions.pokemon_functions import *
from functions.user_functions import *

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y"
    
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jtorr:JT@localhost/pokemon_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_DEBUG'] = True

db.init_app(app)

TOTAL_POKEMON_COUNT = 1118
ITEMS_PER_PAGE = 50

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
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Incorrect Username or Password. Please try again')

    return render_template('login.html')

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

@app.route('/profile', endpoint='profile')
def user_profile():
    if 'username' in session:
        username = session['username']
        user = get_user_by_username(username)
        
        if user:
            user_profile = {
                'username': user.username
            }
            return render_template('profile.html', user_profile=user_profile)

    flash('Please log in to access your profile', 'warning')
    return redirect(url_for('login'))

@app.route('/list-of-pokemon', methods=['GET'])
def list_of_pokemon():
    ITEMS_PER_PAGE = 50 
    page = int(request.args.get('page', 1))

    total_pokemon_count = get_total_pokemon()
    total_pages = (total_pokemon_count + ITEMS_PER_PAGE - 1)// ITEMS_PER_PAGE

    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = page * ITEMS_PER_PAGE

    pokemon_data = fetch_pokemon_data(start_idx, end_idx)

    return render_template('list-of-pokemon.html', pokemon_data=pokemon_data, page=page, total_pages=total_pages)

@app.route('/catch-pokemon', methods=['POST'])
def catch_pokemon_route():
    if 'username' in session:
        username = session['username']
        pokemon_name = request.form.get('pokemon_name')

        user_id = get_user_id_by_username(username)
        if user_id is not None:
            sprite_url = fetch_sprite_urls(pokemon_name)  # Fetch the sprite URL
            catch_pokemon(user_id, pokemon_name, sprite_url)  # Pass the sprite URL to catch_pokemon
            return jsonify({'status': 'success', 'pokemon_name': pokemon_name})
        return redirect('/profile')
    return redirect('/login')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')

@app.route('/submit-suggestion', methods=['POST'])
def submit_suggestion():
    if request.method == 'POST':
        suggestion_text = request.form.get('suggestion')

        # Save the suggestion to your database or a file, or take any other desired action.

        flash('Thank you for your suggestion! We appreciate your feedback.')
        return redirect('/suggestions')

    return redirect('/suggestions')

if __name__ == "__main__":
    app.run(debug=True)