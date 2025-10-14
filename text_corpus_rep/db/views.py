import numpy as np
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db.models import Q

from .api.CorpusRepository import CorpusRepository
from .api.TextRepository import TextRepository
from .api.embedding_utils import get_embeddings, cos_compare, get_chunks
from .api.ontologyRepository import OntologyRepository
from.onthology_namespace import *
from .models import Test
from core.settings import *

# API IMPORTS
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

# REPO IMPORTS
from db.api.TestRepository import TestRepository

@api_view(['GET', ])
@permission_classes((AllowAny,))
def getTest(request):
    id = request.GET.get('id', None)
    if id is None:
        return HttpResponse(status=400)
    
    testRepo = TestRepository()
    result = testRepo.getTest(id = id)
    return Response(result)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def postTest(request):
    data = json.loads(request.body.decode('utf-8'))
    testRepo = TestRepository()
    test = testRepo.postTest(test_data = data)
    return JsonResponse(test)

@api_view(['DELETE', ])
@permission_classes((AllowAny,))
def deleteTest(request):
    id = request.GET.get('id', None)
    if id is None:
        return HttpResponse(status=400)
    
    testRepo = TestRepository()
    result = testRepo.deleteTest(id = id)
    return Response(result)

# -----------------------
#  CORPUS API
# -----------------------

@api_view(['POST'])
@permission_classes((AllowAny,))
def createCorpus(request):
    data = json.loads(request.body.decode('utf-8'))
    repo = CorpusRepository()
    result = repo.create_corpus(data.get("title"), data.get("description"), data.get("genre"))
    return Response(result)

@api_view(['POST'])
@permission_classes((AllowAny,))
def updateCorpus(request):
    data = json.loads(request.body.decode('utf-8'))
    repo = CorpusRepository()
    result = repo.update_corpus(data["id"], **data)
    return Response(result)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getCorpus(request):
    corpus_id = request.GET.get("id")
    repo = CorpusRepository()
    result = repo.get_corpus(corpus_id)
    return Response(result)

@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteCorpus(request):
    corpus_id = request.GET.get("id")
    repo = CorpusRepository()
    result = repo.delete_corpus(corpus_id)
    return Response(result)

# -----------------------
#  TEXT API
# -----------------------

@api_view(['POST'])
@permission_classes((AllowAny,))
def createText(request):
    data = json.loads(request.body.decode('utf-8'))
    repo = TextRepository()
    result = repo.create_text(
        title=data.get("title"),
        description=data.get("description"),
        text=data.get("text"),
        corpus_id=data.get("corpus_id"),
        has_translation_id=data.get("has_translation")
    )
    return Response(result)

@api_view(['POST'])
@permission_classes((AllowAny,))
def updateText(request):
    data = json.loads(request.body.decode('utf-8'))
    repo = TextRepository()
    result = repo.update_text(data["id"], **data)
    return Response(result)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getText(request):
    text_id = request.GET.get("id")
    repo = TextRepository()
    result = repo.get_text(text_id)
    return Response(result)

@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteText(request):
    text_id = request.GET.get("id")
    repo = TextRepository()
    result = repo.delete_text(text_id)
    return Response(result)

# -----------------------
#  ONTOLOGY API
# -----------------------

