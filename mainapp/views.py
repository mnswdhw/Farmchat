import json
import boto3
import numpy
from botocore.exceptions import NoCredentialsError
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import *
from .predictor import get_disease_from_label as predictor_2
from .predictor import image_to_symptoms as predictor


# ACCESS_KEY = 'AKIAU4IITNHAKQT7VN65'
# SECRET_KEY = '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'


# session = boto3.Session(
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY
# )



class image():
    def UploadImage(name, image, labels):
        filename = name
        imagedata = image
        s3 = boto3.resource('s3')
        try:
            data = open(f'/home/manas/Desktop/courses/csd/ai-farmbot-backend/ai-farmbot-backend/farmbotbackend/media/assets/{name}', 'rb')
            s3.Bucket('killshotsheenu').put_object(Key=f'{name}', Body=data)

            #store the image link in the database along with the predicted captions 

            s3_link = f"https://killshotsheenu.s3.amazonaws.com/{name}"
            return s3_link
        except Exception as e:
            return e

# Create your views here.


@csrf_exempt  # To exempt from default requirement for CSRF tokens to use postman
def TheModelView(request):

    if (request.method == "POST"):
        # Turn the body into a dict
        # body = json.loads(request.body.decode("utf-8"))

        # labels = predictor(body)

        # # Turn the object to json to dict, put in array to avoid non-iterable error
        # # send json response with new object
        # return JsonResponse(labels, safe=False)
        f = request.FILES['sentFile']
        # data = request.FILES['image'] # or self.files['image'] in your form

        path = default_storage.save(f'/home/manas/Desktop/courses/csd/ai-farmbot-backend/ai-farmbot-backend/farmbotbackend/media/assets/{f.name}', ContentFile(f.read()))

        print("Local file path:",path)

        img = Image.open(f)
        np_img = numpy.array(img)
        labels = predictor(np_img)
        s3_link = image.UploadImage(f.name, f, labels)

        #remove start and end from the predicted labels
        pred_symp = labels["symptoms"]
        pred_symp = pred_symp[1:-1]
        
        labels["symptoms"] = pred_symp

        default_storage.delete(path)

        #save the s3 image link in the database
        imgobjectadded = ImgData(s3link = s3_link)
        imgobjectadded.save()
       
        to_send = {"labels":labels, "s3link":s3_link}

        return JsonResponse(to_send, safe=False)


@csrf_exempt
def TheModelView2(request):

    if (request.method == "POST"):
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))

        # print("HELLO", body)
        s3_link = body["s3_link"]
        corrected_symptoms = body["symptoms"]
        corrected_symptoms=','.join(corrected_symptoms)
        a_to_t = body["a2t"]
        a = ImgData.objects.filter(s3link=s3_link)
        for x in a:
            x.captions_user=corrected_symptoms
            x.audio_text=a_to_t
            x.save()
        
        diseases = predictor_2(body)

        #also return the images of the disease

        # print(diseases)

        d_1 = diseases[0]
        d_2 = diseases[1]

        a = Reference.objects.filter(disease=d_1)
        for x in a:
            img_d1 = x.image_url
        a = Reference.objects.filter(disease=d_2)
        for x in a:
            img_d2 = x.image_url




        return JsonResponse({"first":[d_1,img_d1],"second":[d_2,img_d2]}, safe=False)


@csrf_exempt
def AddReview(request):

    if (request.method == "POST"):
        # Turn the body into a dict
        reviewObj = json.loads(request.body.decode("utf-8"))
        reviewObjAdded = Review(rating=int(
            reviewObj["rating"]), user_review=reviewObj["user_review"])

        reviewObjAdded.save()

        # Turn the object to json to dict, put in array to avoid non-iterable error
        # send json response with new object
        return JsonResponse({"message": "Review added successfully"}, safe=False)


@csrf_exempt
def AddExpert(request):

    if (request.method == "POST"):
        # Turn the body into a dict
        expObj = json.loads(request.body.decode("utf-8"))

        # print("Hello",expObj)
        expObjAdded = Expert(name=expObj["name"], email=expObj["email"],
                             phone=expObj["phone"], qualification=expObj["qualification"])

        expObjAdded.save()

        # Turn the object to json to dict, put in array to avoid non-iterable error
        # send json response with new object
        return JsonResponse({"message": "Expert added successfully"}, safe=False)


@csrf_exempt
def AddReference(request):

    if (request.method == "POST"):
        # Turn the body into a dict
        refObj = json.loads(request.body.decode("utf-8"))
        refObjAdded = Reference(
            captions=refObj["captions"], image_url=refObj["image_url"])

        refObjAdded.save()

        # Turn the object to json to dict, put in array to avoid non-iterable error
        # send json response with new object
        return JsonResponse({"message": "Reference added successfully"}, safe=False)


@csrf_exempt
def AddImgData(request):

    if (request.method == "POST"):
        # Turn the body into a dict
        imgObj = json.loads(request.body.decode("utf-8"))
        imgObjAdded = ImgData(
            captions_user=imgObj["captions_user"], s3link=imgObj["s3link"], audio_text=imgObj["audio_text"])

        imgObjAdded.save()

        # Turn the object to json to dict, put in array to avoid non-iterable error
        # send json response with new object
        return JsonResponse({"message": "Image data added successfully"}, safe=False)
