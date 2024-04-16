pip install python-keycloak

https://www.keycloak.org/getting-started/getting-started-docker

docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:24.0.2 start-dev

https://blog.stackademic.com/integrating-keycloak-with-django-7ae39abe3a0b

## Aula Luiz

- Criar um Realm próprio: codeflix
- Criar um usuário
  - **email verified**
  - Credentials: **reset password**
    - **Não fazer temporary**
- [ ] admin ou admin@email.com?
- Request para obter um token:

```bash
curl -X POST 'http://localhost:8080/realms/codeflix/protocol/openid-connect/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=codeflix-frontend' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'username=admin@admin.com' \
--data-urlencode 'password=admin'
```

- Mover para o Postman
- Criar client-id: codeflix-admin-frontend
  - Criou tudo "padrão"
  - Nosso app não precisaria gerar o token, o client REACT que faz a criação do token.
  - Vamos criar só para testar.

### Client

- Capability config:
  - Client authentication OFF (user )

```bash
curl -X POST 'http://localhost:8080/realms/codeflix/protocol/openid-connect/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=codeflix-frontend' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'username=admin' \
--data-urlencode 'password=admin'
```

Response token

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyM0lzQXViajA5Uk45ZjlLTjFid1JFTFdBbVRaS3VWV1hNbDB4WUdvemtnIn0.eyJleHAiOjE3MTI4ODc0NzYsImlhdCI6MTcxMjg4NzE3NiwianRpIjoiNmE0YTdlMzEtYjkzMi00Yjk3LThkZjgtOTAxZGY4OGI2NWMzIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9jb2RlZmxpeCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI0YjU0YjgxMi0xY2ZhLTRjMjUtOWQ4Ny1mMjE3ZWMwYTQ5OTAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjb2RlZmxpeC1mcm9udGVuZCIsInNlc3Npb25fc3RhdGUiOiJiMmYzZDcxNC03OTU3LTRjZDctYTA4Ny1lYjQ5ZWI0ODg2MjMiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1jb2RlZmxpeCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6ImIyZjNkNzE0LTc5NTctNGNkNy1hMDg3LWViNDllYjQ4ODYyMyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiYWRtaW4gYWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbiIsImdpdmVuX25hbWUiOiJhZG1pbiIsImZhbWlseV9uYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.JmHFDtPUB_lLIEa62zN8q-PNtk_GF7SV9sSW5NSOcj04AkYR1xqNPwg3XR2QoL8_qygRwyFlzsq5mCKpdaimNXaQDH1lYo2QoZKtg5r4LYEiRqQLaMX0y47FaoU-2yQX-ZM0Dt4zIo1UjbxyLbxi-FDV6VZFLCICspEkAfzANuv8WRBdyLA87RqfWAzgJ8kEnsq2oxUnrM-cLs0HdWDnABJQC4FopKZzclV-vFISxTKaluFzv8WJWoQi4muuVL_F1J_66H4IDOOCTSg_mY_NtbR0XYUTRLykXgrDctRbek5vBciItLK7rAu0XLEVXEwCzboJEG5BPahvvKXEriEyNA",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3Y2JjMmU4Mi1jMDQzLTRmM2MtOTNiYS1iYjM2Y2I5MDcxMTAifQ.eyJleHAiOjE3MTI4ODg5NzYsImlhdCI6MTcxMjg4NzE3NiwianRpIjoiYTQ3ZDQ2MmItNDY0OC00NmFhLWE3ZjgtZWNlNDgyNzlmNmQxIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9jb2RlZmxpeCIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9yZWFsbXMvY29kZWZsaXgiLCJzdWIiOiI0YjU0YjgxMi0xY2ZhLTRjMjUtOWQ4Ny1mMjE3ZWMwYTQ5OTAiLCJ0eXAiOiJSZWZyZXNoIiwiYXpwIjoiY29kZWZsaXgtZnJvbnRlbmQiLCJzZXNzaW9uX3N0YXRlIjoiYjJmM2Q3MTQtNzk1Ny00Y2Q3LWEwODctZWI0OWViNDg4NjIzIiwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwic2lkIjoiYjJmM2Q3MTQtNzk1Ny00Y2Q3LWEwODctZWI0OWViNDg4NjIzIn0.8TK-w9ToF1MGJkgk7qNQGKf8z_Cy3_Gm51x5xi_pWOSLLtP562fVCQ0q7aoMpJguTMnDlFDxBsc9oK0Yh9vM4A",
  "token_type": "Bearer",
  "not-before-policy": 0,
  "session_state": "b2f3d714-7957-4cd7-a087-eb49eb488623",
  "scope": "profile email"
}
```

### Client

- Capability config:
  - [ ] Client authentication ON
  - [ ] Service accounts roles ONa
  -

```bash
curl -X POST 'http://localhost:8080/realms/codeflix/protocol/openid-connect/token' \
   -H 'Content-Type: application/x-www-form-urlencoded' \
   --data-urlencode 'client_id=codeflix-frontend' \
   --data-urlencode 'grant_type=client_credentials' \
   --data-urlencode 'client_secret=bmaQCatHQKKP6qEagXNDZiRnIEPoIGtZ'
