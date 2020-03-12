from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from google.cloud import translate_v2 as translate
from django.core.cache import cache
from translation_project.celery import app

def home(request):
    return HttpResponse("Translation")
    
# async method to get translation of a text
@app.task
def async_translate_text(text, target_lang):
    translate_client = translate.Client()
    translated_text = translate_client.translate(text,target_language=target_lang)
    return translated_text


#translate from source language to tagret language
@api_view(['POST'])
def translation(request):

    if request.method == 'POST':

        text = 'welcome'
        target_lang = 'de'

        # if the text cached , it will return the first text (germany text)
        if cache.get(text):
            print("Cached")
            # this will return cache version 1 ==> germany text
            #return Response({'germany_text':cache.get(text)})

            # this will return cache version 2 ==> japanese text
            #return Response({'japanese_text':cache.get(text,version=2)})

            # this will return cache version 3 ==> french text
            #return Response({'french_text': cache.get(text,version=3)})

            # this will return all translated text
            return Response({'germany_text':cache.get(text), 'japanese_text':cache.get(text,version=2),'french_text':cache.get(text,version=3)})
        
        translate_client = translate.Client()
        
        output = translate_client.translate(text,target_language=target_lang)
        # cache translated text to germany
        cache.set(text,output)
        japanese_text = async_translate_text.delay(text,'ja').get()
        french_text = async_translate_text.delay(text,'fr').get()
        # cache translated text to japanese
        cache.set(text,japanese_text,version=2)
        # cache translated text to french
        cache.set(text,french_text, version=3)
        # printing germany text
        print(cache.get(text))
        # printing japanese text
        print(cache.get(text,version=2))
        # printing french text
        print(cache.get(text,version=3))
        # return 3 texts
        return Response({'output':output,'japanese':japanese_text,'french':french_text})




    






