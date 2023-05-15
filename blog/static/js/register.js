const registerForm = document.getElementById("register-form");

//GET Data from Register Form
function getRegisterInputData(){
    const firstName = document.getElementById('first-name')
    const LastName = document.getElementById('last-name')
    const username = document.getElementById('username')
    const email = document.getElementById('email')
    const password = document.getElementById('password')

    userData = {
        "first_name":firstName.value,
        "last_name":LastName.value,
        "username":username.value,
        "email":email.value,
        "password":password.value
    }
    return userData
}

//API Call to Register API
registerForm.addEventListener("submit", async(e) => {
  e.preventDefault();

  const data = getRegisterInputData()
  options={
      method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
    }
  const response = await fetch("http://127.0.0.1:8000/api/register/",options)
  if(response.ok){
    window.location.href = "/login";
  }
  else{
    console.log("registration error")
}

});
