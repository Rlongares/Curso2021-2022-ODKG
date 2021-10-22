# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wN4xHrqpix-5QvIdSbYhvU76SjW85AoJ

**Task 08: Completing missing data**
"""

#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

print('Grafo 1')
for s,p,o in g1:
  print(s,p,o)

print('Grafo 2')
for s,p,o in g2:
  print(s,p,o)

ns = Namespace('http://data.org#')
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""

# q2 = prepareQuery('''
#   SELECT ?val WHERE {
#     ?Person VCARD:Family ?val
#   }
#   ''',
#   initNs = { "VCARD": VCARD}
# )

# # for s,p,o in g2.triples((ns.JohnDoe,VCARD.Family, None)):
# #   print(s,p,o)
# for q in g2.query(q2, initBindings={'?Person': ns.JohnDoe}):
#   print(q)

# Persons in data01
q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Class rdfs:subClassOf* ?Person.
    ?Subject rdf:type ?Class
  }
  ''',
  initNs = { "rdfs": RDFS, "rdf": RDF}
)

# Query of Given, Family, email
q2 = prepareQuery('''
  SELECT ?val WHERE {
    ?Person ?vcard ?val
  }
  '''
)

info = ['Given','Family','EMAIL']

# Insert the remaining information
for r in g1.query(q1, initBindings = {'?Person' : ns.Person}):
  # print(r[0])
  for i in info:
    for q in g2.query(q2, initBindings={'?Person': r[0], '?vcard': VCARD[i]}):
      g1.add((r[0],VCARD[i],q[0]))

print('Grafo 1')
for s,p,o in g1:
  print(s,p,o)