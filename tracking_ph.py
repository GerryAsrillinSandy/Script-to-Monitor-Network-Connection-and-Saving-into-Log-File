from twilio.rest import Client

# Twilio Account SID and Auth Token
account_sid = 'AC58473d7acf785d8ba344ed65412ac04a'
auth_token = '6a5e2801031e2f7402b6b17db49d3a41'

# Create a Twilio client
client = Client(account_sid, auth_token)


def track_phone_location(phone_number):
    try:
        # Fetch the phone number information
        number_info = client.lookups.phone_numbers(
            phone_number).fetch(type='carrier')

        # Retrieve the carrier information
        carrier = number_info.carrier['name']

        # Retrieve the country and network type
        country = number_info.country_code
        network_type = number_info.carrier['type']

        # Print the location details
        print(f'Phone Number: {phone_number}')
        print(f'Carrier: {carrier}')
        print(f'Country: {country}')
        print(f'Network Type: {network_type}')

    except Exception as e:
        print(f'Error: {str(e)}')


# Enter the phone number you want to track
phone_number = input('Enter the phone number to track: ')

# Track the phone location
track_phone_location(phone_number)
