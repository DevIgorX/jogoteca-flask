# [WEB + FLASK] Jogoteca: Gerenciador de Biblioteca de Jogos

Aplicação web desenvolvida em **Python (Flask)** para gerenciar uma coleção pessoal de videogames. O sistema permite o cadastro, edição, visualização e exclusão de títulos, incluindo upload de imagens de capa e um sistema seguro de autenticação de usuários.

---

## 🔗 Funcionalidades

### 1. Autenticação e Segurança de Usuários
* O sistema possui uma rota de login robusta que verifica credenciais no banco de dados. As senhas são armazenadas utilizando **Hash (Bcrypt)**, garantindo que não fiquem expostas em texto puro.
* **Impacto:** Garante a segurança dos dados dos usuários e impede acessos não autorizados à área administrativa, protegendo a integridade da coleção.

### 2. Gestão de Conteúdo (CRUD Completo)
* Permite criar novos registros de jogos (Nome, Categoria, Console), editar informações existentes e deletar jogos que não fazem mais parte da coleção.
* **Impacto:** Centraliza a organização da biblioteca em um único lugar, substituindo planilhas ou anotações manuais por uma interface web intuitiva e responsiva.

### 3. Upload e Gerenciamento de Mídia
* Integração com o sistema de arquivos para permitir o upload de capas personalizadas para cada jogo. O sistema gerencia nomes de arquivos para evitar conflitos e exibe uma imagem padrão caso nenhuma seja enviada.
* **Impacto:** Melhora drasticamente a experiência do usuário (UX) através da identificação visual rápida dos títulos na listagem.

### 4. Validação de Dados e Proteção
* Utiliza **Flask-WTF** para a criação de formulários com validação no lado do servidor e proteção contra ataques CSRF (Cross-Site Request Forgery).
* **Impacto:** Assegura que apenas dados válidos entrem no banco de dados e protege a aplicação contra vulnerabilidades web comuns.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **Flask:** Framework web principal.
* **Werkzeug:** Biblioteca WSGI utilitária para Python (base do Flask).
* **Flask-SQLAlchemy:** ORM para interação com banco de dados SQLite.
* **Flask-WTF:** Manipulação e validação de formulários.
* **Flask-Bcrypt:** Criptografia de senhas.
* **Bootstrap 5:** Estilização e responsividade do frontend.

---

## 🚀 Forma de execução em ambiente de Desenvolvimento

Certifique-se de ter o Python instalado.

### 1. Instalação das dependências

```bash
# Instale as bibliotecas necessárias
pip install flask werkzeug flask-sqlalchemy flask-wtf flask-bcrypt
