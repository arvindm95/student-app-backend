#  Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""An Example of a DNNClassifier for the Iris dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
class globals():
    train_x = None
    train_y = None
    test_x = None
    test_y = None
    batch_size = 100
    train_steps = 1000

@app.route('/')
def hello_world():
    return 'Hello, World!'

import argparse
import tensorflow as tf

import iris_data


parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')
@app.route('/tf')
def callTf():
    if __name__ == '__main__':
        tf.app.run(main)
        return 'done'

def main(argv):
    args = parser.parse_args(argv[1:])
    
    # Fetch the data
    (train_x, train_y), (test_x, test_y) = iris_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        model_dir='models/iris',
        # The model must choose between 3 classes.
        n_classes=3)

    # Train the Model.
    #print (train_x)
    classifier.train(
        input_fn=lambda:iris_data.train_input_fn(train_x, train_y,
                                                 args.batch_size),
        steps=args.train_steps)

    # Evaluate the model.
   # eval_result = classifier.evaluate(
   #     input_fn=lambda:iris_data.eval_input_fn(test_x, test_y,
   #                                            args.batch_size))

   # print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))
    predictApp(classifier, args)



@app.route('/train')
def trainSystem():
    # Fetch the data
    if globals.train_x is None:
        (globals.train_x, globals.train_y), (globals.test_x, globals.test_y) = iris_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in globals.train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        model_dir='models/iris',
        # The model must choose between 3 classes.
        n_classes=3)

    # Train the Model.
    classifier.train(
        input_fn=lambda:iris_data.train_input_fn(globals.train_x, globals.train_y,
                                                 globals.batch_size),
        steps=globals.train_steps)
    return 'Training done'


@app.route('/predict', methods = ['POST'])
def getPrediction():
    print (request.json)
    '''request_data = {
        'M1': [91.0, 13.0, 40.0],
        'M2': [86.0, 10.0, 38.0],
        'M3': [91.0, 11.0, 60.0],
        'M4': [81.0, 10.0, 65.0],
        'sQ1': [1.0, 0.0, 1.0],
        'sQ2': [1.0, 1.0, 0.0],
        'sQ3': [1.0, 0.0, 1.0],
        'sQ4': [1.0, 0.0, 1.0],
        'sQ5': [1.0, 1.0, 0.0],
        'TQ1': [1.0, 1.0, 1.0],
        'TQ2': [1.0, 0.0, 0.0],
        'TQ3': [1.0, 1.0, 0.0],
        'TQ4': [1.0, 0.0, 1.0],
        'TQ5': [1.0, 0.0, 0.0],
    }'''
    request_data = request.json
    
    args = ''
    if globals.train_x is None:
        (globals.train_x, globals.train_y), (globals.test_x, globals.test_y) = iris_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in globals.train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        model_dir='models/iris',
        # The model must choose between 3 classes.
        n_classes=3)
    output = jsonify(predictApp(classifier, request_data))
    return output


def predictApp(classifier, data):
    # Generate predictions from the model
    expected = ['PG','DropOut','Job']
    predict_x = data
    predictions = classifier.predict(
        input_fn=lambda:iris_data.eval_input_fn(predict_x,
                                                labels=None,
                                                batch_size=globals.batch_size))
    for pred_dict, expec in zip(predictions, expected):
        template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

        class_id = pred_dict['class_ids'][0]
        probability = pred_dict['probabilities'][class_id]

        print(template.format(iris_data.SPECIES[class_id],
                              100 * probability, expec))
        output_data = {"prediction":iris_data.SPECIES[class_id],"value":round(probability,4)}
        return output_data



@app.route('/done')
def api():
    #input_data = request.json
    model_api = getPredictionAlone()
    output_data = model_api()
    response = jsonify(output_data)
    return response


def getPredictionAlone():
    args = ''
    if globals.train_x is None:
        (globals.train_x, globals.train_y), (globals.test_x, globals.test_y) = iris_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in globals.train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))
    print(my_feature_columns)
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        hidden_units=[10, 10],
        n_classes=3,
        model_dir='models/iris'
    )
       # feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
     #   hidden_units=[10, 10],
     #   n_classes=3,
     
     #   model_dir='models/iris'
        # The model must choose between 3 classes.)
   # classifier = tf.estimator.Estimator(model_fn='DNNClassifier', model_dir='models/iris')    
    print ('this is called')
    def model_api():
        # Generate predictions from the model
        expected = ['PG','DropOut','Job']
        predict_x = {
            'M1': [91.0, 13.0, 40.0],
            'M2': [86.0, 10.0, 38.0],
            'M3': [91.0, 11.0, 60.0],
            'M4': [81.0, 10.0, 65.0],
            'sQ1': [1.0, 0.0, 1.0],
            'sQ2': [1.0, 1.0, 0.0],
            'sQ3': [1.0, 0.0, 1.0],
            'sQ4': [1.0, 0.0, 1.0],
            'sQ5': [1.0, 1.0, 0.0],
            'TQ1': [1.0, 1.0, 1.0],
            'TQ2': [1.0, 0.0, 0.0],
            'TQ3': [1.0, 1.0, 0.0],
            'TQ4': [1.0, 0.0, 1.0],
            'TQ5': [1.0, 0.0, 0.0],
        }
        predictions = classifier.predict(
            input_fn=lambda:iris_data.eval_input_fn(predict_x,
                                                    labels=None,
                                                    batch_size=1000))
        for pred_dict, expec in zip(predictions, expected):
            template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

            class_id = pred_dict['class_ids'][0]
            probability = pred_dict['probabilities'][class_id]

            print(template.format(iris_data.SPECIES[class_id],
                                100 * probability, expec))
            output_data = {"prediction":iris_data.SPECIES[class_id],"value":round(probability,4)}
            #output_data = iris_data.SPECIES[class_id]
            return output_data
    
    
    
   # output = jsonify(predictApp(classifier, args))


    return model_api


if __name__ == '__main__':
    '''tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)'''
    app.run(host='0.0.0.0', debug=True)