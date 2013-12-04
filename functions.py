from scipy.optimize import curve_fit
import numpy as np

def linear(x, a, b):
    return a + b*x

def createPoints(x_vals, y_vals):
    line = []

    if not isinstance(x_vals, list) and not isinstance(y_vals, list):
        return line

    if isinstance(x_vals, str) or isinstance(y_vals, str):#as string is a list, a special condition for the same
        return line

    if len(x_vals) != len(y_vals):
        return line
    for x, y in zip(x_vals, y_vals):
        line.append((x,y))
    return line

def getRelevantData(collection, array_conditions, sort_by, max=15):
    #check to see if the parameters are as expected

    #array condition is an object, collection a pymongo collection, sorting_by needs to have column and type
    conditions = {}

    for condition in array_conditions:
        conditions[condition.keys()[0]] = condition.values()[0]

    documents = collection.find(conditions).sort(sort_by["column"], sort_by["type"])[:max]

    size_of_documents = documents.count()
    if size_of_documents > max :
        size_of_documents = max

    result = {'x' : [], 'y': []}
    for document in documents:
        result['x'].append(document['x_val'])
        result['y'].append(document['y_val'])

    if size_of_documents != max and len(array_conditions) > 1:
        sub_result = getRelevantData(collection, array_conditions[1:], sort_by, max - size_of_documents)
        result['x'] += sub_result['x']
        result['y'] += sub_result['y']

    return result

def prediction(hours_before, waiting_list, data):

    graph_data = {
        "lines" : []
    }

    if len(data['x']) == 0:
        return {
            "prediction" : False,
            "message" : "Not Enough data for prediction",
            "data" : graph_data,
            "prediction_val" : 0
        }

    prediction_array = []

    for x_values, y_values in zip(data['x'], data['y']):

        linearopt = curve_fit(linear, np.array(x_values), np.array(y_values))
        linear_val_at_hours = int(linear(hours_before, linearopt[0][0], linearopt[0][1]))
        linear_val_at_zero = int(linear(0, linearopt[0][0], linearopt[0][1]))
        pred = linear_val_at_zero - (linear_val_at_hours - waiting_list)

        prediction_array.append(pred)
        line_data = {
            "points" : createPoints(x_values, y_values)
        }
        graph_data["lines"].append(line_data)

    mean = np.mean(prediction_array)
    result = {
        "data" : graph_data,
        "prediction_val" : mean
    }
    if mean > 0:
        result = dict(result.items() + {
            "prediction" : False,
            "message" : "high chances that your ticket will not be confirmed",
        }.items())
    else:
        result = dict(result.items() + {
            "prediction" : True,
            "message" : "high chances that your ticket will be confirmed",
        }.items())

    return result
