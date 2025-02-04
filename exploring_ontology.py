from owlready2 import get_ontology

# Carregando a ontologia
ontology_path = "public/ontology/MFOEM.owl"
onto = get_ontology(ontology_path).load()

def search_ontology(term):
    # Buscar a classe pelo nome do termo
    term_class = onto.search(label=term)
    
    # Verificar se encontramos a classe
    if term_class:
        for cls in term_class:
            print(f"Classe: {cls.label[0]}")
            # Mostrar os pais (hierarquia) da classe encontrada
            if hasattr(cls, 'is_a'):
                print(cls.is_a)
                for parent in cls.is_a:
                    print(f"  É uma subclasse de: {parent}")
            else:
                print("Não há informação hierárquica para essa classe.")
    else:
        print(f"Termo '{term}' não encontrado na ontologia.")


results = search_ontology("stress")
for result in results:
    print(f"Identifier: {result['identifier']}, Label: {result['label']}")
