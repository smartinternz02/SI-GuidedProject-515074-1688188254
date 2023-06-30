# Sign Language Detection

Training of the **Sign Language Detection** model was done in [Google colab](https://colab.research.google.com/)

## Model Summary

<pre>
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 222, 222, 24)      672       
                                                                 
 max_pooling2d (MaxPooling2D  (None, 111, 111, 24)     0         
 )                                                               
                                                                 
 conv2d_1 (Conv2D)           (None, 109, 109, 32)      6944      
                                                                 
 max_pooling2d_1 (MaxPooling  (None, 54, 54, 32)       0         
 2D)                                                             
                                                                 
 conv2d_2 (Conv2D)           (None, 52, 52, 32)        9248      
                                                                 
 max_pooling2d_2 (MaxPooling  (None, 26, 26, 32)       0         
 2D)                                                             
                                                                 
 conv2d_3 (Conv2D)           (None, 24, 24, 48)        13872     
                                                                 
 max_pooling2d_3 (MaxPooling  (None, 12, 12, 48)       0         
 2D)                                                             
                                                                 
 conv2d_4 (Conv2D)           (None, 10, 10, 64)        27712     
                                                                 
 max_pooling2d_4 (MaxPooling  (None, 5, 5, 64)         0         
 2D)                                                             
                                                                 
 conv2d_5 (Conv2D)           (None, 3, 3, 64)          36928     
                                                                 
 max_pooling2d_5 (MaxPooling  (None, 1, 1, 64)         0         
 2D)                                                             
                                                                 
 flatten (Flatten)           (None, 64)                0         
                                                                 
 dense (Dense)               (None, 62)                4030      
                                                                 
 dense_1 (Dense)             (None, 32)                2016      
                                                                 
 dense_2 (Dense)             (None, 16)                528       
                                                                 
 dense_3 (Dense)             (None, 21)                357       
                                                                 
=================================================================
Total params: 102,307
Trainable params: 102,307
Non-trainable params: 0
_________________________________________________________________
</pre>

## Dataset

Google Drive Link: https://drive.google.com/drive/folders/1p3QviZMkpTyyijICqSa0K4QFP7RoQf-H?usp=sharing
<br>Present in folder `ExternshipProject_Dataset/SignLanguage_Dataset`
