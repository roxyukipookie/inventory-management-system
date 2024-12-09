<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/roxyukipookie/inventory-management-system
">
    <img src="stock_inventory/static/images/LOGO.png" alt="Logo" width="100" height="100">
  </a>

<h3 align="center">Product Inventory Management System</h3>

  <p align="center">
    The Inventory Management System is a Django-based web application designed to streamline the management of product inventories for businesses. This solution is ideal for businesses seeking an efficient and reliable way to manage their inventory operations.
    <br />
    <a href="https://github.com/roxyukipookie/inventory-management-system"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/roxyukipookie/inventory-management-system">View Demo</a>
    ·
    <a href="https://github.com/roxyukipookie/inventory-management-system/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/roxyukipookie/inventory-management-system/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Screen Shot][product-screenshot]](https://github.com/roxyukipookie/inventory-management-system)

This project aims to address the challenges faced by small businesses in managing their product inventory effectively. This application will transform existing processes by providing an automated, user-friendly system that simplifies inventory management. The application will support small business owners by enabling them to track stock levels in real-time, manage product details, receive alerts for low stock levels, and maintain accurate sales records.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Django][Django-shield]][Django-url]
* [![HTML][HTML-shield]][HTML-url]
* [![CSS][CSS-shield]][CSS-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features

1. **User Registration and Authentication:** Users can create accounts and log in securely.
2. **Dashboard:** Users can view key metrics, such as total stock quantity, products running low on stock, and recent transactions
3. **Product Management:** Users can add, update, and delete products, including details like name, description, quantity, and price.
4. **Transaction History:** View the list of past transactions, including product sales and inventory adjustments.
5. **Role-Based Access Control:** Different user roles with varying levels of access to features and data.
6. **Notifications:** Receive alerts for low stock levels, new product arrivals, and more.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy of this project up and running, follow these simple steps.

### Prerequisites

#### 1. Install Python
Install ```python-3.12.5```. Follow the steps from the below reference document based on your Operating System.
Reference: [https://docs.python-guide.org/starting/installation/](https://docs.python-guide.org/starting/installation/) 

#### 2. Setup virtual environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv/scripts/Activate

# Install dependencies
pip install django-excel
pip pillow
```

#### 3. Clone git repository
```bash
git clone "https://github.com/roxyukipookie/inventory-management-system.git"
```

#### 4. Install requirements
```bash
cd stock_inventory/
pip install -r requirements.txt
```

#### 5. Run the server
```bash
# Make migrations
python manage.py makemigrations
python manage.py migrate

# Run the server
python manage.py runserver

# your server is up on port 8000
```
Try opening [http://localhost:8000](http://localhost:8000) in the browser.
Now you are good to go.

<!-- USAGE EXAMPLES -->
## Usage
Useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space.

### Dashboard:
[![Product Screen Shot][product-screenshot]](https://github.com/roxyukipookie/inventory-management-system)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/roxyukipookie/inventory-management-system/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=roxyukipookie/inventory-management-system" alt="contrib.rocks image" />
</a>


# Links:
https://docs.google.com/spreadsheets/d/1OFXsZk7QUNmsHOwiR8ewBccnk4cWuhCA/edit?usp=sharing&ouid=111017210003517529526&rtpof=true&sd=true

https://www.figma.com/design/UDq0B6N5ZnCryDHuMJXyVh/Product-Inventory?node-id=0-1&t=xWjwR97Uu3pIvADi-1

https://lucid.app/lucidchart/b5c83653-cc57-4b7e-9603-799dd79cbe4c/edit?viewport_loc=-307%2C-363%2C4459%2C2345%2C0_0&invitationId=inv_29864427-542b-4a66-a26e-b95757951efe

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/roxyukipookie/inventory-management-system.svg?style=for-the-badge
[contributors-url]: https://github.com/roxyukipookie/inventory-management-system/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/roxyukipookie/inventory-management-system.svg?style=for-the-badge
[issues-url]: https://github.com/roxyukipookie/inventory-management-system/issues
[license-shield]: https://img.shields.io/github/license/roxyukipookie/inventory-management-system.svg?style=for-the-badge
[license-url]: https://github.com/roxyukipookie/inventory-management-system/blob/master/LICENSE.txt
[product-screenshot]: stock_inventory/static/images/screenshot2.png
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[Django-shield]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[HTML-shield]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
[CSS-shield]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
