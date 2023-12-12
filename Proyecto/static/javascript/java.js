function desplegar(id) {
	var textoMostrar = document.getElementById(id);

	if (window.getComputedStyle(textoMostrar).display === 'block') {
		textoMostrar.style.display = 'none';
	} else {
		textoMostrar.style.display = 'block';
	}
}
function sendMessage() {
	const message = document.getElementById('messageInput').value;
	const filePath = document.getElementById('selectedFilePath').textContent;

	const chatMessages = document.getElementById('chatMessages');
	chatMessages.innerHTML += '<div class="message sent">' + message + '</div>';
	if (filePath) {
		chatMessages.innerHTML += '<div class="message sent">' + filePath + '</div>';
	}

	document.getElementById('messageInput').value = '';
	document.getElementById('selectedFilePath').textContent = '';
	document.getElementById('fileInput').value = '';
}
function handleFileSelect(input) {
	const file = input.files[0];
	if (file) {
		const filePath = file.name;
		displayFilePath(filePath);
	}
}

function displayFilePath(filePath) {
	const selectedFilePath = document.getElementById('selectedFilePath');
	selectedFilePath.textContent = 'Archivo seleccionado: ' + filePath;
}
function mostrarVentanaEmergente() {
	document.getElementById("popup-container").style.display = "block";
}
function cerrarVentanaEmergente() {
	document.getElementById("popup-container").style.display = "none";
}
function submitForm() {
	document.getElementById("boton_submit").click();
}
function toggleSize() {
	var anuncio = document.getElementById("miAnuncio");

	if (anuncio.style.height === "200px" || anuncio.style.height === "") {
		anuncio.style.display = "none";
		anuncio.style.top = "0";
	} else {
		anuncio.style.height = "200px";
	}
}
function changeAd2() {
	var adImages2 = [
		"https://www.publico.es/uploads/2018/06/04/5b154139a2ce5.jpg",
		"https://img.pccomponentes.com/pcblog/2120/1200x628-3.png",
		"https://media.tenor.com/gOr8iWY9iIsAAAAC/ronaldinho-danet-natillas.gif",
		"https://s2.ppllstatics.com/elcomercio/www/multimedia/202203/07/media/cortadas/messi-lays-kPrD-U160122932914299E-1248x770@El%20Comercio.jpg",
		"https://unapausaparalapublicidad.files.wordpress.com/2014/08/san-miguel.gif",
		"https://cuartoenfoque.com/wp-content/uploads/2021/02/videos-publicitarios-hp.gif"
	];

	var currentAdIndex2 = 0;
	var adImage2 = document.getElementById('adImage2');
	currentAdIndex2 = (currentAdIndex2 + 1) % adImages2.length;
	adImage2.src = adImages2[currentAdIndex2];
}
function changeAd() {
	var adImage = [
		"https://www.mercaderesdigitales.com/wp-content/uploads/2018/10/Imagen-animada-Restaurante-03.gif",
		"https://www.mercaderesdigitales.com/wp-content/uploads/2018/10/cocacolagiphy-1.gif",
		"https://anaortizpublicidad.com/wp-content/uploads/2020/11/Navidad-1200x480.jpg",
		"https://s1.ppllstatics.com/hoy/www/multimedia/201805/02/media/cortadas/POKER-FAMOSOS-k1TF-U501775935057sbH-624x385@Hoy.jpg",
		"https://www.elplural.com/uploads/s1/59/92/19/casino-page-1530522070811-tcm1719-408799.png",
		"https://www.elfinanciero.com.mx/resizer/yVBPPlV_02MM4m5d70zk0l7y-i0=/1200x630/filters:format(jpg):quality(70)/cloudfront-us-east-1.images.arcpublishing.com/elfinanciero/SUJH2N6DTRDGXNBXO2VRSAUCZA.jpg"
	];
	var currentAdIndex = 0; 
	var adImage = document.getElementById('adImage');
	currentAdIndex = (currentAdIndex + 1) % adImages.length;
	adImage.src = adImages[currentAdIndex];
}
setInterval(changeAd, 5000);
setInterval(changeAd2, 5000);

document.addEventListener("DOMContentLoaded", function() {
	if (!cookiesAceptadas() && !localStorage.getItem("cookiesRechazadas")) {
		mostrarNotificacionCookies();
	}
});
function mostrarNotificacionCookies() {
	var notification = document.getElementById("cookie-notification");
	notification.style.display = "block";
}
function mostrarNotificacionCookiesAceptadas() {
	var notification = document.getElementById("cookie-accepted-notification");
	notification.style.display = "block";
	setTimeout(function() {
		notification.style.display = "none";
	}, 5000); // Ocultar la notificación después de 5 segundos (puedes ajustar este valor)
}
function aceptarCookies() {
	setCookie("cookiesAceptadas", "true", 30); // Establecer cookie de aceptación por 30 días
	document.getElementById("cookie-notification").style.display = "none";
	localStorage.setItem("cookiesAceptadas", "true");
	mostrarNotificacionCookiesAceptadas();
}
function rechazarCookies() {
	// Puedes agregar acciones adicionales al rechazar cookies si es necesario
	document.getElementById("cookie-notification").style.display = "none";
	localStorage.setItem("cookiesRechazadas", "true");
}
function setCookie(nombre, valor, dias) {
	var fechaExpiracion = new Date();
	fechaExpiracion.setTime(fechaExpiracion.getTime() + (dias * 24 * 60 * 60 * 1000));
	var expira = "expires=" + fechaExpiracion.toUTCString();
	document.cookie = nombre + "=" + valor + ";" + expira + ";path=/";
}
function cookiesAceptadas() {
	return localStorage.getItem("cookiesAceptadas") === "true";
}
function getCookie(nombre) {
	var nombreC = nombre + "=";
	var cookies = decodeURIComponent(document.cookie).split(';');
	for(var i = 0; i < cookies.length; i++) {
		var c = cookies[i].trim();
		if (c.indexOf(nombreC) == 0) {
			return c.substring(nombreC.length, c.length);
		}
	}
	return "";
}

