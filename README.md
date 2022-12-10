# Dj's [Little Snitch](https://www.obdev.at/products/littlesnitch/index.html) rules collection

For rules for an application, have a look in the [apps](apps) directory, and see if anything strikes your fancy. Then, subscribe to the feed with the following URL:

`https://raw.githubusercontent.com/djpadz/lsrules/main/apps/<appname>.lsrules`

Where `<appname>` is the name of the application.

For example, to subscribe to the rules for Microsoft Office, subscribe to:

`https://raw.githubusercontent.com/djpadz/lsrules/main/apps/microsoft-office.lsrules`

For rules for a country, subscribe to a rule of the form:

`https://raw.githubusercontent.com/djpadz/lsrules/main/by-country/<cc>-<action>.lsrules`

where `<cc>` is the [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code and `<action>` is one of:
* `allow` - allow all traffic to the country
* `block` - block all traffic to the country
* `ask` - ask before allowing traffic to the country

For example, to block all traffic to Zimbabwe, subscribe to:

`https://raw.githubusercontent.com/djpadz/lsrules/main/by-country/zw-deny.lsrules`
