document.addEventListener("DOMContentLoaded", () => {

const generateButton = document.getElementById('generate-pokemon');
const catchButton = document.getElementById('catch-button');
const homeLink = document.getElementById('home-link');
const profileLink = document.getElementById('profile-link');
const listOfPokemonLink = document.getElementById('list-of-pokemon-link');
const aboutLink = document.getElementById('about-link');
const suggestionsLink = document.getElementById('suggestions-link');
const loginLink = document.getElementById('login-link');
const signupLink = document.getElementById('signup-link');
const pokemonList = document.getElementById('pokemon-list');
// const tradeCenterLink = getElementById('trade-center-link');

homeLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/';
});

profileLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/profile';
});

listOfPokemonLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/list-of-pokemon';
});

loginLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/login';
});

signupLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/signup';
});

aboutLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/about';
});

suggestionsLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/suggestions';
});

// tradeCenterLink.addEventListener('click', function(evt) {
//     evt.preventDefault();
//     window.location.href = '/trade-center';
// });

generateButton.addEventListener('click', async () => {
    console.log("Button works");
    generateButton.disabled = true;

    try {
        const apiResponse = await axios.get('/generate-pokemon');
        console.log("API Response");
        const pokemonData = apiResponse.data;
        console.log("Pokemon Data");
        updatePokemon(pokemonData);

        const randomNum = Math.floor(Math.random() * 10) + 1;

        if (randomNum === 1) {
            pokemonData.sprites.front_default = pokemonData.sprites.front_shiny;
        }

        updatePokemon(pokemonData);
        generateButton.disabled = false;
    } catch (error) {
        console.error("Error generating new Pokemon:", error);
        generateButton.disabled = false;
    }
});

function updatePokemon(pokemonData) {
    console.log("Updating Pokemon:", pokemonData)
    const pokemonName = document.getElementById('pokemon-name');
    const pokemonArtwork = document.querySelector('#roulette img');

    const capitalizedPokemonName = capitalizeFirstLetter(pokemonData['name']);
    pokemonName.textContent = capitalizedPokemonName;
    console.log(capitalizedPokemonName);

    pokemonArtwork.src = pokemonData['sprites']['front_default'];
}

function capitalizeFirstLetter(string) {
    if (string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    return "";
}

function appendPokemonToProfile(spriteUrl) {
    if (pokemonList) {
        const img = document.createElement('img');
        img.src = spriteUrl;
        img.alt = 'Pokemon Sprite';
        pokemonList.appendChild(img);
    }
}

catchButton.addEventListener('click', async function () {
    try {
        const apiResponse = await axios.get('/generate-pokemon');
        const randomSpriteUrl = apiResponse.data.spriteUrl;
        const pokemonName = apiResponse.data.name;

        const catchApiResponse = await axios.post('/catch-pokemon', {
            pokemon_name: pokemonName, 
            sprite_url: randomSpriteUrl
        });

        if (catchApiResponse.data.status === 'success') {
            alert(`You caught ${pokemonName}!`);
        } else {
            alert(`Failed to save Pokemon.`);
        }
    } catch (error) {
        console.error('Error catching Pokemon:', error);
    }
});

})