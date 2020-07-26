import json
import pickle

import numpy as np
import tensorflow
from gensim.models import Word2Vec
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import roc_auc_score
from tensorflow.python.keras import layers
from tensorflow.python.keras import regularizers
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Input, Embedding
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.optimizers import Adam, SGD
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer


# tf.compat.v1.disable_eager_execution()


def list_to_string(lst):
    one_string = ' '.join(lst)

    return one_string


def tokens_to_string(tokens, inverse_map=None):
    words = [inverse_map[token] for token in tokens if token != 0]
    text = ' '.join(words)
    return text


def train(mutated):
    with open('data\\top10_list.pkl', 'rb') as input_file:
        top10_list = pickle.load(input_file)

    titles = []
    for x in top10_list:
        result = _train(mutated, x)
        titles.append(result)
    return json.dumps(titles)


def _train(mutated, module_name):
    mutated = mutated[mutated['mod_keys_found_string'] == module_name]
    train_set, val_set, test_set = np.split(mutated.sample(frac=1), [int(.6 * len(mutated)), int(.8 * len(mutated))])
    tasks_sent_train = [row for row in train_set['task_complete']]
    model_tasks3 = Word2Vec(tasks_sent_train, sg=0, size=100, window=6, min_count=1, workers=4, iter=1000)

    train_set['task_complete_one_string'] = train_set['task_complete'].apply(lambda x: list_to_string(x))
    test_set['task_complete_one_string'] = test_set['task_complete'].apply(lambda x: list_to_string(x))
    val_set['task_complete_one_string'] = val_set['task_complete'].apply(lambda x: list_to_string(x))

    y_train = train_set['consistent'].astype(int)
    print(y_train.value_counts(), y_train.shape)

    y_test = test_set['consistent'].astype(int)
    print(y_test.value_counts(), y_test.shape)

    y_val = val_set['consistent'].astype(int)

    tokenizer_train = Tokenizer(lower=False)
    tokenizer_train.fit_on_texts(train_set['task_complete'])
    print(tokenizer_train)
    tokenizer_train = Tokenizer(lower=False)
    tokenizer_train.fit_on_texts(train_set['task_complete'])
    print(tokenizer_train)

    tokenizer_test = Tokenizer(lower=False)
    tokenizer_test.fit_on_texts(test_set['task_complete'])
    print(tokenizer_test)

    tokenizer_val = Tokenizer(lower=False)
    tokenizer_val.fit_on_texts(val_set['task_complete'])

    tasks_train_tokens = tokenizer_train.texts_to_sequences(train_set['task_complete_one_string'])
    tasks_test_tokens = tokenizer_test.texts_to_sequences(test_set['task_complete_one_string'])
    tasks_val_tokens = tokenizer_val.texts_to_sequences(val_set['task_complete_one_string'])

    num_tokens = [len(tokens) for tokens in tasks_train_tokens]
    num_tokens = np.array(num_tokens)
    np.max(num_tokens)
    np.argmax(num_tokens)
    max_tokens = np.mean(num_tokens) + 2 * np.std(num_tokens)
    max_tokens = int(max_tokens)
    np.sum(num_tokens < max_tokens) / len(num_tokens)
    tasks_train_pad = pad_sequences(tasks_train_tokens, maxlen=max_tokens, padding='post')
    tasks_test_pad = pad_sequences(tasks_test_tokens, maxlen=max_tokens, padding='post')
    tasks_val_pad = pad_sequences(tasks_val_tokens, maxlen=max_tokens, padding='post')

    idx = tokenizer_train.word_index
    inverse_map = dict(zip(idx.values(), idx.keys()))

    embedding_size = 100
    num_words = len(list(tokenizer_train.word_index)) + 1

    embedding_matrix = np.random.uniform(-1, 1, (num_words, embedding_size))
    for word, i in tokenizer_train.word_index.items():
        if i < num_words:
            embedding_vector = model_tasks3[word]
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

    sequence_length = max_tokens
    vocabulary_size = num_words
    embedding_dim = embedding_size
    filter_sizes = [3, 4, 5]
    batch_size = 256

    embedding_layer = Embedding(input_dim=num_words, output_dim=embedding_size, weights=[embedding_matrix],
                                input_length=max_tokens, trainable=False, name='embedding_layer')
    inputs = Input(shape=(sequence_length,))
    embedding = embedding_layer(inputs)
    sample_size = tasks_train_pad.shape
    tensorflow.compat.v1.disable_eager_execution()

    # CNN architecture

    num_classes = 2

    # Training params
    # batch_size = 256
    num_epochs = 20

    # Model parameters
    num_filters = 64
    embed_dim = embedding_size
    weight_decay = 1e-4

    print("training CNN ...")
    model = Sequential()

    # Model add word2vec embedding

    model.add(Embedding(input_dim=num_words,
                        output_dim=embedding_size,
                        weights=[embedding_matrix],
                        input_length=max_tokens,
                        trainable=True,  # the layer is trained
                        name='embedding_layer'))
    model.add(layers.Conv1D(filters=num_filters, kernel_size=max_tokens, activation='relu', padding='same',
                            kernel_regularizer=regularizers.l2(weight_decay)))
    model.add(layers.MaxPooling1D(2))
    model.add(Dropout(0.25))

    model.add(
        layers.Conv1D(filters=num_filters + num_filters, kernel_size=max_tokens, activation='relu', padding='same',
                      kernel_regularizer=regularizers.l2(weight_decay)))
    model.add(layers.GlobalMaxPooling1D())
    model.add(Dropout(0.25))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
    # model.add(BatchNormalization())
    model.add(layers.Dense(num_classes, activation='softmax'))

    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss=tensorflow.keras.losses.MeanAbsoluteError(), optimizer=sgd, metrics=['accuracy'])
    model.summary()

    model.fit(tasks_train_pad, to_categorical(y_train), batch_size=batch_size, epochs=num_epochs,
              validation_data=(tasks_test_pad, to_categorical(y_test)),
              shuffle=True, verbose=2)

    score = model.evaluate(tasks_val_pad, to_categorical(y_val), verbose=0)
    print('loss:', score[0])
    print('Validation accuracy:', score[1])
    y_pred = model.predict_classes(tasks_val_pad)

    cm = confusion_matrix(y_val, y_pred)
    tp = cm[1][1]
    fp = cm[0][1]
    fn = cm[1][0]
    tn = cm[0][0]
    precision = round(tp / (tp + fp), 2)
    print('Consistent: precision=%.3f' % (precision))
    recall = round(tp / (tp + fn), 2)
    print('Consistent: recall=%.3f' % (recall))
    f1_score = (2 * precision * recall) / (precision + recall)
    print('Consistent: f1_score=%.3f' % (f1_score))
    precision_neg = round(tn / (tn + fn), 2)
    print('Inconsistent: precision=%.3f' % (precision_neg))
    recall_neg = round(tn / (tn + fp), 2)
    print('Inconsistent: recall=%.3f' % (recall_neg))
    f1_score_neg = (2 * precision_neg * recall_neg) / (precision_neg + recall_neg)
    print('Inconsistent: f1_score=%.3f' % (f1_score_neg))
    ns_probs = [0 for _ in range(len(y_val))]
    ns_auc = roc_auc_score(y_val, ns_probs)
    lr_auc = roc_auc_score(y_val, y_pred)
    mcc = matthews_corrcoef(y_val, y_pred)
    print(precision)
    print('No Skill: ROC AUC=%.3f' % (ns_auc))
    print('Our model: ROC AUC=%.3f' % (lr_auc))
    print('Our model: MCC=%.3f' % (mcc))

    json_out = {
        "module": module_name,
        "MCC": mcc,
        "AUC": lr_auc
    }
    # y = json.dumps(json_out)
    model.save('models\\' + module_name)
    # with open('models\\' + module_name + '.pkl', 'wb') as output_file:
    #     pickle.dump(model, output_file)

    return json_out


