### This will be archived soon, see https://github.com/brave/omaha-server-build/issues/1

# Example

```

git clone https://github.com/RyanJarv/omaha-server.git

cd omaha-server
git submodule sync
git submodule update

# This will start omaha-server in docker, sign and upload the dmg to it
./scripts/test.sh ~/path/to/app.dmg path/to/dsa_priv.pem

# Should be able to test the update with the url http://localhost:9090/sparkle/test/stable/appcast.xml
