"""Technitium Dns ontology contribution (CONCEPT:AU-KG.ontology.federation-provider-leg).

Data-only subpackage: it carries ``technitium.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/technitium`` module) which the scion-sdk hub federates in via
the ``scion_sdk.ontology_providers`` entry-point. It holds no business logic
and no heavy imports so the hub can resolve it cheaply.
"""
