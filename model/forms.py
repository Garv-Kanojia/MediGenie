from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(required=False, help_text="Upload an image file.")

class ImageURLForm(forms.Form):
    image_url = forms.URLField(required=False, help_text="Or provide an image URL.")
