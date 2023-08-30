# efarm Django Project
![GitHub top language](https://img.shields.io/github/languages/top/peter-evance/demo-efarm)
![GitHub last commit](https://img.shields.io/github/last-commit/peter-evance/demo-efarm)
![GitHub repo size](https://img.shields.io/github/repo-size/peter-evance/demo-efarm)

## Introduction

efarm is a Django project designed to help farmers streamline their operations by providing a digital platform for precision agriculture. The project consists of three apps mainly - Dairy, Poultry, and Swine. Each app has different models for managing data relevant to that sector of agriculture.

## Installation

1. Clone the repository using `git clone https://github.com/peter-evance/demo-efarm.git`.
2. Change into the `efarm` directory using `cd efarm`.
3. Create a virtual environment using `python3 -m venv env`.
4. Activate the virtual environment using `source env/bin/activate` on Linux/macOS or `.\env\Scripts\activate` on Windows.
5. Install the dependencies using `pip install -r requirements.txt`.
6. Run migrations using `python manage.py migrate`.
7. Start the development server using `python manage.py runserver`.
8. Run the `python manage.py createsuperuser` and create a superuser of you own liking, you can delete the database in
or use the username (peterevance) and password (qq) for the database you find in this repository.

## Usage

Once the development server is running, you can access the efarm app on `http://localhost:8000/`. From here, you can navigate to the different apps and models to view and manage data relevant to your farm.

## Feedback

I value your feedback on how we can improve the efarm project.

## Contributing

I welcome contributions to the efarm project. Please read [contribution guidelines](CONTRIBUTING.md) before submitting a pull request.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
