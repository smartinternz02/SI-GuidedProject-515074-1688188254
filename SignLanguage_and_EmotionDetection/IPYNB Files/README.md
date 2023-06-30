# IPYNB files for Training of our Emotion and Sign language Detection model
This repository contains the IPYNB files used for training our Emotion and Sign Language Detection models. The training process involved utilizing Convolutional Neural Networks (CNN) and employing a diverse dataset for training, validation, and testing purposes.

* Our Emotion Detection model takes an image as input and predicts its belonging to one of the six classes: 'Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sadness', and 'Surprise'. By leveraging CNN architecture, our model achieves accurate emotion classification.

* Similarly, our Sign Language Detection model operates by accepting an image as input and identifying landmarks on the user's hands, using the `mediapipe` library. These landmarks are then processed by our model, which accurately predicts the corresponding American Alphabet character depicted by the user's hand gestures.

Through this repository, we showcase our professional approach in training these models, leveraging advanced techniques and datasets to achieve reliable results in both Emotion and Sign Language Detection.

# Datasets Used


We utilized the following datasets for our project:

* **Emotion Detection**: We used the Emotion Detection dataset available at this [Kaggle link](https://www.kaggle.com/datasets/ananthu017/emotion-detection-fer). It provides a comprehensive collection of images labeled with different emotions, enabling us to train our Emotion Detection model effectively.

* **Sign Language Detection**: For our Sign Language Detection model, we created our own dataset. Using OpenCV, we recorded frames capturing various hand signs representing the American Hand Sign language letters. This custom dataset allowed us to train our model specifically for accurate Sign Language Detection.

To access the datasets, please visit the following Google Drive link: [Google Drive Link](https://drive.google.com/drive/folders/1p3QviZMkpTyyijICqSa0K4QFP7RoQf-H?usp=sharing). It provides access to the necessary data for both Emotion and Sign Language Detection components of our project.
