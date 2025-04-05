# Endpoints da API

## `POST /enrich_prompt`

Esse endpoint recebe um prompt enviado pelo usuário e aplica uma série de técnicas de enriquecimento semântico baseadas em **ontologias** e **extração de termos-chave**, com níveis variáveis de **precisão semântica**.

---

### 📥 Requisição

**Método:** `POST`  
**URL:** `/enrich_prompt`  
**Content-Type:** `application/json`

#### 🔹 Corpo da requisição:

| Campo       | Tipo   | Descrição                                                                                                                                   |
| ----------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt`    | string | Texto enviado pelo usuário a ser enriquecido                                                                                                |
| `precision` | string | Nível de precisão semântica desejado: `very_low_precision`, `low_precision`, `medium_precision`, `high_precision`, ou `very_high_precision` |

#### Exemplo:

```json
{
  "prompt": "How can someone cope with sadness after a significant loss?",
  "precision": "medium_precision"
}
```

---

### 📤 Resposta

A resposta varia de acordo com o sucesso ou não do enriquecimento.

---

#### ✅ Exemplo de resposta com sucesso:

```json
{
  "Status": "Prompt enriched!",
  "Message": "The ontology matches were relevant enough for enrichment!",
  "Original Prompt": "How can someone cope with sadness after a significant loss?",
  "Enriched Prompt": "How can someone cope with sadness after a significant loss? The relationship between sadness and grief might offer new perspectives. Altogether, these relationships could enrich our understanding of the underlying concepts.",
  "Threshold used": 0.6,
  "Precision level used": "medium_precision",
  "Key terms": ["loss", "significant", "cope", "sadness"],
  "Ontology matches": {
    "loss": [
      {
        "identifier": "MFOEM_000106",
        "label": "appraisal of loss",
        "parents": [
          {
            "term": "appraisal",
            "similarity": 0.03448363021016121
          }
        ],
        "children": [],
        "siblings": [
          {
            "term": "appraisal of suddenness",
            "similarity": 0.1623242348432541
          }
        ],
        "ancestors": [
          {
            "term": "representation",
            "similarity": 0.008483306504786015
          }
        ]
      }
    ],
    "significant": [],
    "cope": [],
    "sadness": [
      {
        "identifier": "MFOEM_000056",
        "label": "sadness",
        "parents": [
          {
            "term": "emotion process",
            "similarity": 0.24776813387870789
          }
        ],
        "children": [],
        "siblings": [
          {
            "term": "anger",
            "similarity": 0.16203878819942474
          }
        ],
        "ancestors": [
          {
            "term": "emotion process",
            "similarity": 0.24776813387870789
          }
        ]
      }
    ]
  }
}
```

---

#### ❌ Exemplo de resposta sem enriquecimento:

```json
{
  "Status": "Prompt not enriched!",
  "Message": "The ontology matches were not relevant enough for enrichment!",
  "Original Prompt": "How can someone cope with sadness after a significant loss?",
  "Enriched Prompt": "How can someone cope with sadness after a significant loss?",
  "Threshold used": null,
  "Precision level used": "very_high_precision",
  "Key terms": ["loss", "significant", "cope", "sadness"],
  "Ontology matches": {
    "loss": [
      {
        "identifier": "MFOEM_000106",
        "label": "appraisal of loss",
        "parents": [
          {
            "term": "appraisal",
            "similarity": 0.03448363021016121
          }
        ],
        "children": [],
        "siblings": [
          {
            "term": "appraisal of suddenness",
            "similarity": 0.1623242348432541
          }
        ],
        "ancestors": [
          {
            "term": "representation",
            "similarity": 0.008483306504786015
          }
        ]
      }
    ],
    "significant": [],
    "cope": [],
    "sadness": [
      {
        "identifier": "MFOEM_000056",
        "label": "sadness",
        "parents": [
          {
            "term": "emotion process",
            "similarity": 0.24776813387870789
          }
        ],
        "children": [],
        "siblings": [
          {
            "term": "anger",
            "similarity": 0.16203878819942474
          }
        ],
        "ancestors": [
          {
            "term": "emotion process",
            "similarity": 0.24776813387870789
          }
        ]
      }
    ]
  }
}
```

---

### ⚙️ Lógica interna (resumo técnico)

1. **Extração de termos-chave:**  
   O serviço analisa o prompt e extrai palavras relevantes.

2. **Consulta à ontologia:**  
   Para cada termo, busca conceitos relacionados na ontologia MFOEM, a Emotion Ontology, considerando a **precisão** escolhida.

3. **Expansão do prompt:**  
   Se forem encontrados resultados relevantes, o prompt original é reformulado para incluir essas informações.

4. **Iteração por níveis de threshold:**  
   A API tenta enriquecer o prompt usando os thresholds definidos para o nível de precisão. Se algum nível for satisfatório, retorna o prompt enriquecido.

---

### 🎯 Possíveis valores de `precision`

| Nível                 | Thresholds usados         |
| --------------------- | ------------------------- |
| `very_low_precision`  | `[0.2, 0.15, 0.1, 0.05]`  |
| `low_precision`       | `[0.4, 0.35, 0.3, 0.25]`  |
| `medium_precision`    | `[0.6, 0.55, 0.5, 0.45]`  |
| `high_precision`      | `[0.8, 0.75, 0.7, 0.65]`  |
| `very_high_precision` | `[0.99, 0.95, 0.9, 0.85]` |

---

### 📌 Observações

- Se nenhum nível de precisão gerar um resultado considerado enriquecido, a resposta mantém o prompt original.
- O enriquecimento é orientado pela ontologia, o que garante alinhamento com conhecimento estruturado e atualizado.
