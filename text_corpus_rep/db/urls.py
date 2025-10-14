from django.urls import path
from django.conf.urls import url

from db.views import (
    getTest,
    postTest,
    deleteTest,

    createCorpus,
    updateCorpus,
    getCorpus,
    deleteCorpus,

    createText,
    updateText,
    getText,
    deleteText,

    getOntology,
    getClass,
    createClass,
    deleteClass,
    createObject,
    getSignature,
    getClassParents,
    getClassChildren,
    getClassObjects,
    updateClass,
    addClassParent,
    addClassAttribute,
    deleteClassAttribute,
    addClassObjectAttribute,
    deleteClassObjectAttribute,
    getObject,
    updateObject,
    deleteObject,

    build_embeddings,
    compare_embeddings,
    chunk_text,
)

urlpatterns = [
    path('getTest',getTest , name='getTest'),
    path('postTest',postTest , name='postTest'),
    path('deleteTest',deleteTest , name='deleteTest'),

    # Corpus
    path('corpus/create/', createCorpus, name='createCorpus'),
    path('corpus/update/', updateCorpus, name='updateCorpus'),
    path('corpus/', getCorpus, name='getCorpus'),
    path('corpus/delete/', deleteCorpus, name='deleteCorpus'),

    # Text
    path('text/create/', createText, name='createText'),
    path('text/update/', updateText, name='updateText'),
    path('text/', getText, name='getText'),
    path('text/delete/', deleteText, name='deleteText'),

    # Ontology
    path('ontology/', getOntology, name='getOntology'),
    path('ontology/class/', getClass, name='getClass'),
    path('ontology/class/create/', createClass, name='createClass'),
    path('ontology/class/delete/', deleteClass, name='deleteClass'),
    path('ontology/object/create/', createObject, name='createObject'),
    path('ontology/signature/', getSignature, name='getSignature'),
    path('ontology/class/parents/', getClassParents, name='getClassParents'),
    path('ontology/class/children/', getClassChildren, name='getClassChildren'),
    path('ontology/class/objects/', getClassObjects, name='getClassObjects'),
    path('ontology/class/update/', updateClass, name='updateClass'),
    path('ontology/class/parent/add/', addClassParent, name='addClassParent'),
    path('ontology/class/attribute/add/', addClassAttribute, name='addClassAttribute'),
    path('ontology/class/attribute/delete/', deleteClassAttribute, name='deleteClassAttribute'),
    path('ontology/class/object-attribute/add/', addClassObjectAttribute, name='addClassObjectAttribute'),
    path('ontology/class/object-attribute/delete/', deleteClassObjectAttribute, name='deleteClassObjectAttribute'),
    path('ontology/object/', getObject, name='getObject'),
    path('ontology/object/update/', updateObject, name='updateObject'),
    path('ontology/object/delete/', deleteObject, name='deleteObject'),

    # Embedding
    path('embeddings/build/', build_embeddings, name='build_embeddings'),
    path('embeddings/compare/', compare_embeddings, name='compare_embeddings'),
    path('embeddings/chunk/', chunk_text, name='chunk_text'),
]