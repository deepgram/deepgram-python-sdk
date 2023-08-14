import pytest
import pytest_asyncio  # Required to ensure pytest-asyncio is installed
from deepgram import Deepgram


api_key = pytest.api_key
assert api_key, "Pass Deepgram API key as an argument: `pytest --api-key <key> tests/`"

deepgram = Deepgram(api_key)


@pytest.mark.asyncio  # Requires pytest-asyncio to be installed
async def test_projects_and_billing():
    """
    Test to ensure that projects and billing are working as expected.
    """
    projects = await deepgram.projects.list()
    assert projects['projects'] is not None
    if len(projects['projects']) > 0:
        project = projects['projects'][0]
        project_id = project['project_id']
        response = await deepgram.billing.list_balance(project_id)
        assert 'balances' in response
        balances = response['balances']
        assert type(balances) == list
        balance_id = balances[0]['balance_id']
        amount = balances[0]['amount']
        units = balances[0]['units']
        purchase_order_id = balances[0]['purchase_order_id']
        assert type(balance_id) == str
        assert type(amount) == float
        assert type(units) == str
        assert type(purchase_order_id) == str