# Estrutura do Projeto

Esta seção descreve a organização do projeto de backend utilizado para o sistema de enriquecimento de prompts baseado em ontologias e linguagem natural.

---

## 📁 Estrutura de Diretórios

```
/public
  └── ontology/
      └── MFOEM.owl
/src
  └── app/
      ├── controller/
      │   └── prompt_controller.py
      ├── service/
      │   ├── new_content_service.py
      │   ├── ontology_service.py
      │   ├── prompt_service.py
      │   ├── similarity_service.py
      │   └── text_processing_service.py
      └── main.py
requirements.txt
README.md
.gitignore
```

---

## 🧭 Descrição das Pastas e Arquivos

### `/public/ontology/`

- **MFOEM.owl**: Arquivo de ontologia utilizado para enriquecer semanticamente os prompts. Essa ontologia contém conceitos e relações estruturadas relevantes ao domínio de interesse.

---

### `/src/app/`

#### 🔹 `main.py`

- Ponto de entrada da aplicação FastAPI. Responsável por inicializar a API, importar as rotas e configurar o servidor.

#### 🔹 `/controller/prompt_controller.py`

- Define os endpoints da aplicação. No momento, possui o endpoint `POST /enrich_prompt`, que processa o prompt enviado e retorna o resultado enriquecido.

#### 🔹 `/service/`

Contém os serviços responsáveis pela lógica de negócio do sistema:

- **`new_content_service.py`**: Responsável por montar o novo prompt com base nos termos encontrados na ontologia.
- **`ontology_service.py`**: Realiza a consulta à ontologia, buscando termos semelhantes aos extraídos do prompt.
- **`prompt_service.py`**: Serviço principal que orquestra todo o processo de enriquecimento, desde a extração de termos até o retorno do novo prompt.
- **`similarity_service.py`**: Implementa funções de similaridade semântica entre termos, utilizada para validar os conceitos da ontologia.
- **`text_processing_service.py`**: Responsável por pré-processar o prompt e extrair os termos-chave para busca semântica.

---

## 📄 Arquivos na raiz

- **`requirements.txt`**: Lista as dependências do projeto. Pode ser utilizado para instalação com `pip install -r requirements.txt`.

- **`README.md`**: Documento com instruções iniciais do projeto.

- **`.gitignore`**: Define arquivos e pastas que devem ser ignorados pelo Git, como ambientes virtuais, arquivos temporários etc.

---

## ✅ Considerações

A estrutura do projeto segue boas práticas de separação de responsabilidades, com módulos bem definidos para controle, lógica de negócio e manipulação de dados. Essa organização facilita a manutenção, testes e extensão do sistema.
