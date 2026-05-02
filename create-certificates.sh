mkdir -p ./nginx/certs
cd ./nginx/certs

echo "*" > .gitignore

echo "Ensuring the local mkcert's CA is install in your trust store . . . "
mkcert -install

echo "Generating certificates . . . "
mkcert -cert-file test-site.crt -key-file test-site.key \
  example.com 127.0.0.1 ::1 localhost

echo "All done!"
