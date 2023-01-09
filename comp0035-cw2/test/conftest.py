import pytest
import user
from datetime import date


@pytest.fixture(scope='function')
def data_analyst():
    data_user = user.User(first_name='analyst', last_name='data',
                          email='email@gmail.com', password='unknown13j78',
                          dob=date(2001, 12, 10))
    yield data_user
