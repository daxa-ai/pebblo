def describe_pebblo_semantic_stats(documents: list) -> None:
    """
    Describe the semantic stats of the documents
    """
    unique_identities = set()
    unique_topics = set()
    unique_entities = set()

    for doc in documents:
        unique_identities.update(doc.metadata.get("authorized_identities", []))
        unique_topics.update(doc.metadata.get("pebblo_semantic_topics", []))
        unique_entities.update(doc.metadata.get("pebblo_semantic_entities", []))

    print("\nIndentity and Semantic Stats:")
    print(f"Authorized Identities: {list(unique_identities)}")
    print(f"Semantic Topics: {list(unique_topics)}")
    print(f"Semantic Entities: {list(unique_entities)}")
    print("\n")
