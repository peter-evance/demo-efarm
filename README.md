# eFarm Django Project

## Introduction

eFarm is a Django project designed to help farmers streamline their operations by providing a digital platform for precision agriculture. The project consists of three apps - Dairy, Poultry, and Swine. Each app has different models for managing data relevant to that sector of agriculture.

## Installation

1. Clone the repository using `git clone https://github.com/peter-evance/demo-efarm.git`.
2. Change into the `efarm` directory using `cd efarm`.
3. Create a virtual environment using `python3 -m venv env`.
4. Activate the virtual environment using `source env/bin/activate` on Linux/macOS or `.\env\Scripts\activate` on Windows.
5. Install the dependencies using `pip install -r requirements.txt`.
6. Run migrations using `python manage.py migrate`.
7. Start the development server using `python manage.py runserver`.

## Usage

Once the development server is running, you can access the eFarm app on `http://localhost:8000/`. From here, you can navigate to the different apps and models to view and manage data relevant to your farm.

## Feedback

I value your feedback on how we can improve the eFarm project.

## Contributing

I welcome contributions to the eFarm project. Please read [contribution guidelines](CONTRIBUTING.md) before submitting a pull request.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
