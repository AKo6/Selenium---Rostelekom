import pytest


from auth_page import AuthPage
from config_page import RegPage


# Тест-кейс N-001
# Корректное отображение "Страницы авторизации"
def test_start_page_is_correct(web_browser):
    page = AuthPage(web_browser)
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert phone_tab_class == "rt-tab rt-tab--small rt-tab--active"
    assert page.phone.is_clickable()
    assert page.password.is_clickable()
    assert page.btn_login.is_clickable()
    assert page.registration_link.is_clickable()
    assert page.auth_title.get_text() == "Авторизация"
    assert page.logo_lk.get_text() == "Личный кабинет"


# Тест-кейс N-001 (Баг N-001)
# Проверка элементов в левом и правом блоке страницы
@pytest.mark.xfail(reason="Расположение элементов на странице не соответствует документации")
def test_location_of_page_blocks(web_browser):
    page = AuthPage(web_browser)
    assert page.auth_form.find(timeout=1)
    assert page.lk_form.find(timeout=1)


# Тест-кейс N-001(Баг N-003)
# Проверка названия кнопки "Номер"
@pytest.mark.xfail(reason="Название кнопки 'Номер' не соответствует документации")
def test_phone_tab(web_browser):
    page = AuthPage(web_browser)
    assert page.phone_tab.get_text() == "Номер"


# Тест-кейс N-007 (Баг N-012)
# Проверка названия кнопки "Продолжить" в форме "Регистрация"
@pytest.mark.xfail(reason="Кнопка должна иметь текст 'Продолжить'")
def test_registration_page_and_continue_button(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    assert reg_page.name_field_text.get_text() == "Имя"
    assert reg_page.last_name_field_text.get_text() == "Фамилия"
    assert reg_page.region_field_text.get_text() == "Регион"
    assert reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон"
    assert reg_page.password_field_text.get_text() == "Пароль"
    assert reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля"
    assert reg_page.continue_button.get_text() == "Продолжить"


# Тест-кейс N-009
# Регистрация пользователя с пустым полем "Имя"
def test_registration_page_with_empty_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('')
    reg_page.last_name_field.send_keys("Кобылинский")
    reg_page.email_or_mobile_phone_field.send_keys("test.kob2022@gmail.com")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс N-010
# Регистрация пользователя со значением в поле "Имя" меньше двух символов
def test_registration_with_an_incorrect_value_in_the_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('А')
    reg_page.last_name_field.send_keys("Кобылинский")
    reg_page.email_or_mobile_phone_field.send_keys("test.kob2022@gmail.com")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс N-011
# Регистрация пользователя со значением в поле "Фамилия" превышающим 30 символов
def test_registration_with_an_incorrect_value_in_the_last_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Александр")
    reg_page.last_name_field.send_keys("Кооооббббыыыылиииинсссссскиииий")
    reg_page.email_or_mobile_phone_field.send_keys("test.kob2022@gmail.com")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс N-012
# Регистрация пользователя с вводом недопустимых символов в поле "Фамилия"
def test_instead_of_cyrillic_invalid_characters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Александр")
    reg_page.last_name_field.send_keys("!@№;%:?*()_+=-?")
    reg_page.email_or_mobile_phone_field.send_keys("test.kob2022@gmail.com")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс N-013
# Регистрация пользователя с вводом невалидной электронной почты в поле ввода "Email или мобильный телефон"
def test_invalid_email_or_mobile_phone(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Антон")
    reg_page.last_name_field.send_keys("Чехов")
    reg_page.email_or_mobile_phone_field.send_keys("chehonte@mailru")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email в формате example@email.ru"

# Тест-кейс N-014
# Регистрация пользователя со значением в поле "Пароль"  менее 8 символов
def test_incorrect_password_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Антон")
    reg_page.last_name_field.send_keys("Чехов")
    reg_page.email_or_mobile_phone_field.send_keys("chehonte@mailru")
    reg_page.password_field.send_keys("Test1")
    reg_page.password_confirmation_field.send_keys("Test1")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"


# Тест-кейс N-015 (Баг NN-014)
# Значения в поле ввода "Пароль" и поле ввода "Подтверждение пароля" в форме "Регистрация" не совпадают
def test_password_and_password_confirmation_do_not_match(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Антон")
    reg_page.last_name_field.send_keys("Чехов")
    reg_page.email_or_mobile_phone_field.send_keys("chehonte@mailru")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("54321Test")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


# Тест-кейс N-016
# Регистрация пользователя со значением в поле "Пароль" без заглавных букв
def test_password_and_password_do_not_have_capital_letters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Антон")
    reg_page.last_name_field.send_keys("Чехов")
    reg_page.email_or_mobile_phone_field.send_keys("chehonte@mailru")
    reg_page.password_field.send_keys("test12345")
    reg_page.password_confirmation_field.send_keys("test12345")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароль должен содержать хотя бы одну заглавную букву"

# Тест-кейс N-017
# Форма регистрации. Негативный сценарий
def test_negative_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Ааааааааааннннтттттооооооооооон")
    reg_page.last_name_field.send_keys("Ч")
    reg_page.email_or_mobile_phone_field.send_keys("chehonte.mailru")
    reg_page.password_field.send_keys("test12345")
    reg_page.password_confirmation_field.send_keys("54321Test")
    reg_page.continue_button.click()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email в формате example@email.ru"
    assert reg_page.error_message_password.get_text() == "Пароль должен содержать хотя бы одну заглавную букву"
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


# Тест-кейс N-018
# Регистрация пользователя с уже зарегистрированной почтой
def test_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Антон")
    reg_page.last_name_field.send_keys("Чехов")
    reg_page.email_or_mobile_phone_field.send_keys("test.kob2022@gmail.com")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible


# Тест-кейс N-020
# Регистрация пользователя с уже зарегистрированным номером
def test_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Антон")
    reg_page.last_name_field.send_keys("Чехов")
    reg_page.email_or_mobile_phone_field.send_keys("+79063612597")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible


# Тест-кейс N-020(Баг N-017,Баг N-018 )
# Проверка кнопки "Х" - закрыть всплывающее окно в оповещающей форме
@pytest.mark.xfail(reason="Должен быть значок закрыть 'х'")
def test_notification_form(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Антон")
    reg_page.last_name_field.send_keys("Чехов")
    reg_page.email_or_mobile_phone_field.send_keys("+79063612597")
    reg_page.password_field.send_keys("Test12345")
    reg_page.password_confirmation_field.send_keys("Test12345")
    reg_page.continue_button.click()
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'


# Тест-кейс N-021
# Авторизация зарегистрированного пользователя с неправильным паролем
def test_authorization_of_a_user_with_an_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79063612597')
    page.password.send_keys("Test")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')


# Тест-кейс N-022
# Тестирование аутентификации зарегистрированного пользователя по электронной почте
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys("test.kob2022@gmail.com")
    page.password.send_keys("Test12345")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()

# Тест-кейс N-023
# Тестирование аутентификации зарегистрированного пользователя по номеру телефона
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys("+79063612597")
    page.password.send_keys("Test12345")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс N-024
# Тестирование аутентификации зарегистрированного пользователя по логину
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys("rtkid_1671898539730")
    page.password.send_keys("Ermolina1997")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс N-025 (Баг N-009)
# Тестирование аутентификации зарегистрированного пользователя по лицевому счёту
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys("125930510062")
    page.password.send_keys("Test12345")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()