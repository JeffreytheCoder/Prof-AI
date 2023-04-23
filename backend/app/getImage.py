import os
import sys
import random
import requests
from dotenv import load_dotenv


def convert_md(file_string):
    replaced_file_string = replace_image_with_url(get_images_by_keywords(find_image_keywords(file_string)), file_string)
    hash = random.getrandbits(128)
    print("hash value: %032x" % hash)
    f = open(f"{hash}.md", "w")
    f.write(replaced_file_string)
    f.close()
    subprocess.run(["marp", f"{hash}.md", "--pdf", "--theme", "uncover"])


def replace_image_with_url(res, file_string):
    for key in res:
        url = res[key]
        file_string = file_string.replace(f"<image> (keyword: {key})", f"![bg left]({url})")
        print(f"{key}: {url}")
    return file_string


def find_image_keywords(file_string):
    return re.findall(r'<image> \(keyword: (.*?)\)', file_string)


def get_images_by_keywords(queries):
    res = {}
    for query in queries:
        res[query] = get_image(query)
    return res

# Fetch an image from Google Custom Search API
def get_image(query):
    load_dotenv()
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        print("GOOGLE_API_KEY not found in .env file")
        sys.exit(1)
    pse_id = '86382df91391748a6'
    params = {
        'cx': pse_id,
        'num': '10',
        'q': query,
        'searchType': 'image',
        'key': key
    }
    response = requests.get(
        'https://www.googleapis.com/customsearch/v1', params=params)
    data = response.json()
    res = random.choice(data['items'])
    return res['link']


convert_md("""# Introduction to Linear Regression

- **Linear regression** is a method used to model the relationship between a dependent variable and one or more independent variables.
- It assumes that there is a linear relationship between the variables and tries to find the line of best fit that minimizes the sum of squared errors.
<image> (keyword: Linear regression summary)
---

## Simple Linear Regression

- Simple linear regression involves modeling the relationship between a dependent variable `y` and a single independent variable `x`.
- The line of best fit can be represented by the equation `y = b0 + b1*x`, where `b0` is the y-intercept and `b1` is the slope of the line.

---

## Multiple Linear Regression

- Multiple linear regression involves modeling the relationship between a dependent variable `y` and multiple independent variables `x1, x2, ..., xn`.
- The line of best fit can be represented by the equation `y = b0 + b1*x1 + b2*x2 + ... + bn*xn`.
<image> (keyword: multi-variable)
---

## Implementing Linear Regression in Python

- We can use the `LinearRegression` class from the `scikit-learn` library to perform linear regression in Python.
- Here is an example of how to fit a simple linear regression model:

```python
from sklearn.linear_model import LinearRegression

# define the data
X = [[0], [1], [2]]
y = [0, 1, 2]

# create and fit the model
model = LinearRegression()
model.fit(X, y)

# make predictions
predictions = model.predict([[3], [4]])
```
---
## Visualizing Results
- We can use visualization libraries such as matplotlib or seaborn to create scatter plots and visualize the line of best fit.
- Here is an example of how to create a scatter plot with a fitted line:
```python
import matplotlib.pyplot as plt

# define the data
X = [0, 1, 2]
y = [0, 1, 2]

# plot the data
plt.scatter(X, y)

# plot the fitted line
plt.plot(X, y)

# show the plot
plt.show()
Is there anything else you would like to know?
```
""")

# print(get_images_by_keywords(find_image_keywords("""# Introduction to Linear Regression
#
# - **Linear regression** is a method used to model the relationship between a dependent variable and one or more independent variables.
# - It assumes that there is a linear relationship between the variables and tries to find the line of best fit that minimizes the sum of squared errors.
# <image> (keyword: Linear regression summary)
# ---
#
# ## Simple Linear Regression
#
# - Simple linear regression involves modeling the relationship between a dependent variable `y` and a single independent variable `x`.
# - The line of best fit can be represented by the equation `y = b0 + b1*x`, where `b0` is the y-intercept and `b1` is the slope of the line.
#
# ---
#
# ## Multiple Linear Regression
#
# - Multiple linear regression involves modeling the relationship between a dependent variable `y` and multiple independent variables `x1, x2, ..., xn`.
# - The line of best fit can be represented by the equation `y = b0 + b1*x1 + b2*x2 + ... + bn*xn`.
# <image> (keyword: multi-variable)
# ---
#
# ## Implementing Linear Regression in Python
#
# - We can use the `LinearRegression` class from the `scikit-learn` library to perform linear regression in Python.
# - Here is an example of how to fit a simple linear regression model:
#
# ```python
# from sklearn.linear_model import LinearRegression
#
# # define the data
# X = [[0], [1], [2]]
# y = [0, 1, 2]
#
# # create and fit the model
# model = LinearRegression()
# model.fit(X, y)
#
# # make predictions
# predictions = model.predict([[3], [4]])
# ```
# ---
# ## Visualizing Results
# - We can use visualization libraries such as matplotlib or seaborn to create scatter plots and visualize the line of best fit.
# - Here is an example of how to create a scatter plot with a fitted line:
# ```python
# import matplotlib.pyplot as plt
#
# # define the data
# X = [0, 1, 2]
# y = [0, 1, 2]
#
# # plot the data
# plt.scatter(X, y)
#
# # plot the fitted line
# plt.plot(X, y)
#
# # show the plot
# plt.show()
# Is there anything else you would like to know?
# ```
# """)))

