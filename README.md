Requirements:
1) Docker
2) Python 3.6+

Run the following command to start Keycloak server:

>docker run -p 8080:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:26.0.6 start-dev

Configure your Keycloak client and google identity provider.
Check if credentials are correct in the python files then run the server.
Add `.env` file to the project with the configuration below.

```env
HR_OAUTH2_CLIENT_ID=hr_web_app
HR_OAUTH2_CLIENT_SECRET=""
CRM_OAUTH2_CLIENT_ID=crm_web_app
CRM_OAUTH2_CLIENT_SECRET=""

OAUTH2_ISSUER=http://localhost:8080/realms/AuthApp
FLASK_SECRET=MyLongFlaskSecret

HR_FLASK_PORT=3000
CRM_FLASK_PORT=3001
```
