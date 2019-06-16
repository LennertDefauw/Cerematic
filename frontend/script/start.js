let socket = '';
let statusRechts,
	statusLinks,
	soortRechts,
	soortLinks,
	inhoudLinks,
	inhoudRechts,
	gewichtLinks,
	gewichtRechts,
	refreshedLinks;

let valueLinks, valueRechts;
let refreshLinks, refreshRechts;

let selectLinks, selectRechts;

let buttonLinks, buttonRechts;
let tabRechts;
const lanIP = window.location.hostname;

const getDOMElements = function() {
	statusRechts = document.querySelector('.js-komRechts');
	statusLinks = document.querySelector('.js-komLinks');
	soortRechts = document.querySelector('.js-soortRechts');
	soortLinks = document.querySelector('.js-soortLinks');
	inhoudLinks = document.querySelector('.js-inhoudLinks');
	inhoudRechts = document.querySelector('.js-inhoudRechts');
	refreshLinks = document.querySelector('.js-refreshLinks');
	refreshRechts = document.querySelector('.js-refreshRechts');
	gewichtLinks = document.querySelector('.js-gewichtLinks');
	gewichtRechts = document.querySelector('.js-gewichtRechts');
	selectLinks = document.querySelector('.js-select-links');
	selectRechts = document.querySelector('.js-select-rechts');
	buttonLinks = document.querySelector('.js-button-links');
	buttonRechts = document.querySelector('.js-button-rechts');
	tabRechts = document.querySelector('#tab2');
};

const listenToDOM = function() {
	refreshLinks.addEventListener('click', function() {
		socket.emit('refreshLinks');
	});

	refreshRechts.addEventListener('click', function() {
		socket.emit('refreshRechts');
	});

	tabRechts.addEventListener('click', function() {
		socket.emit('connectRechts');
	});

	selectLinks.addEventListener('change', function() {
		buttonLinks.setAttribute('portie', this.value);
	});

	buttonLinks.addEventListener('click', function() {
		socket.emit('useMotor', {
			portie: buttonLinks.getAttribute('portie'),
			motor: 'links'
		});
	});

	selectRechts.addEventListener('change', function() {
		buttonRechts.setAttribute('portie', this.value);
	});

	buttonRechts.addEventListener('click', function() {
		socket.emit('useMotor', {
			portie: buttonRechts.getAttribute('portie'),
			motor: 'rechts'
		});
	});
};
const init = function() {
	getDOMElements();
	listenToDOM();
	getSocketConnection();
};

const roundvalue = function(getal) {
	rounded = Math.round(getal * 100) / 100;
	return rounded;
};

const getSocketConnection = function() {
	socket = io(`http://${lanIP}:5000`);

	socket.emit('connectLinks');

	socket.on('connectLinks', function(data) {
		statusLinks.innerHTML = data['statuslinks'];
		soortLinks.innerHTML = data['soortlinks'][0]['naam'];
		inhoudLinks.innerHTML = roundvalue(data['afstandlinks']) + '%';

		valueLinks = data['gewichtlinks'];
		if (valueLinks < 5) {
			valueLinks = 0;
		}
		gewichtLinks.innerHTML = roundvalue(valueLinks) + ' gram';
	});

	socket.on('intervalLinks', function(data) {
		statusLinks.innerHTML = data['statuslinks'];
		soortLinks.innerHTML = data['soortlinks'][0]['naam'];
		inhoudLinks.innerHTML = roundvalue(data['afstandlinks']) + '%';

		valueLinks = data['gewichtlinks'];
		if (valueLinks < 5) {
			valueLinks = 0;
		}
		gewichtLinks.innerHTML = roundvalue(valueLinks) + ' gram';
	});

	socket.on('refreshLinks', function(data) {
		statusLinks.innerHTML = data['statuslinks'];
		soortLinks.innerHTML = data['soortlinks'][0]['naam'];
		inhoudLinks.innerHTML = roundvalue(data['afstandlinks']) + '%';

		refreshedLinks = data['gewichtlinks'];
		if (refreshedLinks < 5) {
			refreshedLinks = 0;
		}
		gewichtLinks.innerHTML = roundvalue(refreshedLinks) + ' gram';
	});

	socket.on('connectRechts', function(data) {
		statusRechts.innerHTML = data['statusrechts'];
		soortRechts.innerHTML = data['soortrechts'][0]['naam'];
		inhoudRechts.innerHTML = roundvalue(data['afstandrechts']) + '%';

		refreshedRechts = data['gewichtrechts'];
		if (refreshedRechts < 5) {
			refreshedRechts = 0;
		}
		gewichtRechts.innerHTML = roundvalue(refreshedRechts) + ' gram';
	});

	socket.on('intervalRechts', function(data) {
		statusRechts.innerHTML = data['statusrechts'];
		soortRechts.innerHTML = data['soortrechts'][0]['naam'];
		inhoudRechts.innerHTML = roundvalue(data['afstandrechts']) + '%';

		refreshedRechts = data['gewichtrechts'];
		if (refreshedRechts < 5) {
			refreshedRechts = 0;
		}
		gewichtRechts.innerHTML = roundvalue(refreshedRechts) + ' gram';
	});

	socket.on('refreshRechts', function(data) {
		statusRechts.innerHTML = data['statusrechts'];
		soortRechts.innerHTML = data['soortrechts'][0]['naam'];
		inhoudRechts.innerHTML = roundvalue(data['afstandrechts']) + '%';

		refreshedRechts = data['gewichtrechts'];
		if (refreshedRechts < 5) {
			refreshedRechts = 0;
		}
		gewichtRechts.innerHTML = roundvalue(refreshedRechts) + ' gram';
	});
};

document.addEventListener('DOMContentLoaded', init);
