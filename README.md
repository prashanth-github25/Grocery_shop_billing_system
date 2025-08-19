# Grocery_shop_billing_system
This is a simple project on grocery shop billing system made using Python and FastAPI(backend) and also Jinja2templates(frontend).
The system allows users(shopkeepers) to manage products, update stock, and generate bills with discount support.
It provides a user friendly interface for the shopkeeper to make it easy for usage.

----------Features----------
- Add, update, and remove products from the inventory
- Manage stock levels
- Generate bills for customers
- Apply discounts automatically to the total bill by just providing the perecntage
- Persistent data storage using JSON file

----------Tech used----------
- Python
  Python is a high-level, interpreted programming language known for its readability and versatility. It supports multiple programming styles and has a large standard library.
  
- FastAPI
  FastAPI is a modern, high-performance Python web framework designed for building APIs. We can say it's been used to connect backend and frontend
  
- Jinja2templates
  FastAPI does not include built-in support for rendering HTML templates but seamlessly integrates with template engines like Jinja2. This allows for dynamic HTML generation and serving within a FastAPI application.
  
- Uvicorn
  Uvicorn is a lightning-fast Asynchronous Server Gateway Interface (ASGI) web server implementation for Python. It is commonly used to serve asynchronous Python web applications, particularly those built with frameworks like FastAPI.

----------Limitations----------
- This project is currently not finished for the actual implementation at the shops, its actually a simple and basic project which does some basic things. I would like to or maybe enhance it in the future where we wil be able to actually implement the software in the shops.
- Currently it has no database, it just has json file which stores only the inventory products, and is not suitable for large scale implementation.
- We can say this as a project suitable for college submissions

----------How to run----------
- Open VS code(or any other code editors)
- Clone the grocery_shop1 file
- Install FastApi, Jinja2templates and Uvicorn (search in google how to) in the terminal (refer requirements.txt if nescessary)
- Run the command -> python -m uvicorn main:app --reload
- Then open the URL, your server will be running and the home page will be opened in the browser. 
