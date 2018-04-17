# Example

```

git clone https://github.com/RyanJarv/omaha-server.git

cd omaha-server
git submodule sync
git submodule update

./scripts/sign_and_upload.sh ~/path/to/app.dmg path/to/dsa_priv.pem
