import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Add
import numpy as np

# Load the pre-trained ResNet50 model
base_model = ResNet50(weights='imagenet')
model = Model(base_model.input, base_model.layers[-2].output)

# Function to preprocess images
def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.resnet50.preprocess_input(img)
    return img

# Function to extract features from the image
def extract_image_features(image_path):
    img = preprocess_image(image_path)
    features = model.predict(img)
    return features

# RNN/LSTM for caption generation
def build_captioning_model(vocab_size, max_length):
    inputs = tf.keras.Input(shape=(2048,))
    features = tf.keras.layers.Dense(256, activation='relu')(inputs)
    
    seq_input = tf.keras.Input(shape=(max_length,))
    embedded_seq = Embedding(vocab_size, 256)(seq_input)
    lstm_out = LSTM(256)(embedded_seq)
    
    merged = Add()([features, lstm_out])
    output = Dense(vocab_size, activation='softmax')(merged)
    
    return Model(inputs=[inputs, seq_input], outputs=output)

# Function to generate caption from the model
def generate_caption(model, image_features, tokenizer, max_length):
    caption = "startseq"
    for i in range(max_length):
        seq = tokenizer.texts_to_sequences([caption])[0]
        seq = pad_sequences([seq], maxlen=max_length)
        yhat = model.predict([image_features, seq], verbose=0)
        word = np.argmax(yhat)
        caption += ' ' + tokenizer.index_word[word]
        if word == tokenizer.word_index['endseq']:
            break
    return caption

# Example usage
image_path = 'example_image.jpg'
image_features = extract_image_features(image_path)

# Assuming we have the trained caption model, tokenizer, and max_length set up
caption_model = build_captioning_model(vocab_size=5000, max_length=34)
caption = generate_caption(caption_model, image_features, tokenizer, max_length=34)
print(caption)