@api_view(['GET'])
@permission_classes((AllowAny,))
def getOntology(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    data = repo.get_ontology()
    repo.close()
    return Response(data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def createClass(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    data = json.loads(request.body.decode('utf-8'))
    title = data.get("title")
    description = data.get("description")
    parent_uri = data.get("parent_uri")
    result = repo.create_class(title, description, parent_uri)
    repo.close()
    return Response(result)


@api_view(['GET'])
@permission_classes((AllowAny,))
def getClass(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    uri = request.GET.get("uri")
    result = repo.get_class(uri)
    repo.close()
    return Response(result)


@api_view(['POST'])
@permission_classes((AllowAny,))
def createObject(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    data = json.loads(request.body.decode('utf-8'))
    class_uri = data.get("class_uri")
    title = data.get("title")
    description = data.get("description")
    result = repo.create_object(class_uri, title, description)
    repo.close()
    return Response(result)


@api_view(['GET'])
@permission_classes((AllowAny,))
def getSignature(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    uri = request.GET.get("uri")
    result = repo.collect_signature(uri)
    repo.close()
    return Response(result)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteClass(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    uri = request.GET.get("uri")
    result = repo.delete_class(uri)
    repo.close()
    return Response({"deleted": result})


@api_view(['GET'])
@permission_classes((AllowAny,))
def getClassParents(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    uri = request.GET.get("uri")
    result = repo.get_class_parents(uri)
    repo.close()
    return Response(result)


@api_view(['GET'])
@permission_classes((AllowAny,))
def getClassChildren(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    uri = request.GET.get("uri")
    result = repo.get_class_children(uri)
    repo.close()
    return Response(result)


@api_view(['GET'])
@permission_classes((AllowAny,))
def getClassObjects(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    uri = request.GET.get("uri")
    result = repo.get_class_objects(uri)
    repo.close()
    return Response(result)


@api_view(['POST'])
@permission_classes((AllowAny,))
def updateClass(request):
    data = json.loads(request.body.decode('utf-8'))
    uri = data.get("uri")
    title = data.get("title")
    description = data.get("description")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    result = repo.update_class(uri, title, description)
    repo.close()
    return Response(result)


@api_view(['POST'])
@permission_classes((AllowAny,))
def addClassAttribute(request):
    data = json.loads(request.body.decode('utf-8'))
    class_uri = data.get("class_uri")
    attr_name = data.get("attr_name")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    result = repo.add_class_attribute(class_uri, attr_name)
    repo.close()
    return Response(result)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteClassAttribute(request):
    prop_uri = request.GET.get("uri")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    result = repo.delete_class_attribute(prop_uri)
    repo.close()
    return Response({"deleted": result})


@api_view(['POST'])
@permission_classes((AllowAny,))
def addClassObjectAttribute(request):
    data = json.loads(request.body.decode('utf-8'))
    class_uri = data.get("class_uri")
    attr_name = data.get("attr_name")
    range_class_uri = data.get("range_class_uri")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    result = repo.add_class_object_attribute(class_uri, attr_name, range_class_uri)
    repo.close()
    return Response(result)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteClassObjectAttribute(request):
    prop_uri = request.GET.get("uri")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    result = repo.delete_class_object_attribute(prop_uri)
    repo.close()
    return Response({"deleted": result})


@api_view(['POST'])
@permission_classes((AllowAny,))
def addClassParent(request):
    data = json.loads(request.body.decode('utf-8'))
    parent_uri = data.get("parent_uri")
    target_uri = data.get("target_uri")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    repo.add_class_parent(parent_uri, target_uri)
    repo.close()
    return Response({"added": True})


@api_view(['GET'])
@permission_classes((AllowAny,))
def getObject(request):
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    object_uri = request.GET.get("uri")
    result = repo.get_object(object_uri)
    repo.close()
    return Response(result)


@api_view(['POST'])
@permission_classes((AllowAny,))
def updateObject(request):
    data = json.loads(request.body.decode('utf-8'))
    object_uri = data.get("uri")
    title = data.get("title")
    description = data.get("description")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    result = repo.update_object(object_uri, title, description)
    repo.close()
    return Response(result)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteObject(request):
    object_uri = request.GET.get("uri")
    repo = OntologyRepository(DB_URI, DB_USER, DB_PASSWORD)
    result = repo.delete_object(object_uri)
    repo.close()
    return Response({"deleted": result})

# -----------------------
#  EMBEDDING API
# -----------------------

@api_view(['POST'])
@permission_classes((AllowAny,))
def build_embeddings(request):
    """
    Получает текст(ы), возвращает эмбеддинги.
    """
    data = json.loads(request.body.decode('utf-8'))
    texts = data.get("texts", [])
    embeddings = get_embeddings(texts)
    return Response({"embeddings": embeddings.tolist()})

@api_view(['POST'])
@permission_classes((AllowAny,))
def compare_embeddings(request):
    """
    Сравнивает два эмбеддинга по косинусному сходству.
    """
    data = json.loads(request.body.decode('utf-8'))
    emb1 = np.array(data["emb1"])
    emb2 = np.array(data["emb2"])
    similarity = cos_compare(emb1, emb2)
    return Response({"similarity": similarity})

@api_view(['POST'])
@permission_classes((AllowAny,))
def chunk_text(request):
    """
    Разбивает текст на чанки.
    """
    data = json.loads(request.body.decode('utf-8'))
    text = data.get("text", "")
    chunks = get_chunks(text)
    return Response({"chunks": chunks})