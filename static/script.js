"use strict";

function change() {
	var a = document.getElementById('date1').value;
	var b = document.getElementById('date2').value;
	var image = document.getElementById('image_box');
	image.src = "/test?date1=" + a + "&date2=" + b;
}
