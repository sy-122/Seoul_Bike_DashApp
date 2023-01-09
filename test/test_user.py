from user import User

def test_user_calculate_age_return_correct_value(data_analyst):
    """
    GIVEN a new user of a dob=date(2001, 12, 10) (created as a fixture)
    WHEN the user is passed to User.calculate_age function
    THEN the result should equal 20
    """
    age = User.calculate_age(data_analyst)
    assert age == 20

def test_user_correct_password(data_analyst):
    """
    GIVEN a new user (created as a fixture)
    WHEN password passed to User.is_correct_password is correct
    THEN it should return TRUE
    """
    result = User.is_correct_password(data_analyst, 'unknown13j78')
    assert result is True

def test_user_incorrect_password(data_analyst):
    """
    GIVEN a new user (created as a fixture)
    WHEN password passed to User.is_correct_password is incorrect
    THEN it should return FALSE
    """
    result = User.is_correct_password(data_analyst, '12345')
    assert result is False


