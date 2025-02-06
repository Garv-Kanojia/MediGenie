import io
import requests
from PIL import Image
from django.shortcuts import render , redirect
from .forms import ImageUploadForm, ImageURLForm
from model.pretrained import model
import torch
from torchvision import transforms

def index(request):
    return render(request , 'index.html')

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])
    ])
    
    image = transform(image).unsqueeze(0)
    return image

def predict_image(image):
    model.eval()
    with torch.no_grad():
        output = model(image)
        predictions = torch.sigmoid(output)
        probabilities = predictions.cpu().numpy()
    return probabilities

def handle_image(image_file):
    image = Image.open(image_file).convert('L')
    image_array = preprocess_image(image)
    predictions = predict_image(image_array)
    return predictions

def handle_image_url(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content)).convert("L")
    image_array = preprocess_image(image)
    predictions = predict_image(image_array)
    return predictions

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            predictions = handle_image(image_file)
            predicted_labels = (predictions >= 0.2).astype(int)  # Threshold for prediction is 0.5
            # print(predictions[0])
            

            labels = ['Cardiomegaly', 'Emphysema', 'Effusion', 'Hernia', 'Infiltration', 'Mass', 'Nodule',
                      'Atelectasis', 'Pneumothorax', 'Pleural_Thickening', 'Pneumonia', 'Fibrosis', 'Edema', 'Consolidation']
            
            # Zip labels and predictions
            prediction_list = list(zip(labels, predictions[0]))
            prediction_list2 = list(zip(labels, predicted_labels))
            # print(prediction_list)
            # print(prediction_list2)

            # Filter predictions above threshold (0.5) and sort them by probability in descending order
            significant_predictions = [(label, prob) for label, prob in prediction_list if prob > 0.2]
            significant_predictions.sort(key=lambda x: x[1], reverse=True)

            if len(significant_predictions) == 0:  # No diseases above the threshold
                result = 'No significant findings'
                top_predictions = []
            else:
                # Collect the top 4 predictions
                top_predictions = significant_predictions
                result = 'The Patient may be suffering from '

            # Pass result and top predictions to the context
            context = {'predictions': result, 'top_predictions': [(label, round(prob * 100, 2)) for label, prob in top_predictions]}
            return render(request, 'results.html', context)
    
    return redirect('index')


def url_image(request):
    if request.method == 'POST':
        form = ImageURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['image_url']
            predictions = handle_image_url(url)
            predicted_labels = (predictions >= 0.2).astype(int)

            labels = ['Cardiomegaly', 'Emphysema', 'Effusion', 'Hernia', 'Infiltration', 'Mass', 'Nodule',
                      'Atelectasis', 'Pneumothorax', 'Pleural_Thickening', 'Pneumonia', 'Fibrosis', 'Edema', 'Consolidation']
            
            # Zip labels and predictions
            prediction_list = list(zip(labels, predictions[0]))
            prediction_list2 = list(zip(labels, predicted_labels))
            # print(prediction_list)
            # print(prediction_list2)

            # Filter predictions above threshold (0.2) and sort by probability in descending order
            significant_predictions = [(label, prob) for label, prob in prediction_list if prob > 0.2]
            significant_predictions.sort(key=lambda x: x[1], reverse=True)

            if len(significant_predictions) == 0:  # No diseases above the threshold
                result = 'No significant findings'
                top_predictions = []
            else:
                # Collect the top 4 predictions
                top_predictions = significant_predictions
                result = 'The Patient may be suffering from '

            # Pass result and top predictions to the context
            context = {'predictions': result, 'top_predictions': [(label, round(prob * 100, 2)) for label, prob in top_predictions]}
            return render(request, 'results.html', context)
        
    return redirect('index')
