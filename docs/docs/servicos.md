# Serviços

Esta seção descreve os serviços utilizados no backend do Prompt Enricher. Cada serviço é responsável por uma parte específica do processo de enriquecimento de prompts, desde o processamento textual até a consulta e expansão com base em ontologias.

---

## `new_content_service.py`

Este módulo é responsável por gerar frases dinâmicas que expandem o prompt original com base em relacionamentos ontológicos.

### Funções:

- **`expand_prompt(original_prompt, ontology_matches, key_terms, threshold)`**  
  Expande o prompt original gerando frases adicionais baseadas em relacionamentos ontológicos relevantes.

- **`generate_dynamic_phrase(term_a, related_terms, relationship)`**  
  Gera uma frase descritiva baseada no relacionamento entre um termo principal e seus termos relacionados.

- **`pick_relationship_for_type(relation_type)`**  
  Seleciona dinamicamente um tipo de relacionamento textual com base no tipo de relação ontológica (pais, filhos, irmãos, etc.).

---

## `ontology_service.py`

Responsável pela consulta à ontologia OWL e obtenção de informações hierárquicas (pais, filhos, irmãos, ancestrais) sobre os termos.

### Funções:

- **`search_ontology(term, key_terms, threshold, prompt)`**  
  Pesquisa entidades na ontologia relacionadas ao termo fornecido e as filtra com base na relevância semântica.

- **`get_entity_parents(entity)`**  
  Recupera os rótulos das entidades "pais" de uma entidade ontológica.

- **`get_entity_children(entity)`**  
  Recupera os rótulos das entidades "filhos".

- **`get_entity_siblings(entity)`**  
  Recupera os rótulos das entidades "irmãs".

- **`get_entity_ancestors(entity)`**  
  Recupera os rótulos das entidades "ancestrais", removendo duplicatas.

---

## `prompt_service.py`

Camada principal de orquestração do enriquecimento do prompt, integrando os demais serviços.

### Funções:

**`enrich_prompt(promptRequest: PromptRequest)`**  
 Realiza o processo completo de enriquecimento:

1. Extrai termos-chave do prompt.
2. Pesquisa por correspondências ontológicas relevantes com base em diferentes limiares de similaridade.
3. Expande o prompt com base nas entidades encontradas.
4. Retorna o prompt enriquecido, juntamente com detalhes do processo.

---

## `similarity_service.py`

Este módulo é responsável por calcular a similaridade semântica entre os termos do prompt e os rótulos da ontologia.

### Funções:

- **`compute_similarity(term, label)`**  
  Calcula a similaridade de cosseno entre embeddings de um termo e um rótulo.

- **`filter_relevant_terms(similarity_dicts, threshold)`**  
  Filtra os termos mais relevantes com base no limiar de similaridade.

- **`is_prompt_related(label, key_terms, threshold)`**  
  Verifica se um rótulo da ontologia é semanticamente relevante para os termos do prompt.

---

## `text_processing_service.py`

Realiza o processamento linguístico do prompt original para extrair os termos mais significativos.

### Funções:

**`extract_key_terms(prompt)`**  
 Extrai e lematiza os termos-chave do prompt (substantivos, adjetivos e verbos) com base em análise gramatical.
