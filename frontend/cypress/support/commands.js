Cypress.Commands.add('login', (email, password) => {
  cy.request('POST', 'http://localhost:5000/api/auth/login', {
    email: email,
    password: password
  }).then((response) => {
    window.localStorage.setItem('token', response.body.access_token);
  });
});