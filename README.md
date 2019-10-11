[![codebeat badge](https://codebeat.co/badges/39c486b0-d8cd-4212-bd9b-4f4e17908814)](https://codebeat.co/projects/github-com-mandelak-ourcommerce-develop) [![Maintainability](https://api.codeclimate.com/v1/badges/5c4a7339c188399bf36c/maintainability)](https://codeclimate.com/github/MandelaK/ourcommerce/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/5c4a7339c188399bf36c/test_coverage)](https://codeclimate.com/github/MandelaK/ourcommerce/test_coverage) [![Coverage Status](https://coveralls.io/repos/github/MandelaK/ourcommerce/badge.svg?branch=develop)](https://coveralls.io/github/MandelaK/ourcommerce?branch=develop)

Welcome to ourCommerce. This is an ecommerce platform that contains a broad API and lots of features in the pipeline.




## Setting Up
- [ ] Clone repo
- [ ] Create a virtual environment and make sure to use python 3.6. Run command `virtualenv venv --python=python3.6`
- [ ] Install dependencies by running `pip install -r server/requirements.txt`
- [ ] Populate your environment variables by running `cp server/.env.sample server/.env` and filling your `server/.env` file with proper values.
- [ ] Set up your Postgres DB and run migrations using `python server/manage.py migrate`
- [ ] Start the backend API by running `python server/manage.py runserver`


## Testing
- [ ] Ensure to populate and source your `server/.env` file.
- [ ] Simply run `tox`

## Contributing


## License

