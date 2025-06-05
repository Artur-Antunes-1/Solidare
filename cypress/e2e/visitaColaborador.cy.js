
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
    cy.get('#id_email').type('administrador@teste.com');
    cy.get('#id_password1').type('12345');
    cy.get('#id_password2').type('12345');
    cy.get('button').click();
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
    cy.get('#id_email').type('colaborador@teste.com');
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



Cypress.Commands.add('apadrinhar', () => {
    cy.get('nav > [href="/apadrinhar/"]').click();
    cy.get(':nth-child(1) > .btn-sponsor').click();
    cy.get('.actions > button').click();
    cy.get('[href="/meus_apadrinhados/"]').click();
});

Cypress.Commands.add('agendar', () => {
    cy.get('#data').type('2025-06-02');
    cy.get('#hora').type('10:30');
    cy.get('#motivo').type('parabenizar meu apadrinhado por ter ido muito bem esse mês');
    cy.get('main > form > button').click();
});

Cypress.Commands.add('aprovarESair', () => {
    cy.get('[href="/adm/visitas-pendentes/"]').click();
    cy.get('[action^="/adm/aprovar-visita/"] > button').click();
    cy.get('button').click();
});

Cypress.Commands.add('recusarESair', () => {
    cy.get('[href="/adm/visitas-pendentes/"]').click();
    cy.get('[action^="/adm/recusar-visita/"] > button').click();
    cy.get('button').click();
});


describe('agendar visita como colaborador', () => {


    beforeEach(() => {
        cy.deleteUsers();
        cy.deleteApadrinhados()
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
    });
    });
    it('Cenario 1: agendar uma visita e ela ser aceita ', () => {
        cy.cadastroAdministrador();
        cy.loginAdministrador();
        cy.cadastroApadrinhado();
        cy.get(':nth-child(2) > form > button').click();
        cy.get('p > a').click();
        cy.cadastroColaborador();
        cy.loginColaborador();
        cy.apadrinhar();
        cy.get('.btn-agendar').click();
        cy.agendar();
        cy.wait(1000);
        cy.get(':nth-child(2) > form > button').click();
        cy.loginAdministrador();
        cy.aprovarESair();
        cy.loginColaborador();
        cy.get('[href="/minhas-visitas/"]').click();
        cy.wait(1500);
    });
    it('Cenario 2 : agendar uma visita e ela ser recusada', () => {
        cy.cadastroAdministrador();
        cy.loginAdministrador();
        cy.cadastroApadrinhado();
        cy.get(':nth-child(2) > form > button').click();
        cy.get('p > a').click();
        cy.cadastroColaborador();
        cy.loginColaborador();
        cy.apadrinhar();
        cy.get('.btn-agendar').click();
        cy.agendar();
        cy.wait(1000);
        cy.get(':nth-child(2) > form > button').click();
        cy.loginAdministrador();
        cy.recusarESair();
        cy.loginColaborador();
        cy.get('[href="/minhas-visitas/"]').click();
        cy.wait(1500);
    });
});