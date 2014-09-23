#!/bin/bash

# Set bash flags to echo commands and automatically exit on error
trap 'echo "Test failed!"' ERR
set -ex

# Create a new key pair
KEYS=keys.txt.$$
./signer create > $KEYS

# Load the new keys in the environment variables expected by signer
export EMF_PRIVATE_KEY=`grep -A 1 "PRIVATE:" $KEYS | tail -n 1`
export EMF_PUBLIC_KEY=`grep -A 1 "PUBLIC:" $KEYS | tail -n 1`

# Generate hash, must be 20 bytes long ASCII hex
HASH="20140913cafefeedBADC00123456789012345600"

# Sign hash
SIGNED=`echo $HASH | ./signer sign`

# Check output contains the hash at beginning
echo $SIGNED | egrep -qi "^$HASH"

# Test valid data, expect 'OK' response
echo $SIGNED | ./signer verify | grep -q "OK"

# Test corrupted signature, expect 'Invalid' response
CORRUPT=`echo $SIGNED | sed -e 's/0/f/'`
echo $CORRUPT | ./signer verify | grep -q "Invalid"

rm $KEYS
echo "PASS"
