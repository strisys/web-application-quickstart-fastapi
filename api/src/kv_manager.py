import os, logging
from azure.identity import DefaultAzureCredential, ChainedTokenCredential, AzureCliCredential, EnvironmentCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
dotenv_path = current_dir / '.env'
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class KeyVaultUtility:    
    def init(self, vault_name: Optional[str] = None, credential: Optional[ChainedTokenCredential] = None):
        try:
            if (not credential):
                credential = ChainedTokenCredential(AzureCliCredential(), EnvironmentCredential(), ManagedIdentityCredential())

            vault_name = (vault_name or os.getenv("KEY_VAULT_NAME", None))

            if (not vault_name):
                raise Exception("Vault name not provided through argument or environment variable KEY_VAULT_NAME")

            vault_url = f"https://{vault_name}.vault.azure.net/"
            self.credential = credential
            self.client = SecretClient(vault_url=vault_url, credential=self.credential)
        except Exception as e:
            logger.error(f"Failed to initialize Key Vault client ({vault_url}): {str(e)}")
            raise

    def try_get_secret(self, secret_name: str, version: Optional[str] = None) -> Optional[str]:
        try:
            secret = self.client.get_secret(secret_name, version=version)
            return secret.value
        except Exception as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {str(e)}")
            return None

    def get_secret(self, secret_name: str, version: Optional[str] = None) -> Optional[str]:
        secret = self.try_get_secret(secret_name, version)

        if (not secret):
            raise Exception(f"Failed to retrieve secret {secret_name}")

        return secret

    def load_secrets_to_env(self, prefix: str = "", secret_mapping: dict[str, str] = {}) -> dict[str, bool]:
        try:
            secrets = self.client.list_properties_of_secrets()
            results = {}

            for secret_properties in secrets:
                secret_name = secret_properties.name

                if (not secret_name):
                    continue

                results[secret_name] = False
                env_var_name = secret_mapping.get(secret_name, secret_name)
                env_var_name = f"{prefix}{env_var_name}".upper()

                if os.getenv(env_var_name) is not None:
                    logger.info(f"Environment variable already exists as environment variable: {env_var_name}")

                    continue

                secret_value = self.try_get_secret(secret_name)

                if secret_value is not None:
                    os.environ[env_var_name] = secret_value
                    assert os.environ.get(env_var_name) == secret_value
                    logger.info(f"Loaded secret into environment variable: {env_var_name}")
                    results[secret_name] = True

            logger.info(f"Successfully loaded secrets into environment variables: {','.join([name for name, loaded in results.items() if loaded])}")

            return results    
        except Exception as e:
            logger.error(f"Error loading secrets into environment: {str(e)}")
            return {}