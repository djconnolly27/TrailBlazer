# Implementation
Trail Blazer has several key components, all of which are integrated into the GUI design. To begin, our GUI handles the interactions between the users and the programs and additionally controls how all of the visuals are ultimately displayed. When the GUI sends a request for a new route, the route-finding portion of Trail Blazer, which relies heavily on its Graph and Edge classes, comes into play. At the same time, the GUI queries for and displays elevation and weather data.

Below is a class diagram of Trail Blazer in its current state:
![alt text](images/SoftDes_Final_UML.svg)

Trail Blazer's performance is rather intimately tied to the size of the graph it creates. In other words, the performance of Trail Blazer changes greatly depending on the geographic area in which you utilize it. For instance, in an area of southeastern Iowa with few roads and intersections, the depth-first algorithm Trail Blazer employs easily queries for and plots routes of up to 15 kilometers.

In contrast, in denser areas such as cities like Boston, Trail Blazer has difficulty locating cycles in the graph that are longer than 3 kilometers.
