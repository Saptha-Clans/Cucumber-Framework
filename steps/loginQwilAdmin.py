from behave import *
from src.helpers.api.managers_helper import ManagersHelper
from src.helpers.api.platform_helper import PlatformHelper
from src.helpers.web.platform_admin.admin_signin_helper import AdminSigninHelper
from src.helpers.api.user_helper import UserHelper
from src.helpers.utils.utils_helper import UtilsHelper
import logging
from selenium import webdriver
import src.framework.global_config as config
from http import HTTPStatus

use_step_matcher("re")
admin_signup_helper = AdminSigninHelper()
user_helper = UserHelper()
utils_helper = UtilsHelper()
user_a = None
user_b = None
user_c = None
managers_helper = ManagersHelper()
platform_helper = PlatformHelper()
contractor = utils_helper.get_new_contractor()
url = None
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
utils_helper = UtilsHelper()
tenant_name = "test-tenant"
manager_view = "manager/manager/?tenant=1"
platform_view = "user/platform/?tenant=1"
driver = webdriver.Chrome(executable_path='/Users/Sapthagiri/Workspace/Automation repo/api-automation-repo/src/drivers/chromedriver')
config.DRIVER = driver
manager_id = None
platform_id = None
manager_user = None
manager_name = None

@given("I am in the Qwil admin webpage")
def visit_qwil_admin_page(context):
    admin_signup_helper.visit_page()

@when("I enter the user email and password and login")
def enter_email_and_password(context):
    admin_signup_helper.admin_login()

@step("I visit the user detail page and create a user")
def create_a_user(context):
    global manager_user
    global user_a
    user_a = utils_helper.get_new_user()
    admin_signup_helper.login_as_qwil_admin_and_new_user(
        email=user_a["email"],
        password=utils_helper.get_default_password(),
        confirm_password=utils_helper.get_default_password(),
        url=url,
    )
    manager_user = user_a["email"]
    print(manager_user)

@step("I make the created user as Manager and assign tenant")
def create_a_manager(context):
    global manager_name
    global manager_id

    manager_name = utils_helper.get_manager_name()
    print("***********")
    print("MANAGER_NAME", manager_name)
    print("***********")
    admin_signup_helper.login_as_qwil_admin_and_add_manager(
        tenant_name=tenant_name,
        manager_name=manager_name,
        email=user_a["email"],
        url=url,
    )

    manager_id = admin_signup_helper.login_as_qwil_admin_and_make_manager_as_tenants(
        url=url, manager_name=manager_name, tenant_name=tenant_name
    )
    print("***********")
    print("Manager_id:", manager_id)
    print("***********")


# @step("I assign tenant to the created Manager")
# def make_created_manager_as_tenant(context):
#     #manager_name = utils_helper.get_manager_name()


@step("I create a platform under the Manager")
def create_platform(context):
    global platform_id
    #manager_id = make_created_manager_as_tenant(context)
    #manager_name = utils_helper.get_manager_name()
    global user_c
    user_c = utils_helper.get_new_user()
    print("***********")
    print("Manager_id:", manager_id)
    print("***********")
    response = managers_helper.create_managers_platform_by_id(
        manager_id=manager_id, email=manager_user, password=utils_helper.get_default_password(), name=manager_name, user=user_c, url=url
    )
    platform_id = response["url"].split("/")[-2]
    print("***********")
    print("PLATFORM_ID", platform_id)
    print("***********")
    # context.create_contractor(platform_id=platform_id)
    #return platform_id
    platform_id = response["url"].split("/")[-2]
    platform_name = response["name"]
    print(platform_id)

    # step3: set invoice_payment_recipient as Qwil Controlled Account and is_without_direct_terms
    admin_signup_helper.set_platform_invoice_payment_and_direct_terms(
        platform_name=platform_name, value="qwil controlled account", url=url
    )

    # step5: Activate platform

    admin_signup_helper.activate_platform(
        platform_name,
        url=url,
        expecting_activate_message=True,
        view=platform_view,
    )

@step("I add Contractor to the Platform")
def create_contractor(context):
    #platform_id = create_platform(context)
    print("***********")
    print("PLATFORM_ID", platform_id)
    print("***********")
    response = platform_helper.add_contractor_to_platform(
        platform_pk=platform_id,
        contractor_dict=contractor,
        email=manager_user,
        password=utils_helper.get_default_password(),
        url=url,
        expected=HTTPStatus.CREATED,
    )

@then("I was able to successfully add a contractor under a platform")
def step_impl(context):
    print("Successfully created a contractor under a platform")

@step("I add Contractor to the under a Manager")
def add_contractor_under_tenant_manager(context):
    # member = make_created_manager_as_tenant()
    # manager_id = member.manager_id
    global user_b
    user_b = utils_helper.get_new_user()
    print("***********")
    print("Manager_id:", manager_id)
    print("***********")
    managers_helper.create_managers_contractors_by_id(
        manager_id=manager_id,
        email=manager_user,
        password=utils_helper.get_default_password(),
        user=user_b,
        contractor=contractor,
        expected=HTTPStatus.CREATED,
    )

@then("I was able to successfully add a contractor under a Manager")
def step_impl(context):
    print("successfully add a contractor under a Manager")


@step("I logout the Qwil admin")
def step_impl(context):
    admin_signup_helper.admin_logout()