# Genvex Connect
This component integrates Genvex Connect and Nilan Gateway devices directly into Home Assistant.
It uses the [GenvexNabto](https://github.com/superrob/genvexnabto) library, which manages local communication with the devices. For more technical details about the project, refer to that repository.

To use this integration, an official gateway is required. This can be either a Genvex Connect gateway or a Nilan gateway. Newer Genvex Optima devices come with a built-in gateway on the mainboard and only require an Ethernet connection.

### Supported controller models
|Controller         | Gateway required     | Supported       | Tested  |
|------------------:|:---------------------:|:---------------:|:------:|
|Optima 250         | Yes, internet gateway | ✅              | ✅     |
|Optima 251         | Yes, internet gateway | ✅              | ✅     |
|Optima 260         | Yes, internet gateway | ✅              |        |
|Optima 270         | Built in              | ✅              | ✅     |
|Optima 301         | Yes, internet gateway | ✅              | ✅     |
|Optima 312         | Yes, internet gateway | ✅              | ✅     |
|Optima 314         | Built in              | ✅              |        |
|Nilan CTS400       | Yes, nilan gateway    | ✅              | ✅     |
|Nilan CTS602       | Yes, nilan gateway    | ✅              | ✅     |
|Nilan CTS602 Light | Yes, nilan gateway    | ✅              | ✅     |
|Nilan CTS602 Geo   | Yes, nilan gateway    | ✅              |        |

If you have one of the controllers not currently listed as tested, please report if the integration works as expected.

## Installation (HACS)

The preferred method to install is to use HACS. The repository is part of the default list.
Go to HACS -> Integrations, search for Genvex Connect and then install.
Restart your Home Assistant instance to complete installation.

## Installation (No HACS)

If you don't have/want HACS installed, you will need to manually install the integration

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. Drag the `custom_components` folder into your HA configuration folder.
3. Restart Home Assistant

## Setup
To setup the integration, go into "Configuration" -> "Integrations" and press on the "+" button. Find Genvex Connect from the list.
The integration should search for your device and let you choose which one to use. You then need to provide it with the same email as used in the Genvex Connect app. This is case sensitive. 
Then if all goes well, your device should be added and working in Home Assistant.

## A little note to Genvex/Nilan
I understand that you have the ability to remotely update your devices, and that closing local connections is straightforward. However, please use this power responsibly.
The local communication requires the email associated with the app as the password, making misuse highly unlikely. The capabilities are on par with, or even more limited than direct Modbus connections.
This should not be considered a security concern. It also enhances the value of your Gateway solutions for the end user.

# Obligatory statement
The contributors are not responsible for any damages resulting from the use of this integration. No warranty is provided.