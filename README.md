Blockstream AMP CLI

# What is Blockstream AMP?

AMP is a platform with a flexible API made by Blockstream aimed to issue and manage digital assets on the Liquid Network.

More details on https://blockstream.com/amp/

# How to install the Blockstream AMP CLI

```
pip install -r requirements.txt
python setup.py build
python setup.py install
```

# How to use the Blockstream AMP CLI

```
$ amp --help
usage: amp [-h] [--profile PROFILE] {assets,assignments,categories,distributions,users,gaids,managers,account} ...

Blockstream AMP CLI tool.

positional arguments:
  {assets,assignments,categories,distributions,users,gaids,managers,account}
                        sub-command help
    assets              Assets management.
    assignments         Assignments management.
    categories          Categories management.
    distributions       Distributions management.
    users               Users management.
    gaids               GAID management.
    managers            Managers management.
    account             Account management.

optional arguments:
  -h, --help            show this help message and exit
  --profile PROFILE     Profile name to load from ~/.amp/profiles
```

# Configuration

Create a file named `~/.amp/profiles` with the following content:
```
[default]
API_URL=https://amp.blockstream.com/api # You can replace that with the test URL if you need
BLOCKSTREAM_AMP_USERNAME= # Your Username
BLOCKSTREAM_AMP_PASSWORD= # Your Password
```

You can also create as many profile as you want by creating a new section named after your profile.

```
[default]
API_URL=https://amp.blockstream.com/api # You can replace that with the test URL if you need
BLOCKSTREAM_AMP_USERNAME= # Your Username
BLOCKSTREAM_AMP_PASSWORD= # Your Password

[production]
API_URL=https://amp.blockstream.com/api
BLOCKSTREAM_AMP_USERNAME= # Your Username
BLOCKSTREAM_AMP_PASSWORD= # Your Password
```

Then to use your `production` profile add the profile argument to the CLI calls like this: `amp --profile production ...`

# Missing features

- Remove category
- Asset activities
- Asset balance
- And some more...

Feel free to help us to improve the CLI by sending us a pull request on [Github](https://github.com/Exordium-Limited/blockstream-amp-cli).
