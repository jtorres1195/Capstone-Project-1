document.addEventListener("DOMContentLoaded", () => {

const generateButton = document.getElementById('generate-pokemon');
const catchButton = document.getElementById('catch-button');
const homeLink = document.getElementById('home-link');
const myProfileLink = document.getElementById('my-profile-link');
const listOfPokemonLink = document.getElementById('list-of-pokemon-link');
const aboutLink = getElementById('about-link');
const suggestionsLink = getElementById('suggestions-link');
const loginLink = document.getElementById('login-link');
const signupLink = document.getElementById('signup-link');
// const tradeCenterLink = getElementById('trade-center-link');

homeLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/';
});

myProfileLink.addEventListener('click', function(evt) {
    evt.preventDefault();
    window.location.href = '/my-profile';
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
    try {
        const apiResponse = await axios.get('/generate-pokemon');
        console.log("API Response");
        const pokemonData = apiResponse.data;
        console.log("Pokemon Data");
        updatePokemon(pokemonData);
    } catch (error) {
        console.error("Error generating new Pokemon:", error);
    }
});

catchButton.addEventListener('click', () => {
    const pokemonName = '{{ random_pokemon["name"] }}';
    savePokemon(pokemonName);
})

function updatePokemon(pokemonData) {
    console.log("Updating Pokemon:", pokemonData)
    const pokemonName = document.getElementById('pokemon-name')
    console.log(pokemonName);
    const pokemonArtwork = document.querySelector('#roulette img')

    const capitalizedPokemonName = capitalizeFirstLetter(pokemonData['name']);
    pokemonName.textContent = capitalizedPokemonName;
    console.log(capitalizedPokemonName);
    
    pokemonArtwork.src = pokemonData['sprites']['other']['official-artwork']['front_default'];
}

function capitalizeFirstLetter(string) {
    if (string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    return "";
    }
})


async function savePokemon(pokemonName) {
    try {
        const apiResponse = await axios.post('/save-pokemon', { pokemon_name: pokemonName });
        if (apiResponse.data === 'success') {
            alert(`You caught ${pokemonName}!`);
        } else {
            alert(`Failed to save Pokemon.`);
        }
    } catch (error) {
        console.error('Error saving Pokemon:', error);
    }
}