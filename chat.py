import torch
import os, json, random
import numpy as np
from nltk.tokenize import word_tokenize
from utils.loader import DatasetManager
from utils.process import Evaluator
from utils.config import *
import actions as br

# Fix the random seed of package random.
random.seed(args.random_state)
np.random.seed(args.random_state)

# Fix the random seed of Pytorch when using CPU.
torch.manual_seed(args.random_state)
torch.random.manual_seed(args.random_state)

# Instantiate a dataset object.
dataset = DatasetManager(args)
dataset.quick_build()
dataset.show_summary()

model = torch.load('new_model.pkl', map_location=torch.device('cpu'))

#Get Prediction
def prediction_deployment(model, batch_texts, dataset):
    pred_slot = []
    pred_intent = []

    padded_text, seq_lens = dataset.add_padding(
            batch_texts,
            digital=False
    )
    digit_text = dataset.word_alphabet.get_index(padded_text)
    var_text = torch.LongTensor(digit_text)
    slot_idx, intent_idx, matrix = model(var_text, seq_lens, n_predicts=1)
    nested_slot = Evaluator.nested_list([list(Evaluator.expand_list(slot_idx))], seq_lens)[0]
    pred_slot.extend(dataset.slot_alphabet.get_instance(nested_slot))
    intent_idx_ = [[] for i in range(len(digit_text))]
    for item in intent_idx:
        intent_idx_[item[0]].append(item[1])
    intent_idx = intent_idx_
    pred_intent.extend(dataset.intent_alphabet.get_instance(intent_idx))
    
    matrix = matrix.cpu().data.numpy()
    matrix = matrix.squeeze(2)
    final_matrix = np.transpose(matrix, (1, 0))[intent_idx[0]]
    vector = final_matrix.max(axis=0)
    final_matrix = final_matrix == vector

    intent_idx, text_pred_idx = np.where(final_matrix==1)
    intent_index = { ind:intent for intent,ind in zip(pred_intent[0], range(len(pred_intent[0]))) }
    print(intent_index)
    intent_slot = { key:"" for key in pred_intent[0]}
    for i in range(len(intent_idx)):
        intent_slot[intent_index[intent_idx[i]]] += " " + batch_texts[0][text_pred_idx[i]]

    return intent_slot

def tokenize_texts(texts):
    tokenized_texts = []
    for text in texts:
        tokenized_texts.append((word_tokenize(text)))
    
    return tokenized_texts

def get_response(msg):
    tokenized_texts = tokenize_texts([msg])
    intent_slot = prediction_deployment(model=model, batch_texts=tokenized_texts, dataset=dataset)

    action_and_data = []
    for intent, message in intent_slot.items():
        try:
            if intent == "BookRestaurant":
                action_and_data.append((intent, br.get_restaurants(message)))
            elif intent == "GetWeather":
                action_and_data.append((intent, br.getWeather(message)))
            else:
                action_and_data.append(("Error", "Server have problem, Please resent!"))
        except:
            action_and_data.append(("Error", "Server have problem, Please resent!"))
            

    return action_and_data

# print(get_response("can you add confessions to my playlist called clasica and what is the weather forecast for close-by burkina"))
