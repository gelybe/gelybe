from pytest_bdd import scenario

from pytest_bdd import (
    given,
    scenarios,
    then,
    when,
)


@given('Пользователь заходит на страницу авторизации')
def user_is_on_login_page():
    """Пользователь заходит на страницу авторизации."""
    pass


@when('Пользователь вводит свой логин и пароль')
def user_fills_valid_username_and_password():
    """Пользователь вводит свой логин и пароль"""
    pass


@when('кликает на кнопку войти')
def clicks_on_submit_button():
    """кликает на кнопку войти."""
    pass


@then('Пользователь прошел авторизацию и видит стартовую страницу')
def user_is_able_to_login_and_view_landing_page():
    """Пользователь прошел авторизацию и видит стартовую страницу."""
    pass


@scenario("../features/login.feature", "Вход в приложение")
def test_enter_in_app():
    """Вход в приложение."""
    pass