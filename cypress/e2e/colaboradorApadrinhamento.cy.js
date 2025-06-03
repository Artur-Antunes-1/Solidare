Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout); 
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
  });


Cypress.Commands.add('deleteApadrinhados', () => {
    return cy.exec('python delete_apadrinhados.py', { failOnNonZeroExit: false }).then((result) => {
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

Cypress.Commands.add('cadastroColaborador', () => {
    cy.visit('/');
    cy.get('[href="/registrar/"]').click();
    cy.get('#id_tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Colaborador');
    cy.get('#id_username').type('teste colaborador');
    cy.get('#id_email').type('cypress@teste.com');
    cy.get('#id_password1').type('12345');
    cy.get('#id_password2').type('12345');
    cy.get('button').click();
});

Cypress.Commands.add('loginColaborador', () => {
  cy.get('#username').type('teste colaborador');
  cy.get('#password').type('12345');
  cy.get('.auth-box > form > button').click();
});

Cypress.Commands.add('cadastroApadrinhado', () => {
    cy.get('nav > [href="/registrar/apadrinhado/"]').click();
    cy.get('#nome').type('João');
    cy.get('#idade').type('08');
    cy.get('#genero');
    cy.get('select[name="genero"]').select('Masculino');
    cy.get('.alinhar > button').click();
    
});

Cypress.Commands.add('cadastroApadrinhado2', () => {
    cy.get('nav > [href="/registrar/apadrinhado/"]').click();
    cy.get('#nome').type('Maria');
    cy.get('#idade').type('06');
    cy.get('#genero');
    cy.get('select[name="genero"]').select('Feminino');
    cy.get('.alinhar > button').click();
    
});


describe('Apadrinhamento como colaborador', () => {


    beforeEach(() => {
        cy.deleteUsers();
        cy.deleteApadrinhados()
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
        });
    });
    
    it('Cenario 1: Visualização da lista de apadrinhados disponiveis', () => {
        cy.cadastroAdministrador();
        cy.loginAdministrador();
        cy.cadastroApadrinhado();
        cy.cadastroApadrinhado2();
        cy.get(':nth-child(2) > form > button').click();
        cy.get('p > a').click();
        cy.cadastroColaborador();
    });

});