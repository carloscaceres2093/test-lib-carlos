import paramiko
import io
import logging
import boto3

def open_ftp_connection(sftp_host, sftp_user, sftp_pass):
    
    """
    Opens ftp connection.
        Parameters:
            ftp_host: SFTP host name
            ftp_user: SFTP user name
            ftp_pass: SFTP password
        Returns:
            SFTP Connection
    """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    try:
        transport = paramiko.Transport(sftp_host)
    except Exception as err:
        logging.error('Failed to connect FTP Server!')
        raise SystemExit(err)
    try:
        transport.connect(username=sftp_user, password=sftp_pass)
    except Exception as err:
        logging.error('Incorrect username or password!')
        raise SystemExit(err)
    ftp_connection = paramiko.SFTPClient.from_transport(transport)
    return ftp_connection


def transfer_sftp_2_s3(sftp_conn, s3_conn,  sftp_file_path, s3_file_path, bucket_name):
    """
    Transfer data from sftp to s3.
    :param ftp_file_path:
    :param ftp_file_path:
    :param ftp_file_path:
    :return: connection object.
    """
    """
    Opens ftp connection.
        Parameters:
            sftp_conn: SFTP Connection
            s3_conn: S3 Connection
            sftp_file_path: SFTP Path file
            s3_file_path: S3 Path file
            bucket_name: Destination bucket name
    """
    sftp_file = sftp_conn.file(sftp_file_path, "r")
    sftp_file_data = sftp_file.read()
    with io.BytesIO(sftp_file_data) as part:
        conf = boto3.s3.transfer.TransferConfig(
            multipart_threshold=10000, max_concurrency=4
        )
        s3_conn.upload_fileobj(part, bucket_name, s3_file_path, Config=conf)
        logging.info("SUCCEEDED_STREAM_FILE")
    sftp_file.close()
    logging.info("TRANSFER_COMPLETED_FROM_FTP_TO_S3")


def open_ssh_connection(ssh_host, ssh_user, ssh_pass, port=22):
    
    """
    Opens ftp connection.
        Parameters:
            ftp_host: SFTP host name
            ftp_user: SFTP user name
            ftp_pass: SFTP password
        Returns:
            SFTP Connection
            SSH Connection
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_host, port=port, username=ssh_user, password=ssh_pass)
        sftp_client = ssh_client.open_sftp()
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return sftp_client, ssh_client