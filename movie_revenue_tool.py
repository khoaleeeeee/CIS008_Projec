from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np

# Constant

FILE_NAME = 'cost_revenue_clean.csv'
FEATURES = 'production_budget_usd'
TARGET = 'worldwide_gross_usd'

# Generates graph's labels from dataframe's columns.
def labels_generator(text):
    label = ''
    for letter in text:
        if letter.isalpha():
            label += letter
        else:
            label += ' '
    return label.title()
    
    
# Visualization (Graphing) function
# Call this function in the graphing window.
def data_visualization(plot, file_name=FILE_NAME, features=FEATURES, 
                       target=TARGET,
                       graph_title="Film Cost vs Global Revenue"):
        
    """Displays the data
    
    Keyword arguments:
    plot == subplot. type: AxesSubplot.
    filename -- name of the data file. type: csv.
    features -- name of the features or independent data.
    target -- name of the target or dependent data. 
    graph title -- name of the graph.
    
    """
    
    data = pd.read_csv(file_name)
    
    x = pd.DataFrame(data, columns=[features])
    y = pd.DataFrame(data, columns=[target])
    
    plot.scatter(x, y, color="orange", linewidth=3, alpha = 0.6)
#    plot.xticks(fontsize = 14)
#    plot.yticks(fontsize = 14)
    plot.set_xlabel(labels_generator(features), fontsize = 12, color="b")
    plot.set_ylabel(labels_generator(target), fontsize = 12, color="b")
    plot.title.set_text(graph_title)
#    plot.style.use("bmh")
#    
#    # choosing the range for the axes, ensures the graph displays all values.
    plot.set_xlim(0, round(data.describe()[features]["max"], -7) + 30000000) #rounds the data. 
    plot.set_ylim(0, round(data.describe()[target]["max"], -9)) #rounds the data. 
#    


def get_predicted_revenue(budget):

    """Estimates the revenue of the movie
    
    budget -- the planning budget to spend on the movie
    
    """
    data = pd.read_csv(FILE_NAME)
    
    X = []
    Y = []
    
    for line in open(FILE_NAME):
        x, y = line.split(',')
        if x == FEATURES or y == TARGET:
                continue
        else:
            X.append(float(x))
            Y.append(float(y))
    
    X = np.array(X)
    Y = np.array(Y)
    
    denominator = X.dot(X) - X.mean() * X.sum()
    
    coef = (X.dot(Y) - Y.mean() * X.sum()) / denominator
    intercept = (Y.mean() * X.dot(X) - X.mean() * X.dot(Y)) / denominator

    if budget < 0:
        raise Exception("Please Enter Positive Amount.")
    else:
        try:
            revenue = round((budget * coef + intercept), 3)
        except ValueError:
            print("Invalid input.")
    return revenue
    
    
    

def get_revenue_estimate(budget, high_confidence=True):
    """Estimates predicted revenue
    
    budget -- the planning budget to spend on the movie
    high_confidence -- True for a 95% prediction interval, False for a 68% prediction interval.
    
    """

    estimate = get_predicted_revenue(budget)
    if high_confidence:
        rounded_high = round(estimate + 2*RMSE, 3)
        rounded_low = round(estimate - 2*RMSE, 3)
        interval = 95
    else:
        rounded_high = round(estimate + RMSE, 3)
        rounded_low = round(estimate - RMSE, 3)
        interval = 68
        
    print(f'Estimated revenue is: {estimate}')
    print(f"At {interval}% confidence the valuation range is:")
    print(f"${rounded_low} at the lower value and ${rounded_high} at the higher value.")
    
    
    
    

def model_visualization(plot, file_name=FILE_NAME, features=FEATURES, 
                       target=TARGET,
                       graph_title="Regression Model Graph"):
                       
    """Displays the regression model graph
    
    Keyword arguments:
    filename -- name of the data file. type: csv.
    features -- name of the features or independent data.
    target -- name of the target or dependent data. 
    graph title -- name of the graph. 
    
    """
    X = []
    Y = []
    data = pd.read_csv(FILE_NAME)
    for line in open(FILE_NAME):
        x, y = line.split(',')
        if x == FEATURES or y == TARGET:
                continue
        else:
            X.append(float(x))
            Y.append(float(y))
    
    X = np.array(X)
    Y = np.array(Y)
    
    denominator = X.dot(X) - X.mean() * X.sum()
    
    coef = (X.dot(Y) - Y.mean() * X.sum()) / denominator
    intercept = (Y.mean() * X.dot(X) - X.mean() * X.dot(Y)) / denominator
    
    Yhat = X*coef + intercept

    
    plot.scatter(X, Y, linewidth=3, alpha = 0.6)
    plot.set_xlabel(labels_generator(features), fontsize = 12, color="b")
    plot.set_ylabel(labels_generator(target), fontsize = 12, color="b")
    plot.title.set_text(graph_title)
    
    # choosing the range for the axes, ensures the graph displays all values.
    plot.set_xlim(0, round(data.describe()[features]["max"], -7) + 30000000) #rounds the data. 
    plot.set_ylim(0, round(data.describe()[target]["max"], -9)) #rounds the data. 
    
    
    plot.plot(X, Yhat, color='red', linewidth=3)
