import json

import numpy as np
import torch

from .caption import caption_image_beam_search
from .models2 import DecoderWithAttention, Encoder


def data_preprocess():
    global apple_scab_symptoms, apple_black_rot, tomato_bacterial_spot, tomato_late_blight, tomato_early_blight, final_set
    global asc_indexes, abr_indexes, tbs_indexes, tlb_indexes, teb_indexes, dis_sym_matrix

    apple_scab_symptoms = ['black-spots', 'circular-spots', 'spots-covering-entire-surface', 'pale-spots',
                           'fused-spots', 'yellow-spots', 'olive-green-spots', 'velvety-spots', 'yellow-leaf', 'twisted-leaf']
    apple_black_rot = ['dark-brown-lesions-purple-margin', 'irregular-lesions', 'chlorotic-leaf',
                       'circular-spots', 'purple-red-edge-light-tan-centers', 'small-purple-spots']
    tomato_bacterial_spot = ['greasy-spots', 'circular-spots', 'small-brown-spots',
                             'irregular-lesions', 'rough-lesions', 'yellowish-halo-around-spots']
    tomato_early_blight = ['yellow-tissue-around-spots',
                           'black-lesions', 'concentric-rings-inside-lesions']
    tomato_late_blight = ['dark-brown-patches',
                          'powdery-white-fungal-growth', 'curled-leaf']

    final_set = set(tomato_bacterial_spot)
    final_set = final_set.union(set(tomato_late_blight))
    final_set = final_set.union(set(tomato_early_blight))
    final_set = final_set.union(set(apple_scab_symptoms))
    final_set = final_set.union(set(apple_black_rot))

    asc_indexes = []
    abr_indexes = []
    teb_indexes = []
    tlb_indexes = []
    tbs_indexes = []

    for w, x in enumerate(sorted(final_set)):

        for i, j in enumerate(apple_scab_symptoms):
            if(x == j):
                asc_indexes.append(w)

        for i, j in enumerate(apple_black_rot):
            if(x == j):
                abr_indexes.append(w)

        for i, j in enumerate(tomato_early_blight):
            if(x == j):
                teb_indexes.append(w)

        for i, j in enumerate(tomato_late_blight):
            if(x == j):
                tlb_indexes.append(w)

        for i, j in enumerate(tomato_bacterial_spot):
            if(x == j):
                tbs_indexes.append(w)

        dis_sym_matrix = np.zeros((25, 5))

    for x in range(0, 5):
        if(x == 0):
            for i, y in enumerate(asc_indexes):
                dis_sym_matrix[y, x] = 1

        if (x == 1):
            for i, y in enumerate(abr_indexes):
                dis_sym_matrix[y, x] = 1

        if(x == 2):
            for i, y in enumerate(teb_indexes):
                dis_sym_matrix[y, x] = 1

        if(x == 3):
            for i, y in enumerate(tlb_indexes):
                dis_sym_matrix[y, x] = 1

        if(x == 4):
            for i, y in enumerate(tbs_indexes):
                dis_sym_matrix[y, x] = 1


def image_to_symptoms(data):
    global emb_dim, attention_dim, decoder_dim, dropout

    '''
    img : numpy array received
    '''
    img = data
    emb_dim = 112
    attention_dim = 512
    decoder_dim = 512
    dropout = 0

    with open("./mainapp/WORDMAP_1_cap_per_img_2_min_word_freq.json", 'r') as j:
        word_map = json.load(j)

    checkpoint = torch.load(
        "./mainapp/checkpoint_five_disease_csd.pt", map_location="cpu")

    encoder = Encoder()
    encoder.load_state_dict(checkpoint["encoder"])

    encoder = encoder.eval()

    decoder = DecoderWithAttention(attention_dim=attention_dim, embed_dim=emb_dim,
                                   decoder_dim=decoder_dim, vocab_size=len(word_map), dropout=dropout)
    decoder.load_state_dict(checkpoint["decoder"])

    decoder = decoder.eval()

    my_caption, _ = caption_image_beam_search(
        encoder, decoder, img, word_map, beam_size=3)

    reverse_map = {}
    for key in word_map:
        reverse_map[word_map[key]] = key

    caption = []
    for i, preds in enumerate(my_caption):
        caption.append(reverse_map[preds])

    temp = {}
    temp["symptoms"] = caption
    return temp


def get_disease_from_label(data):
    data_preprocess()
    received = data["symptoms"]
    print(received)
    q_indexes = []
    for j, y in enumerate(received):
        for i, x in enumerate(sorted(final_set)):
            if(y == x):
                q_indexes.append(i)

    single_col_dis = np.zeros((25,))

    for x in q_indexes:
        single_col_dis[x] = 1

    dis_conifdence = []
    single_col_norm = np.dot(single_col_dis, single_col_dis.T)

    for x in range(0, 5):
        test_norm = np.dot(dis_sym_matrix[:, x], dis_sym_matrix[:, x].T)
        product = np.dot(
            single_col_dis, dis_sym_matrix[:, x])/(test_norm*single_col_norm)
        dis_conifdence.append(product)
    print(dis_conifdence)
    disease_info = {
        0: {'dis_name': 'apple_scab',
            'dis_rem': 'preventing this disease'},

        1: {'dis_name': 'apple_black_rot',
            'dis_rem': 'preventing this disease'},

        2: {'dis_name': 'tomato_early_blight',
            'dis_rem': 'preventing this disease'},

        3: {'dis_name': 'tomato_late_blight',
            'dis_rem': 'preventing this disease'},

        4: {'dis_name': 'tomato_bacterial_spot',
            'dis_rem': 'preventing this disease'},

    }

    maxi = dis_conifdence[0]
    maxi_2 = dis_conifdence[0]
    prev_id = 0
    max_id = 0

    for i, x in enumerate(dis_conifdence):
        if(x >= maxi_2 and x < maxi):
            maxi_2 = x
            prev_id = i
        if(x >= maxi):
            maxi_2 = maxi
            prev_id = max_id
            maxi = x
            max_id = i

    # diseases = {}
    # diseases['first'] = disease_info[max_id]['dis_name']
    # diseases['second'] = disease_info[prev_id]['dis_name']

    return (disease_info[max_id]['dis_name'],disease_info[prev_id]['dis_name'])

