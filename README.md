# llSPS-INT-2887-Nutrition-Analysis-Using-Image-Classification
## FRONT-END DEPLOYED AT https://fruitscal.herokuapp.com
## SERVER DEPLOYED AT https://yo-fruits.eu-gb.mybluemix.net/
## Nutrition Analysis Using Image Classification
1. Classify the images of food for further diet monitoring applications using convolution neural networks (CNNs).
2. Then converting this model into a web API which will accept a fruit image as input and returns the name of fruit and using this name to make request using another API (Nutrition API by Nutritionix) to get the nutrition content of that fruit.
3. Creating an interactive web application that will make requests to this API and show the results in a user-friendly environment.

## Dataset 
The dataset is downloaded from the Kaggle's "Fruits 360" dataset. https://www.kaggle.com/moltean/fruits
>* This dataset has 90483. images of fruits and vegetables spread across 131 labels.
>* Each image contains a single fruit or vegetable
>* The images were obtained by ﬁlming the fruits while they are rotated by a motor and then extracting frames. 
>* Behind the fruits we placed a white sheet of paper as background.
>* The fruit after the background removal and after it was scaled down to 100x100 pixels.

##### But the whole dataset is not used in this project ,only the following fruits and are included: 
 > Apples,Bananas,Blueberry,Cherry,Dates,Grapes,Guava,Lemon,Mango,Onion,Orange,Papaya,Pineapple,Pomegranate,Potato,Strawberry,Tomato,Watermelon

##### Subset of the "Fruit 360" dataset used in this project:
>1. Total number of images: 15584.
>2. Training set size: 10597 images (one fruit or vegetable per image).
>3. Test set size: 4987 images (one fruit or vegetable per image).
>4. Number of classes: 18
>5. Image size: 100x100 pixels.
>6. Filename format: jpg

Dataset used in this project can be downloaded from 
https://tinyurl.com/ybnh3lj2
