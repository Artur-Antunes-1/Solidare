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

Cypress.Commands.add('adicionarProgresso', () => {
    cy.get('a[href^="/adm/apadrinhado/"][href$="/adicionar-progresso/"]').click();
    cy.get('#mes').type('Janeiro');
    cy.get('#nota').type('10');
    cy.get('#frequencia').type('86%');
    cy.get('#comentario').type('Aluno foi muito bem esse mês.');
    cy.get('main > form > button').click();
});


Cypress.Commands.add('adicionarProgressoIncompleto', () => {
    cy.get('a[href^="/adm/apadrinhado/"][href$="/adicionar-progresso/"]').click();
    cy.get('#mes').type('Janeiro');
    cy.get('#nota').type('10');
    cy.get('#comentario').type('Aluno foi muito bem esse mês.');
    cy.get('main > form > button').click();
});

Cypress.Commands.add('Apadrinhar', () => {
    cy.get('nav > [href="/apadrinhar/"]').click();
    cy.get(':nth-child(1) > .btn-sponsor').click();
    cy.get('.actions > button').click();
    cy.get('[href="/meus_apadrinhados/"]').click();
});


describe('atualizar progresso de apadrinhado como administrador', () => {


    beforeEach(() => {
        cy.deleteUsers();
        cy.deleteApadrinhados()
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
    });
    });
    
    it('Cenario 1: adicionar o progresso com sucesso ', () => {
      cy.cadastroAdministrador();
      cy.loginAdministrador();
      cy.cadastroApadrinhado();
      cy.adicionarProgresso();
      cy.wait(1500);
    });

    it('Cenario 2: tentar adicionar sem preencher algum campo', () => {
      cy.cadastroAdministrador();
      cy.loginAdministrador();
      cy.cadastroApadrinhado();
      cy.adicionarProgressoIncompleto();
      cy.wait(1500);
    });
});