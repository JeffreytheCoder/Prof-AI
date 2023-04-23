import os
import sys
import random
import requests
import subprocess
import re
from dotenv import load_dotenv


def convert_md(file_string):
    replaced_file_string = replace_image_with_url(get_images_by_keywords(find_image_keywords(file_string)), file_string)
    hash = random.getrandbits(128)
    print("hash value: %032x" % hash)
    f = open(f"../docs/{hash}.md", "w")
    f.write(replaced_file_string)
    f.close()
    subprocess.run(["marp", f"../docs/{hash}.md", "-o", f"../docs/{hash}.pdf"])


def replace_image_with_url(res, file_string):
    for key in res:
        side = "left"
        url = res[key][0]
        if random.randint(0, 1) == 0:
            side = "right"
        if res[key][1] > res[key][2]:
            format_image = f"bg fit {side}:{random.randint(20,40)}%"
        else:
            format_image = f"bg fit {side}"
        file_string = file_string.replace(f"<image> (keyword: {key})", f"![{format_image}]({url})")
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
        'num': '5',
        'q': query + ' concept explained',
        'searchType': 'image',
        'key': key,
        'imgSize': 'medium',
    }
    response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
    data = response.json()
    res = random.choice(data['items'])
    return res['link'], res['image']['height'], res['image']['width']


file_test = """# Introduction to Linear Regression

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
"""

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

file = """# Slide 1: Socket Programming with UDP
- Processes communicate by sending messages into sockets.
- UDP packets require a destination address be attached before being sent.
- Client sends a packet to the server's socket with destination address attached.

<image> (keyword: UDP Socket Programming)

---

# Slide 2: Destination Address in UDP
- Destination address includes destination host’s IP address and socket's port number.
- Routers in the Internet use destination IP address to route packet to destination host.
- Destination socket's port number identifies the particular socket in the destination host.

<image> (keyword: UDP Destination Address)

---

# Slide 3: UDP Client-Server program
- Client reads a line, sends to server.
- Server receives data, modifies to uppercase.
- Server sends modified data to client.

<image> (keyword: UDP program)

---

# Slide 4: Client Side of Application
- Create clientSocket with a random port number.
- Client sends message to server with message and destination address with sendto().
- Client waits for server response.

<image> (keyword: UDP Client Side)

---

# Slide 5: Server Side of Application
- Bind the port number 12000 to the server’s socket.
- Waits for client request, receives data from client.
- Modifies data and sends modified data to client's address.

<image> (keyword: UDP Server Side)

---

# Slide 6: Testing the Application
- Run UDPClient.py on one host and UDPServer.py on another host.
- Be sure to provide the proper hostname or IP address of the server in UDPClient.py.
- Execute UDPServer.py on the server host.
- Execute UDPClient.py on client host.
- Try various sentenses and get updated capitalized sentences back.

<image> (keyword: UDP application test)"""

convert_md(file)
print(get_images_by_keywords(find_image_keywords(file)))
