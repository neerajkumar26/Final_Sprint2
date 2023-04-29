const form = document.getElementById("login-form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username, password: password })
  };

  fetch('/login', requestOptions)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // User is authenticated, do something here
      console.log(data);
      window.location.replace('/cargo');
    })
    .catch(error => {
      // Authentication failed, show error message here
      console.log('There was a problem with the authentication:', error);
    });
});
