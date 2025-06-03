Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout); 
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
  });

 

Cypress.Commands.add('cadastroAdministrador', () => {
    cy.visit('/');
    cy.get('[href="/registrar/"]').click();
    cy.get('#id_tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Administrador');
    cy.get('#id_username').type('teste administrador');
    cy.get('#id_email').type('cypress@teste.com');
    cy.get('#id_password1').type('12345');
    cy.get('#id_password2').type('12345');
    cy.get('.auth-box > form > button').click();
});

Cypress.Commands.add('loginAdministrador', () => {
  cy.get('#username').type('teste administrador');
  cy.get('#password').type('12345');
  cy.get('.auth-box > form > button').click();
});

describe('cadastro como administrador', () => {


    beforeEach(() => {
        cy.deleteUsers()
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
    });
    });

    it('Cadastro', () => {
        cy.cadastroAdministrador();
        cy.loginAdministrador();
    });


});