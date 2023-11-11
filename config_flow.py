from homeassistant import config_entries
from .const import DOMAIN, CONFIG_SCHEMA, DOMAIN_SCHEMA

class DomeneshopDDNSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Domeneshop DDNS config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate user input
            valid = await self.is_valid(user_input)
            if valid:
                return self.async_create_entry(
                    title="DomeneShop DDNS User data",
                    data={
                        "username": user_input["username"],
                        "password": user_input["password"],
                        "domain": user_input["domain"]
                    },
                    options={
                        "timeout": user_input["timeout"]
                    },
                )

            errors["base"] = "auth_error"

        return self.async_show_form(
            step_id="user",
            data_schema= DOMAIN_SCHEMA,
            errors=errors
        )

    async def is_valid(self, user_input):
        return True
