function addPlayer() {
	let request = new XMLHttpRequest();
	let name = prompt("Please enter a player name", "");
	if (name == ""){
		alert("Name cannot be empty");
		return false;
	}
	request.open("POST", "/submit", true);
	request.setRequestHeader("Content-Type", "application/json");
	request.send(name);
}
function validateForm() {
	let obj = document.forms["submit_form"].elements;
	for (let x in obj){
		if (obj[x].value == ""){
			alert(`Please enter all fields ${obj[x].name}`);
			return false;
		}
  	}
}

