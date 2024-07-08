import paramiko
import io
import logging

def open_ftp_connection(ftp_host, ftp_user, ftp_key):
    """
    Opens ftp connection and returns connection object.
    """
    pkey = paramiko.RSAKey.from_private_key(io.StringIO(ftp_key))
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    try:
        transport = paramiko.Transport(ftp_host)
    except Exception as err:
        logging.error("Failed to connect FTP Server!")
        raise SystemExit(err)
    try:
        transport.connect(username=ftp_user, pkey=pkey)
    except Exception as err:
        logging.error("Incorrect username or password!")
        raise SystemExit(err)
    try:
        ftp_connection = paramiko.SFTPClient.from_transport(transport)
    except Exception:
        logging.error("SFTP connection error!")
    return ftp_connection