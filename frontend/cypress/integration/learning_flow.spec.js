describe('Learning Flow', () => {
  beforeEach(() => {
    // Assuming we have a test user set up
    cy.login('testuser@example.com', 'password123');
  });

  it('completes a learning flow', () => {
    // Visit the dashboard
    cy.visit('/dashboard');
    cy.contains('Your Learning Dashboard').should('be.visible');

    // Start a learning material
    cy.contains('Start Learning').first().click();

    // Update progress
    cy.get('[data-testid="progress-slider"]').invoke('val', 50).trigger('change');
    cy.contains('Update Progress').click();

    // Take a quiz
    cy.contains('Take Quiz').click();
    cy.get('[data-testid="quiz-question"]').should('be.visible');
    cy.get('[data-testid="quiz-option"]').first().click();
    cy.contains('Submit Quiz').click();

    // Verify completion
    cy.contains('Quiz completed').should('be.visible');

    // Check updated progress on dashboard
    cy.visit('/dashboard');
    cy.contains('50%').should('be.visible');
  });
});