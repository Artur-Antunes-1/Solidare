// cypress/e2e/adminDoacoesRecebidas.cy.js

describe('Cenario 1: Visualização de Doações Recebidas como Administrador', () => {
  beforeEach(() => {
    cy.deleteUsers();
    cy.deleteApadrinhados();
    cy.deleteDoacoes();
    cy.clearCookies();
    cy.clearLocalStorage();
    cy.visit('/');
  });

  it('Cenario 2: Administrador vê todas as doações registradas', () => {
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
    
    // Colaborador faz doação
    cy.visit('/doar/');
    cy.get('select[name="apadrinhado"]').select('João');
    cy.get('select[name="tipo"]').select('financeira');
    cy.get('input[name="valor"]').type('420');
    cy.get('textarea[name="descricao"]').type('Doação para João');
    cy.wait(1500);
    cy.get('.btn-confirmar').click(); 
    cy.url().should('include', '/painel/');

    // Volta ao login do Admin
    cy.clearCookies();
    cy.clearLocalStorage();
    cy.visit('/login/');
    cy.get('#username').type('admin_teste'); // usuário criado no cy.cadastroAdministrador()
    cy.get('#password').type('Admin123!');
    cy.contains('button', 'Entrar').click();

    // Acessa /doacoes-recebidas/ e verifica tabela
    cy.visit('/doacoes-recebidas/');
    cy.get('table').within(() => {
      cy.contains('td', 'Financeira').should('exist');
      cy.contains('td', '420,00').should('exist');
      cy.get('.badge-sucesso').should('contain.text', 'Sucesso');
      cy.contains('td', 'colaborador_teste').should('exist');
      cy.contains('td', 'João').should('exist'); // se João foi apadrinhado no comando
    });
  });

  it('Administrador vê mensagem “Nenhuma doação encontrada” quando não há registros', () => {
    cy.cadastroAdministrador();
    cy.loginAdministrador();
    cy.visit('/doacoes-recebidas/');
    cy.contains('Nenhuma doação encontrada.').should('be.visible');
  });
});
