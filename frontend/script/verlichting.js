let domColorSelector, domPower, domLight, domColor, domStreaks;
let socket = '';
const lanIP = window.location.hostname;

const init = function() {
	console.log('Loaded');
	getSocketConnection();
	getUIElements();
	domColor.setAttribute('fill', 'black');
};

const getSocketConnection = function() {
	socket = io(`http://${lanIP}:5000`);
	socket.emit('statusLicht');

	useSockets();
};

const useSockets = function() {
	socket.on('statusLicht', function(status) {
		if (status.status == 1) {
			lightHolder.classList.add('active');
		} else if (status.status == 0) {
			lightHolder.classList.remove('active');
		}
	});

	socket.on('powerup', function(status) {
		if (status.status == 1) {
			lightHolder.classList.add('active');
		} else if (status.status == 0) {
			lightHolder.classList.remove('active');
		}
	});
};

const getUIElements = function() {
	domColorSelector = document.querySelector('.js-color-select');
	domPower = document.querySelector('.power');
	lightHolder = document.querySelector('.fancy-bulb');
	domColor = document.querySelector('.js-color');
	domStreaks = document.querySelectorAll('.streaks');

	listenToUI();
};

const listenToUI = function() {
	domColorSelector.addEventListener('change', function() {
		socket.emit('rgb', { value: this.value });
		domColor.setAttribute('fill', this.value);
		for (let item of domStreaks) {
			item.style.background = `${this.value}`;
		}
	});

	domPower.addEventListener('click', function() {
		socket.emit('powerup', { value: domColorSelector.value });
		domColor.setAttribute('fill', domColorSelector.value);

		for (let item of domStreaks) {
			item.style.background = `${domColorSelector.value}`;
		}
	});
};

document.addEventListener('DOMContentLoaded', init);
