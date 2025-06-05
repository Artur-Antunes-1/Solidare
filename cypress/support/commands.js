// cypress/support/commands.js

// ***********************************************
// Comandos Customizados para todo o projeto Cypress
// ***********************************************

// -- LIMPEZA DE DADOS --------------------------------------------------------
// Esses comandos usam cy.exec() para chamar scripts Python que
// removem todos os registros de teste do banco (usuários, apadrinhados, doações).

Cypress.Commands.add('deleteUsers', () => {
  // remove todos os usuários de teste (exceto superusuário “real”)
  return cy.exec('python delete_users.py', { failOnNonZeroExit: false })
    .then((result) => {
      console.log('deleteUsers stdout:', result.stdout);
      if (result.stderr) {
        console.error('deleteUsers stderr:', result.stderr);
      }
    });
});

Cypress.Commands.add('deleteApadrinhados', () => {
  // remove todos os Apadrinhado do banco
  return cy.exec('python delete_apadrinhados.py', { failOnNonZeroExit: false })
    .then((result) => {
      console.log('deleteApadrinhados stdout:', result.stdout);
      if (result.stderr) {
        console.error('deleteApadrinhados stderr:', result.stderr);
      }
    });
});

Cypress.Commands.add('deleteDoacoes', () => {
  // remove todos os objetos Doacao do banco
  return cy.exec('python delete_doacoes.py', { failOnNonZeroExit: false })
    .then((result) => {
      console.log('deleteDoacoes stdout:', result.stdout);
      if (result.stderr) {
        console.error('deleteDoacoes stderr:', result.stderr);
      }
    });
});

// -- CADASTRO / LOGIN DE ADMINISTRADOR --------------------------------------
// Pressupõe que você tenha um formulário em “/registrar/” que aceita:
//   - select[name="tipo_usuario"] com opção "Administrador"
//   - input#id_username, input#id_email, input#id_password1, input#id_password2
//   - um botão que tenha o texto “Cadastrar” para submeter o formulário.

Cypress.Commands.add('cadastroAdministrador', () => {
  cy.visit('/');
  cy.get('[href="/registrar/"]').click();

  // seleciona “Administrador” no campo tipo_usuario
  cy.get('select[name="tipo_usuario"]').select('Administrador');

  // preenche os campos de cadastro
  cy.get('input#id_username').type('admin_teste');
  cy.get('input#id_email').type('admin@example.com');
  cy.get('input#id_password1').type('Admin123!');
  cy.get('input#id_password2').type('Admin123!');

  // IMPORTANTE: clicar exatamente no botão cujo texto é “Cadastrar”
  cy.contains('button', 'Cadastrar').click();

  // garante que não estamos mais na página /registrar/
  cy.url().should('not.include', '/registrar/');
});

Cypress.Commands.add('loginAdministrador', () => {
  cy.visit('/login/');

  // preenche as credenciais já cadastradas acima
  cy.get('#username').type('admin_teste');
  cy.get('#password').type('Admin123!');

  // IMPORTANTE: clicar exatamente no botão cujo texto é “Entrar”
  cy.contains('button', 'Entrar').click();

  // garante que não estamos mais em /login/
  cy.url().should('not.include', '/login/');
});

// -- CADASTRO / LOGIN DE COLABORADOR ----------------------------------------
// Pressupõe que o mesmo formulário “/registrar/” aceita “Colaborador”
// nos mesmos campos (tipo_usuario, username, email, password1, password2).

Cypress.Commands.add('cadastroColaborador', () => {
  cy.visit('/');
  cy.get('[href="/registrar/"]').click();

  // seleciona “Colaborador”
  cy.get('select[name="tipo_usuario"]').select('Colaborador');

  // preenche dados de colaborador
  cy.get('input#id_username').type('colaborador_teste');
  cy.get('input#id_email').type('colaborador@example.com');
  cy.get('input#id_password1').type('Colab123!');
  cy.get('input#id_password2').type('Colab123!');

  // IMPORTANTE: clicar no botão “Cadastrar”
  cy.contains('button', 'Cadastrar').click();

  cy.url().should('not.include', '/registrar/');
});

Cypress.Commands.add('loginColaborador', () => {
  cy.visit('/login/');

  cy.get('#username').type('colaborador_teste');
  cy.get('#password').type('Colab123!');

  // IMPORTANTE: clicar no botão “Entrar”
  cy.contains('button', 'Entrar').click();

  cy.url().should('not.include', '/login/');
});

// -- CADASTRO DE APADRINHADO ------------------------------------------------
// Pressupõe que, após fazer login como Administrador, exista um link ou botão
// para “/apadrinhar/” e um formulário com campos:
//   input#id_nome, input#id_idade, input#id_cidade, select#id_situacao, button “Cadastrar Apadrinhado”.

Cypress.Commands.add('cadastroApadrinhado', () => {
  // assume que estamos logados como Administrador
  cy.get('nav > [href="/registrar/apadrinhado/"]').click();

  // preenche campos do formulário de Apadrinhado
  cy.get('#nome').type('João');
  cy.get('#idade').type('15');
  cy.get('#genero');
  cy.get('select[name="genero"]').select('Masculino');
  cy.get('.alinhar > button').click();

  // garante que saiu da rota /apadrinhar/
  cy.url().should('not.include', 'registrar/apadrinhado/');
});

// -- CADASTRO DE APADRINHADO INCOMPLETO (opcional) --------------------------
// Caso queira testar a validação de “não preencher todos os campos”:
Cypress.Commands.add('cadastroApadrinhadoIncompleto', () => {
  cy.get('[href="/apadrinhar/"]').click();
  cy.contains('button', 'Cadastrar').click();
  cy.get('.alert-error').should('exist');
});

// -- EDIÇÃO DE APADRINHADO ---------------------------------------------------
// Se precisar reusar, ajuste seletores conforme seu HTML real.
Cypress.Commands.add('edicaoApadrinhado', () => {
  cy.visit('/apadrinhados/');
  // clica no botão “Editar” do primeiro apadrinhado (ajuste seletor ao seu caso):
  cy.get('.btn-editar-apadrinhado').first().click();
  // altera campo e salva (botão de texto “Salvar” ou “Atualizar” no seu formulário):
  cy.get('input#id_nome').clear().type('João Editado');
  cy.contains('button', 'Salvar').click();
  cy.contains('Apadrinhado atualizado').should('exist');
});

Cypress.Commands.add('apadrinhar', () => {
    cy.visit('/apadrinhar/');
    cy.get('nav > [href="/apadrinhar/"]').click();
    cy.get(':nth-child(1) > .btn-sponsor').click();
    cy.get('.actions > button').click();
    cy.get('[href="/meus_apadrinhados/"]').click();
});

// -- ASSEGURAR QUE O CYPRESS TENHA ACESSO A ESTE ARQUIVO ---------------------
// No cypress.config.js (Cypress 10+), garanta que “supportFile” aponte para este commands.js
