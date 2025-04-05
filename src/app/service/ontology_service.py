import owlready2
from owlready2 import get_ontology
from app.service.similarity_service import compute_similarity, is_prompt_related

ontology_path = "public/ontology/MFOEM.owl"
onto = get_ontology(ontology_path).load()

def search_ontology(term, key_terms, threshold, prompt):
    """
    Searches the ontology for entities related to the given term and filters them based on relevance.

    Args:
        term (str): The term to search for in the ontology.
        key_terms (list): A list of key terms extracted from the prompt.
        threshold (float): The similarity threshold for filtering relevant entities.
        prompt (str): The original prompt provided by the user.

    Returns:
        list: A list of dictionaries containing information about the matched ontology entities,
              including their parents, children, siblings, and ancestors with similarity scores.
    """
    results = []
    for entity in onto.classes():
        labels = entity.label or []  # Garantir que entity.label seja iterável
        for label in labels:
            # Verificar relação entre o termo e o rótulo
            if term.lower() in label.lower() and is_prompt_related(label, key_terms, threshold):
                entity_parents = get_entity_parents(entity)
                entity_children = get_entity_children(entity)
                entity_siblings = get_entity_siblings(entity)
                entity_ancestors = get_entity_ancestors(entity)

                # Calculate similarity for each relationship
                # Convert locstr to plain strings
                parent_similarities = [
                    {"term": str(parent), "similarity": float(compute_similarity(prompt, str(parent)))}
                    for parent in entity_parents
                ]
                child_similarities = [
                    {"term": str(child), "similarity": float(compute_similarity(prompt, str(child)))}
                    for child in entity_children
                ]
                sibling_similarities = [
                    {"term": str(sibling), "similarity": float(compute_similarity(prompt, str(sibling)))}
                    for sibling in entity_siblings
                ]
                ancestor_similarities = [
                    {"term": str(ancestor), "similarity": float(compute_similarity(prompt, str(ancestor)))}
                    for ancestor in entity_ancestors
                ]

                results.append({
                    "identifier": entity.name,
                    "label": label,
                    "parents": parent_similarities,
                    "children": child_similarities,
                    "siblings": sibling_similarities,
                    "ancestors": ancestor_similarities,
                })
    return results

def get_entity_parents(entity):
    """
    Retrieves the parent entities of the given ontology entity.

    Args:
        entity (owlready2.ThingClass): The ontology entity for which to retrieve parents.

    Returns:
        list: A list of parent labels (strings) for the given entity.
    """
    parents = []
    for parent in entity.is_a:
        if isinstance(parent, owlready2.ThingClass) and parent.label:
            parents.extend(parent.label)  # 'label' pode ser uma lista
    return parents

def get_entity_children(entity):
    """
    Retrieves the child entities of the given ontology entity.

    Args:
        entity (owlready2.ThingClass): The ontology entity for which to retrieve children.

    Returns:
        list: A list of child labels (strings) for the given entity.
    """
    children = []
    for child in entity.subclasses():
        if child.label:
            children.extend(child.label)
    return children

def get_entity_siblings(entity):
    """
    Retrieves the sibling entities of the given ontology entity.

    Args:
        entity (owlready2.ThingClass): The ontology entity for which to retrieve siblings.

    Returns:
        list: A list of sibling labels (strings) for the given entity.
    """
    siblings = []
    for parent in entity.is_a:
        if isinstance(parent, owlready2.ThingClass):
            for child in parent.subclasses():
                if child != entity and child.label:
                    siblings.extend(child.label)
    return siblings

def get_entity_ancestors(entity):
    """
    Retrieves the ancestor entities of the given ontology entity.

    Args:
        entity (owlready2.ThingClass): The ontology entity for which to retrieve ancestors.

    Returns:
        list: A list of ancestor labels (strings) for the given entity, with duplicates removed.
    """
    ancestors = []
    for parent in entity.is_a:
        if isinstance(parent, owlready2.ThingClass):
            ancestors.extend(parent.label or [])
            # Recursivamente buscar ancestrais
            ancestors.extend(get_entity_ancestors(parent))
    return list(set(ancestors))  # Remover duplicatas
