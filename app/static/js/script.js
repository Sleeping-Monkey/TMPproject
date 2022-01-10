document.getElementById("login-section").style.visibility = 'hidden'
document.getElementById("register-section").style.visibility = 'hidden'

document.getElementById("button-create-game").onclick = function() {
  document.getElementById("login-section").style.visibility = 'visible'
}

document.getElementById("show-register").onclick = function() {
  document.getElementById("login-section").style.visibility = 'hidden'
  document.getElementById("register-section").style.visibility = 'visible'  
}

document.getElementById("show-login").onclick = function() {
  document.getElementById("login-section").style.visibility = 'visible'
  document.getElementById("register-section").style.visibility = 'hidden'  
}