```


```python
# pip install pyjwt
import jwt

token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyM0lzQXViajA5Uk45ZjlLTjFid1JFTFdBbVRaS3VWV1hNbDB4WUdvemtnIn0.eyJleHAiOjE3MTMxNDM0NTgsImlhdCI6MTcxMzE0MzE1OCwianRpIjoiMzliMmUwMWEtMjk1OS00NTFmLTkzMDQtOTZkOWE0M2E1ZTZlIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9jb2RlZmxpeCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzZDM1M2FhZC1mMzMxLTQxNmEtOWJkYS1lM2NmNjMyOTQ4M2UiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjb2RlZmxpeC1hZG1pbi1mcm9udGVuZCIsInNlc3Npb25fc3RhdGUiOiJhN2Q5MmI5MC03YTQxLTQxN2QtOGE3YS01YzZiNmJhZThhZGQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1jb2RlZmxpeCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6ImE3ZDkyYjkwLTdhNDEtNDE3ZC04YTdhLTVjNmI2YmFlOGFkZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiQWRtaW4gQWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbiIsImdpdmVuX25hbWUiOiJBZG1pbiIsImZhbWlseV9uYW1lIjoiQWRtaW4iLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSJ9.PqfxK9OSVklXnmYTzrFCy6K0pQfb5SG-MjlN5e72Y5hg8qCaEMVGO286eZUG0oEV7Rb6llMURrwmF0aI46FWEKFp-Mm6pW809XMnAPR6dElDzVJSfOJkjY2yfVtgkVPAA-FppX6feg2CWm3Q6orWFk-lBRchDufbcP8YXu1sW7iV9b2WC48YSLuRGRs_IAuTFuMQdOPoKRpeM5uGCw2rYwbuCxWr2SDl0y5FuGJ43F_WVZ8yOrwc-4gpM-FOWZp0IwlyK_zlJzpWuoqRuecJjCqJC4GuWmIe8TJxz95zsT_6ghQF1_VDIFdhLQRPf7pa5Gb6tmtREILtHWoF2s8emA"
raw_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArJiUCnHm86LdWZlIwHd247CC4/Uz5exIyjDzGH8lvhnCoXT47WoKIy3siMW9RFaeuxOIxqSFhtk5t+eXHsh2LA5dVXTQuW+W8Fc7Z+cen+ZyQYZ18hLUfKx4wJq0ph6Bo/nAXJ1d85EISLaWj3EuGgaRxTWuEPl2YvUsdkgs8KTsj9HTI91Xz7H+mXM+j4QZ6u5080B3CEspP+/iJnoHHh0Wgv7fl6UcoXQX5/VVbtRowOS4xfwLaZF4lLyd3GMcpBj+HwdN6WwEIAsAg3ap+Abq0zylU2qDGjKjv6Xyxo+zNXtFDOrzJjeXUQqD+FEWCk3QiGq+Fyi/YxAbwW1bIQIDAQAB"  # Pegar no keycloak - realm settings key
public_key = f"-----BEGIN PUBLIC KEY-----\n{raw_public_key}\n-----END PUBLIC KEY-----"
# Default keycloak audience: "account" - inspect jwt.io
decode = jwt.decode(token, public_key, algorithms=["RS256"], audience="account")
assert decode == {'exp': 1713143458,
 'iat': 1713143158,
 'jti': '39b2e01a-2959-451f-9304-96d9a43a5e6e',
 'iss': 'http://localhost:8080/realms/codeflix',
 'aud': 'account',
 'sub': '3d353aad-f331-416a-9bda-e3cf6329483e',
 'typ': 'Bearer',
 'azp': 'codeflix-admin-frontend',
 'session_state': 'a7d92b90-7a41-417d-8a7a-5c6b6bae8add',
 'acr': '1',
 'allowed-origins': ['/*'],
 'realm_access': {'roles': ['offline_access',
   'uma_authorization',
   'default-roles-codeflix']},
 'resource_access': {'account': {'roles': ['manage-account',
    'manage-account-links',
    'view-profile']}},
 'scope': 'profile email',
 'sid': 'a7d92b90-7a41-417d-8a7a-5c6b6bae8add',
 'email_verified': True,
 'name': 'Admin Admin',
 'preferred_username': 'admin',
 'given_name': 'Admin',
 'family_name': 'Admin',
 'email': 'admin@admin.com'}
```
