let socket = '';
const lanIP = window.location.hostname;

let inputHolder, buttonHolder, selectHolder, changeHolder;

const getSocketConnection = function() {
	socket = io(`http://${lanIP}:5000`);

	socket.on('successAdd', function() {
		buttonHolder.setAttribute('style', 'background-color: green');
		getCornflakes();
	});

	socket.on('successChange', function() {
		changeHolder.setAttribute('style', 'background-color: green');
	});
};

const fillSelectTag = function(data) {
	let HTMLCode =
		'<option value="" disabled selected hidden>Kies de cornflakes</option>';
	for (let item of data) {
		HTMLCode += `<option value="${item['cornflakesID']}">${
			item['naam']
		}</option>`;
	}

	selectHolder.innerHTML = HTMLCode;
};

const getCornflakes = function() {
	fetch(`http://${lanIP}:5000/api/v1/cornflakes`)
		.then(function(response) {
			return response.json();
		})
		.then(function(data) {
			fillSelectTag(data);
		});
};

const getDOMElements = function() {
	inputHolder = document.querySelector('.js-cereals');
	buttonHolder = document.querySelector('.js-button-input');
	selectHolder = document.querySelector('.js-select');
	changeHolder = document.querySelector('.js-change');
};
const init = function() {
	getDOMElements();
	getSocketConnection();
	listenToUI();
	getCornflakes();
};

const listenToUI = function() {
	inputHolder.addEventListener('change', function() {
		buttonHolder.setAttribute('name', this.value);
	});

	buttonHolder.addEventListener('click', function() {
		socket.emit('insertName', { naam: buttonHolder.getAttribute('name') });
	});

	selectHolder.addEventListener('change', function() {
		changeHolder.setAttribute('id', this.value);
	});

	changeHolder.addEventListener('click', function() {
		socket.emit('changeCornflakesLinks', {
			id: changeHolder.getAttribute('id')
		});
	});
};
document.addEventListener('DOMContentLoaded', init);
