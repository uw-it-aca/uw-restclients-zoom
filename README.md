# REST client for Zoom

Installation:

    pip install UW-RestClients-Zoom

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_ZOOM_DAO_CLASS='Live'

    # Paths to UWCA cert and key files
    RESTCLIENTS_ZOOM_CERT_FILE='/path/to/cert'
    RESTCLIENTS_ZOOM_KEY_FILE='/path/to/key'

    # Zoom REST API hostname (eval or production)
    RESTCLIENTS_ZOOM_HOST='https://zoom.com'

Optional settings:

    # Customizable parameters for urllib3
    RESTCLIENTS_ZOOM_TIMEOUT=5
    RESTCLIENTS_ZOOM_POOL_SIZE=10

See examples for usage.  Pull requests welcome.