def _predict(test_set_module, module_name):
    model = tensorflow.keras.models.load_model('models\\' + module_name)
    node, size = model.get_input_shape_at(0)
    test_set_module['task_complete_one_string'] = test_set_module['task_complete'].apply(lambda x: list_to_string(x))
    tokenizer_val = Tokenizer(lower=False)
    tokenizer_val.fit_on_texts(test_set_module['task_complete'])
    tasks_val_tokens = tokenizer_val.texts_to_sequences(test_set_module['task_complete_one_string'])
    tasks_val_pad = pad_sequences(tasks_val_tokens, maxlen=size, padding='post')
    return model.predict(tasks_val_pad)


def predict(test_set):
    with open('data\\top10_list.pkl', 'rb') as input_file:
        top10_list = pickle.load(input_file)
    mergedlist = []
    for x in top10_list:
        val_set2 = test_set.copy()
        val_set2 = val_set2[val_set2['mod_keys_found_string'] == x]
        if val_set2.empty:
            continue
        result = _predict(val_set2, x)
        y_classes = result.argmax(axis=-1)
        val_set2['consistent'] = y_classes.tolist()
        val_set2['consistent'] = val_set2['consistent'].apply(lambda x: True if x == 1 else False)
        val_set2 = val_set2[['task_name', 'consistent']]
        dic = val_set2.to_dict(orient='records')
        for item in dic:
            mergedlist.append(item)

    return json.dumps(mergedlist)
