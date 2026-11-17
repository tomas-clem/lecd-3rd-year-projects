const rform = document.getElementById("reset-form");
const rmessage = document.getElementById("reset-message")

rform.addEventListener("submit", evt => {
	evt.preventDefault();
	fetch("/reset", {
		method: 'post',
		body: new FormData(evt.target)
	  }).then(resp => resp.json())
		.then(data => {
		  if(data.message != "error"){
			rmessage.innerText = data.message;
		  }else{
			rmessage.innerText = data.error;
		  }
		});
	  // Reset the form.
	  evt.target.reset();
});
