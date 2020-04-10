function validateForm() {
	let obj = document.forms["submit_form"].elements;
	for (let x in obj){
		if (obj[x].value == ""){
			alert(`Please enter all fields ${obj[x].name}`);
			return false;
		}
  	}
};

