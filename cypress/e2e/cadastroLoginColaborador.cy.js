Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout); 
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
  });


Cypress.Commands.add('cadastroColaborador', () => {
    cy.visit('/');
    cy.get('[href="/registrar/"]').click();
    cy.get('#id_tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Colaborador');
    cy.get('#id_username').type('teste colaborador');
    cy.get('#id_email').type('cypress@teste.com');
    cy.get('#id_password1').type('12345');
    cy.get('#id_password2').type('12345');
    cy.get('.auth-box > form > button').click();
});

Cypress.Commands.add('loginColaborador', () => {
  cy.get('#username').type('teste colaborador');
  cy.get('#password').type('12345');
  cy.get('.auth-box > form > button').click();
});

describe('cadastro como colaborador', () => {


    beforeEach(() => {
        cy.deleteUsers()
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
    });
    });

    it('Cadastro', () => {
        cy.cadastroColaborador();
        cy.loginColaborador();
    });


});