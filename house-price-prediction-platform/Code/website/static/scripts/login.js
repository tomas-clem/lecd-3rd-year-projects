const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const sform = document.getElementById("signup-form");
const lform = document.getElementById("login-form");
const serror = document.getElementById("signup-message");
const lerror = document.getElementById("login-message");

signUpButton.addEventListener('click', () => {
	lerror.innerText = "";
	serror.innerText = "";
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	lerror.innerText = "";
	serror.innerText = "";
	container.classList.remove("right-panel-active");
});


sform.addEventListener("submit", evt => {
	evt.preventDefault();
	if(evt.target["email"].value  == "" || evt.target["name"].value == "" || evt.target["password"].value == "" ){
		serror.innerText = "Verifique que preenche todos os campos!"
	}else{
		fetch("/register", {
			method: 'post',
			body: new FormData(evt.target)
		  }).then(resp => resp.json())
			.then(data => {
			  if(data.message == "success"){
				console.log(data.next_page)
					if(data.next_page){
						window.location.replace(data.next_page);
					}else{
						window.location.replace("/");
					}
			  }else{
				serror.innerText = data.error;
			  }
			});
		  // Reset the form.
		  evt.target.reset();
	}
});

lform.addEventListener("submit", evt => {
	evt.preventDefault();
	if(evt.target["email"].value  == "" || evt.target["password"].value == "" ){
		serror.innerText = "Verifique que preenche todos os campos!"
	}else{
		fetch("/login", {
			method: 'post',
			body: new FormData(evt.target)
		}).then(resp => resp.json())
			.then(data => {
				if(data.message == "success"){
					console.log(data.next_page)
					if(data.next_page){
						window.location.replace(data.next_page);
					}else{
						window.location.replace("/");
					}
					
				}else{
					lerror.innerText = data.error;
				}
			});
		// Reset the form.
		evt.target.reset();
	}
});