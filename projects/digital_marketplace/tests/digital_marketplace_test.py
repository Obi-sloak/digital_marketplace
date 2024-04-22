import algokit_utils
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algokit_utils.beta.algorand_client import AlgorandClient, PayParams, AssetCreateParams
from algokit_utils.beta.account_manager import AddressAndSigner

from smart_contracts.artifacts.digital_marketplace.client import DigitalMarketplaceClient


@pytest.fixture(scope="session")
def algorand() -> AlgorandClient:
    """Get an AlgorandClients to use through the test"""
    return AlgorandClient.default_local_net()

def dispenser(algorand: AlgodClient) -> AddressAndSigner:
    """Get the dispenser to fund test addresses"""
    return algorand.account.dispenser()

@pytest.fixture(scope="session")
def creator(algorand: AlgodClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    acct = algorand.account.random()

    algorand.send.payment(PayParams(
        sender= dispenser.address,
        receiver=acct.address,
        amount=10_000_000
    ))

    return acct

@pytest.fixture(scope="session")
def test_asset_id(creator: AddressAndSigner, algorand: AlgorandClient) -> int:
    sent_txn = algorand.send.asset_create(
        AssetCreateParams(sender=creator.address, total=10)
        )
    return sent_txn["confirmation"]["asset-index"]




@pytest.fixture(scope="session")
def digital_marketplace_clients(algorand: AlgorandClient, creator: AddressAndSigner, test_asset_id: int) -> DigitalMarketplaceClient:
    """Instantiate an application client we can use for our tests"""
    client = DigitalMarketplaceClient(
        algod_client=algorand.client.algod,
        sender=creator.address,
        signer=creator.signer,
        )

    client.create_create_application(unitaryPrice=0, assetId=test_asset_id)

def test_pass(digital_marketplace_client: DigitalMarketplaceClient):
    pass