# Shipan configuration

/!\ *** The features described below are not yet implemented *** /!\


## Customization


### Layers

The configuration layers are loaded in the following order:

1. Default configuration (defines the minimum configuration required for the Shipan instance to be functional)
1. Custom configuration

   It is possible to overload and extend the default `SHIPAN.config` in several ways:
   1. via the `settings.py` file
   1. via the `settings_custom.py` file
   1. via the `settings` instance of the `Customization` model in the database

### Priority

1. The configuration defined in the `settings` database instance has priority over the configuration defined in the `settings_custom.py` file,
1. the configuration defined in the `settings_custom.py` file has priority over the configuration defined in the `settings.py` file,
1. the configuration defined in the `settings.py` file has priority over the configuration defined by default (hard-coded).

In summary:
```
database settings    >    settings_custom.py    >    settings.py    >    hard-coded
```


## Example

```
# settings.py
SHIPAN = {
    # ...
    'DATA': {
        'ROOT': {
            'FOLDER': '/data',
            'DISK_QUOTA': 64,               # mb
            'RETENTION_PERIOD': 90          # days
        },
        'BACKUP': {
            'FOLDER': '/data/backup',
            'DISK_QUOTA': 64,               # mb
            'RETENTION_PERIOD': 365         # days
        },
        # ...
    },
    # ...
}
```



## Shipan data


Some Shipan features produce files (such as `backup` which regularly exports live data to an isolated archive), in their dedicated folder.

For example:

* the `backup` feature exploits the `./data/backup` folder
* the `order` feature exploits the `./data/order` folder

### Customize data root config

To use a different folder as the root folder, use the `DATA/ROOT/FOLDER` option in the `SHIPAN` configuration of the settings file.
All the features will automatically use their dedicated folder directly under the defined root folder.

### Customize data config by feature

It is also possible to customize the folder of any feature by defining its `DATA/[FEATURE]/FOLDER` option in the `SHIPAN` configuration.



## Autonomous cleaning system

The autonomous cleaning system is enabled by default.

### Customize the autonomous cleaning system

However, it is possible to modify its behavior by configuring `DATA/*/DISK_QUOTA` and `DATA/*/RETENTION_PERIOD` in the `SHIPAN` configuration.
