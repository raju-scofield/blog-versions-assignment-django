const loginForm = document.getElementById("login-form");

//GET Data from Login Form
function getLoginInputData(){
    const username = document.getElementById('login-username')
    const password = document.getElementById('login-password')
  
    userData = {
        "username":username.value,
        "password":password.value
    }
    return userData
  }

//API Call to Login API
loginForm.addEventListener("submit", async(e) => {
    e.preventDefault();
  
    const data = getLoginInputData()
    options={
        method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
      }
    const response = await fetch("http://127.0.0.1:8000/api/login/",options)
    if(response.ok){
        window.location.href = "/";
    }
    else{
        console.log("login error")
    }
  
  });