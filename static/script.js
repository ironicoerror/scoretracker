function addGame() {
	//adds a game on button click via showing a popup and user entering a game name 
	//input will be checked: cancel dialog (null), empty name(""), name taken("in sgame?")
	let name = prompt("Please enter a game name", "");
	let request = new XMLHttpRequest();
	if (name == null){
		return false;
	}
	else if (name == ""){
		alert("Name cannot be empty");
		return false;
	}
	else {
		for (let option in document.forms["submit_form"]["sgame"].options) {
			if (name == `${document.forms["submit_form"]["sgame"][option].text}`) {
				alert("Game already exists.");
				return false
			}
		}
	}
	request.onload = function() {
		console.log(`Loaded: ${request.status}`);
		location.reload();
	}
	request.onerror = function() {
					console.log(`Error on Post Method: ${request.error}`);
					alert("Network Error");
	}
	request.open("POST", "/submit", true);
	request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	request.setRequestHeader("js_function", "addGame");
	request.send(JSON.stringify({ "game_name": name}));
}

function addPlayer() {
	//adds a player on button click via showing a popup and user entering a player name 
	//input will be checked: cancel dialog (null), empty name(""), name taken("in team1?")
	let name = prompt("Please enter a player name", "");
	let request = new XMLHttpRequest();
	if (name == null){
		return false;
	}
	else if (name == ""){
		alert("Name cannot be empty");
		return false;
	}
	else {
		for (let option in document.forms["submit_form"]["team1"].options) {
			if (name == `${document.forms["submit_form"]["team1"][option].text}`) {
				alert("Player already exists.");
				return false
			}
		}
	}
	request.onload = function() {
		console.log(`Loaded: ${request.status}`);
		location.reload();
	}
	request.onerror = function() {
					console.log(`Error on Post Method: ${request.error}`);
					alert("Network Error");
	}
	request.open("POST", "/submit", true);
	request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	request.setRequestHeader("js_function", "addPlayer");
	request.send(JSON.stringify({ "player_name": name}));
}

function validateForm() {
	//on button submit, checks if all fields in the form have a value
	//alerts the user if not the case with the empty box name
	let obj = document.forms["submit_form"].elements;
	for (let x in obj){
		if (obj[x].value == ""){
			alert(`Please enter field: ${obj[x].name}`);
			return false;
			}
  	}
}

