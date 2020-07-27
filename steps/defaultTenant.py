from http import HTTPStatus

from behave import *

from src.helpers.api.managers_helper import ManagersHelper
from src.helpers.api.platform_helper import PlatformHelper
from src.helpers.api.user_helper import UserHelper
from src.helpers.utils.utils_helper import UtilsHelper
from src.helpers.web.platform_admin.admin_signin_helper import AdminSigninHelper
import src.framework.global_config as config
from selenium import webdriver

use_step_matcher("re")
user_helper = UserHelper()
utils_helper = UtilsHelper()
admin_signin_helper = AdminSigninHelper()
managers_helper = ManagersHelper()
platform_helper = PlatformHelper()
admin_signup_helper = AdminSigninHelper()
tenant_name = "QWIL"
user_pk = None
manager_name = None
email = None
managers_id = None
platform_name = None
manager_user = None
manager_id = None

driver = webdriver.Chrome(
    executable_path='/Users/Sapthagiri/Workspace/Automation repo/api-automation-repo/src/drivers/chromedriver')
config.DRIVER = driver


@given("I create a new User")
def create_new_user(context):
    global user_pk
    global email
    user = utils_helper.get_new_user()
    response = user_helper.create_user(user)
    user_pk = response["url"].split("/")[-2]
    assert user_pk is not None
    email = response["email"]
    print(response)


@step("I make the created User as Demo Manager")
def create_demo_manager(context):
    global manager_name
    global manager_id
    response = user_helper.create_users_as_demo_manager(
        email=email,
        password=utils_helper.get_default_password(),
        name=utils_helper.get_manager_name(),
        user_pk=user_pk,
        expected=HTTPStatus.CREATED,
    )
    manager_id = response["url"].split("/")[-2]
    manager_name = response["name"]
    print("*****")
    print("manager_id:", manager_id)
    assert manager_id is not None

    print("tenant_name:", tenant_name)


@then("the created Manager should be assigned with default tenant")
def check_manager_tenant(context):
    tenant_name = admin_signin_helper.check_the_manager_is_qwil_enabled_tenant(
        manager_name=manager_name
    )
    assert tenant_name == "QWIL"


@then("I login to Qwil admin and check the user is assigned with default tenant")
def check_user_tenant(context):
    tenant_name = admin_signin_helper.check_the_user_is_qwil_enabled_tenant(
        user_email=email
    )
    print(tenant_name)
    assert tenant_name == "QWIL"


@step("I check created Manager is assigned with default tenant")
def step_impl(context):
    admin_signin_helper.check_the_manager_is_qwil_enabled_tenant(
        manager_name=manager_name
    )


@given("I create a new user through Qwil admin")
def step_impl(context):
    global manager_user
    admin_signup_helper.visit_page()
    user_a = utils_helper.get_new_user()
    admin_signup_helper.admin_login()
    admin_signup_helper.login_as_qwil_admin_and_new_user(
        email=user_a["email"],
        password=utils_helper.get_default_password(),
        confirm_password=utils_helper.get_default_password(),
        tenant_name=tenant_name
    )
    manager_user = user_a["email"]
    print(manager_user)


@step("I create a Manager")
def step_impl(context):
    global manager_name
    manager_name = utils_helper.get_manager_name()
    admin_signup_helper.login_as_qwil_admin_and_add_manager(
        tenant_name=tenant_name,
        manager_name=manager_name,
        email=manager_user,
    )


@step("I make the created Manager as tenant")
def step_impl(context):
    global manager_id
    manager_id = admin_signup_helper.login_as_qwil_admin_and_make_manager_as_tenants(
        manager_name=manager_name,
        tenant_name=tenant_name
    )
    print(manager_id)


@step("I create a platform")
def step_impl(context):
    user_b = utils_helper.get_new_user()
    global platform_pk
    global platform_name
    print("*****")
    print("tenant_name:", tenant_name)
    print("manager_id:", manager_id)
    response = managers_helper.create_managers_platform_by_id(
        manager_id=manager_id,
        name=manager_name,
        user=user_b,
        email="arvind+01@qwil.com",
        expected=HTTPStatus.CREATED,
    )
    platform_pk = response["url"].split("/")[-2]
    platform_name = response["name"]
    assert platform_pk is not None


@step("I activate the platform")
def step_impl(context):
    response = platform_helper.activate_platform_by_id(
        platform_id=platform_pk, email="arvind02@qwil.com", expected=HTTPStatus.OK
    )
    print(response)


@then("the created platform should be assigned with default tenant")
def check_platform_tenant(context):
    tenant_name = admin_signin_helper.check_the_platform_is_qwil_enabled_tenant(
        platform_name=platform_name
    )
    assert tenant_name == "QWIL"
