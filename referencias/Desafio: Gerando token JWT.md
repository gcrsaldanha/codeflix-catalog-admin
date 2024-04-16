# Desafio Módulo 14: Gerando token JWT para Testes

- Para executar testes com permissão (sem mockar a `permission_classes`) nós precisamos gerar nosso próprio token JWT com o mesmo formato de payload do Keycloak:
```json
{
    "realm_access": {
        "roles": [
            "offline_access",
            "admin",
            "uma_authorization",
            "default-roles-codeflix"
        ]
    }
}
```
- Na documentação do PyJWT tem um exemplo de como gerar um token assinado: [Encoding & Decoding Tokens with RS256 (RSA)](https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-rs256-rsa)

```python
>>> import jwt
>>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
>>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."
>>> encoded = jwt.encode({"some": "payload"}, private_key, algorithm="RS256")
>>> print(encoded)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
>>> decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])
{'some': 'payload'}
```

- Você vai precisar de um par de chaves privada/pública para codificar/decodificar o token. Você pode gerá-la através de bibliotecas de criptografia (OpenSSL) ou utilizar o site [RSA Key Generator](https://cryptotools.net/rsagen)
- Lembre-se de salvar as chaves em **variáveis de ambiente**.
