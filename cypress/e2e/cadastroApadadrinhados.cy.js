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


Cypress.Commands.add('cadastroApadrinhado', () => {
    cy.get('nav > [href="/registrar/apadrinhado/"]').click();
    cy.get('#nome').type('João');
    cy.get('#idade').type('08');
    cy.get('#genero');
    cy.get('select[name="genero"]').select('Masculino');
    cy.get('.alinhar > button').click();
    
});


Cypress.Commands.add('cadastroApadrinhadoIncompleto', () => {
    cy.get('nav > [href="/registrar/apadrinhado/"]').click();
    cy.get('#nome').type('João');
    cy.get('#genero');
    cy.get('select[name="genero"]').select('Masculino');
    cy.get('.alinhar > button').click();
    
});


Cypress.Commands.add('edicaoApadrinhado', () => {
    cy.get('a[href^="/apadrinhados/editar"][href$="/editar"]').click();
    cy.get('#nome').clear();
    cy.get('#nome').type('Maria');
    cy.get('#idade').clear();
    cy.get('#idade').type('06');
    cy.get('#genero');
    cy.get('[name="genero"]').select('Feminino');
    cy.get('.btn-edit').click();


});


describe('cadastro de apadrinhados como administrador', () => {


    beforeEach(() => {
        cy.deleteUsers();
        cy.deleteApadrinhados()
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
    });
    });

    it('Cenario 1: Cadastro de apadrinhado bem sucedido', () => {
        cy.cadastroAdministrador();
        cy.loginAdministrador();
        cy.cadastroApadrinhado();
        cy.wait(1000);
    });


    it('Cenario 2: Edição de apadrinhados', () => {
        cy.cadastroAdministrador();
        cy.loginAdministrador();
        cy.cadastroApadrinhado();
        cy.edicaoApadrinhado();
        cy.wait(1000);

    });

    it('Cenario 3: Cadastro sem preencher todos os campos', () => {
        cy.cadastroAdministrador();
        cy.loginAdministrador();
        cy.cadastroApadrinhadoIncompleto();
    });
});