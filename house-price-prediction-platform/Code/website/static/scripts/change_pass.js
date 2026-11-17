const rform = document.getElementById("reset-form");
const rmessage = document.getElementById("reset-message")

const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });
document.getElementById("token").value = params.token;

rform.addEventListener("submit", evt => {
	evt.preventDefault();
	fetch("/setpassword", {
		method: 'post',
		body: new FormData(evt.target)
	  }).then(resp => resp.json())
		.then(data => {
		  if(data.message == "success"){
			window.location.replace("/")
		  }else{
			rmessage.innerText = data.error;
		  }
		});
	  // Reset the form.
	  evt.target.reset();
});