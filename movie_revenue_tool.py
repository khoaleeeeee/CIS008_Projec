# we use pandas to open the csv file as the table format
import pandas as pd  
# we use numpy arrays to store the columns budget and revenue.
# This is similar to list but more useful in data analysis
import numpy as np

# Constants

FILE_NAME = 'cost_revenue_clean.csv' # our data file (csv)

FEATURES = 'production_budget_usd'# columns' labels in the data file
TARGET = 'worldwide_gross_usd'# columns' labels in the data file

# Generates graph's labels from dataframe's columns in our graph
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
        
    """draw scatter plots of the data to visualize the distribution.
    
    Keyword arguments:
    plot == subplot. type: AxesSubplot.
    filename -- name of the data file. type: csv.
    features -- name of the features or independent data.
    target -- name of the target or dependent data. 
    graph title -- name of the graph.
    
    """
    
    data = pd.read_csv(file_name) # opens the data file by pandas
    
    x = pd.DataFrame(data, columns=[features])  # split the data to columns (budget)
    y = pd.DataFrame(data, columns=[target]) # split the data to columns (revenue)
    
    plot.scatter(x, y, color="orange", linewidth=3, alpha = 0.6) # plots the points
#    plot.xticks(fontsize = 14)
#    plot.yticks(fontsize = 14)
    plot.set_xlabel(labels_generator(features), fontsize = 12, color="b") # label for x axis
    plot.set_ylabel(labels_generator(target), fontsize = 12, color="b") # label for y axis
    plot.title.set_text(graph_title) # gives the graph a title
#    plot.style.use("bmh")
#    
    # choosing the range for the axes, ensures the graph displays all values nicely.
    plot.set_xlim(0, round(data.describe()[features]["max"], -7) + 30000000) #rounds the data. 
    plot.set_ylim(0, round(data.describe()[target]["max"], -9)) #rounds the data. 
#    


def get_predicted_revenue(budget):

    """Estimates the revenue of the movie by budget vale entered by the user
    
    budget -- the planning budget to spend on the movie
    
    """
    
    X = []
    Y = []
    
    # gets the data from the data file and stores all the values to the lists X and Y.
    # we can't use pandas to open because pandas does not change the type to float. 
    for line in open(FILE_NAME):
        x, y = line.split(',')
        if x == FEATURES or y == TARGET:
                continue
        else:
            X.append(float(x)) # change type to float
            Y.append(float(y))# change type to float
    
    X = np.array(X) # change the list to a numpy array
    Y = np.array(Y) # change the list to a numpy array
    
    # this is like the equations in the powerpoint. coef is a and intercept is b.
    denominator = X.dot(X) - X.mean() * X.sum()
    
    coef = (X.dot(Y) - Y.mean() * X.sum()) / denominator
    intercept = (Y.mean() * X.dot(X) - X.mean() * X.dot(Y)) / denominator
    
    # check for valid inputs
    if budget < 0:
        raise Exception("Please Enter Positive Amount.")
    else:
        try:
            revenue = round((budget * coef + intercept), 3)
        except ValueError:
            print("Invalid input.")
    return revenue
    
    
    
    
# this function combines the previous 2 functions. We end up drawing a regression line in the graph. 
# this is the model visualization.
def model_visualization(plot, file_name=FILE_NAME, features=FEATURES, 
                       target=TARGET,
                       graph_title="Regression Model Graph"):
                       
    """Displays the regression model graph with the scatter plots.
    
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
    
    # we went over these lines on the slides. coef is a and intercept is b.
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
