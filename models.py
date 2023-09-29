"""Models for Pokemon Roulette."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Pokemon(db.Model):
    pokemon_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    evolution_chain_id = db.Column(db.Integer, db.ForeignKey('evolution_chain.evolution_chain_id'))

class EvolutionChain(db.Model):
    evolution_chain_id = db.Column(db.Integer, primary_key=True)

class Ability(db.Model):
    ability_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

class Move(db.Model):
    move_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    pp = db.Column(db.Integer)

class UserPokemon(db.Model):
    user_pokemon_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'))
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.ability_id'))

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

class CapturedPokemon(db.Model):
    captured_pokemon_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    pokemon_name = db.Column(db.String(100), nullable=False)
