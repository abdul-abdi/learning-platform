describe('Login', () => {
  it('should login successfully with correct credentials', () => {
    cy.visit('/login');
    cy.get('input[name=email]').type('testuser@example.com');
    cy.get('input[name=password]').type('password123');
    cy.get('button[type=submit]').click();
    cy.url().should('include', '/dashboard');
    cy.contains('Your Learning Dashboard').should('be.visible');
  });

  it('should show an error message with incorrect credentials', () => {
    cy.visit('/login');
    cy.get('input[name=email]').type('wronguser@example.com');
    cy.get('input[name=password]').type('wrongpassword');
    cy.get('button[type=submit]').click();
    cy.contains('Invalid credentials').should('be.visible');
  });
});