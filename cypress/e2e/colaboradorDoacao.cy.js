// cypress/e2e/doacoesColaborador.cy.js

describe('Fluxo de Doação como Colaborador', () => {
  beforeEach(() => {
    cy.deleteUsers();
    cy.deleteApadrinhados();
    cy.deleteDoacoes();
    cy.clearCookies();
    cy.clearLocalStorage();
    cy.visit('/');
  });

  it('Cenario 1: Colaborador faz doação financeira com sucesso', () => {
    // Cadastra e loga Admin
    cy.cadastroAdministrador();
    cy.loginAdministrador();

    // Cadastra Apadrinhado
    cy.cadastroApadrinhado();

    cy.visit('/logout/')

    // Cadastra e loga Colaborador
    cy.cadastroColaborador();
    cy.loginColaborador();

    cy.get('nav > [href="/apadrinhar/"]').click();
    cy.wait(1500);
    cy.get('.btn-sponsor').click();
    cy.get('.actions > button').click();

    // Preenche o formulário de doação
    cy.visit('/doar/');
    cy.get('select[name="apadrinhado"]').select('João');
    cy.get('select[name="tipo"]').select('financeira');
    cy.get('input[name="valor"]').type('750');
    cy.get('textarea[name="descricao"]').type('Doação de teste Cypress');
    cy.get('.btn-confirmar').click(); 

    // Valida redirecionamento para painel e conteúdo da tabela
    cy.url().should('include', '/painel/');
    cy.get('table').within(() => {
      cy.contains('td', 'Financeira').should('exist');
      cy.contains('td', '750,00').should('exist');
      cy.get('.badge-sucesso').should('contain.text', 'Sucesso');
    });
  });

  it('Cenario 2: Colaborador tenta doar sem preencher valor financeiro e recebe erro', () => {
    cy.cadastroAdministrador();
    cy.loginAdministrador();

    cy.cadastroApadrinhado();
    
    cy.visit('/logout/')

    // Cadastra e loga Colaborador
    cy.cadastroColaborador();
    cy.loginColaborador();

    cy.get('nav > [href="/apadrinhar/"]').click();
    cy.wait(1500);
    cy.get('.btn-sponsor').click();
    cy.get('.actions > button').click();


    cy.visit('/doar/');
    cy.get('select[name="apadrinhado"]').select('João');
    cy.get('select[name="tipo"]').select('financeira');
    cy.get('textarea[name="descricao"]').type('Tentativa sem valor');
    cy.get('.btn-confirmar').click();

    cy.url().should('include', '/painel/');
    cy.get('.badge-falha').should('contain.text', 'Falha');
  });
});
