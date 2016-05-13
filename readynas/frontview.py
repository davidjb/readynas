import argparse
import sys
import os
import requests

def download_configuration(host='localhost',
                           user='admin',
			   password='netgear1',
			   output_dir='.',
			   filename=None,
                           shares=True,
			   services=True,
			   users_groups=True,
			   network=True,
                           misc=True,
			   data=False):
    """ Download the configuration from the given ReadyNAS.
    """
    params = {'OPERATION': 'set',
              'PAGE': 'System',
	      'command': 'ConfigBackupBackup',
	      'download_file_name': 'readynas.zip',
	      'everything': '',
	      'data': data and 'on' or '',
	      'misc': misc and 'on' or '',
              'network': network and 'on' or '',
              'services': services and 'on' or '',
	      'shares': shares and 'on' or '',
	      'user_group': users_groups and 'on' or ''}
    response = requests.get('https://{0}/get_handler'.format(host),
                            verify=False,
                            params=params,
			    auth=(user, password))
    if not filename:
        filename_header = response.headers.get('content-disposition')
        filename = filename_header and filename_header.split('filename=')[1] \
                       or 'readynas-backup.zip' 

    output_path = os.path.join(output_dir, filename)

    with open(output_path, 'wb') as output:
         output.write(response.content)
	 print 'Downloaded configuration as {0}'.format(output_path)
    return response


def download_configuration_main():
    parser = argparse.ArgumentParser(description="Download ReadyNAS configuration as backup")
    parser.add_argument('--host', '-i',
                        help="A host name or IP address for the device to connect to.",
                        default='localhost')
    parser.add_argument('--user', '-u',
                        help="Username to access device as administrator.",
                        default='admin')
    parser.add_argument('--password', '-p',
                        help="Password used to access the device's account.",
                        default='netgear1')
    parser.add_argument('--output-dir', '-d',
                        help="Directory to output downloaded configuration backup.",
			default=".")
    parser.add_argument('--filename', '-f',
                        help="Filename to output. The resulting file will be a zip, so consider appropriate naming. If not specified, this defaults the name provided by Frontview, as if you were downloading the file yourself manually.")

    args = parser.parse_args()
    download_configuration(**vars(args))
