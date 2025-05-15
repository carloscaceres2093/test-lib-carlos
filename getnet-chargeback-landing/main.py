import os
#import boto3
from stat import S_ISDIR, S_ISREG
from datetime import timedelta, datetime
#import json
import yaml
import logging.config
from yuno_data_lib import open_ftp_connection_by_private_key

# AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
# AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
# AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
# ORGCODE = os.getenv("ORGANIZATION_CODE")
# CONNECTION_ID = os.getenv("CONNECTION_ID")
# DS_DATE = os.getenv("DS_DATE")
DS_DATE_TIME = datetime.strptime('2025-04-29', "%Y-%m-%d")
DAYS_BACK = 1#int(os.getenv("DAYS_BACK"))
# LANDING_BUCKET_NAME = os.getenv("LANDING_BUCKET_NAME")
# SFTP_HOST = os.getenv("FTP_HOST")
# SFTP_USERNAME = os.getenv("FTP_USERNAME")
# SFTP_PASSWORD = os.getenv("FTP_PASSWORD")
# SFTP_PATH = os.getenv("FTP_PATH")
# PROVIDER = os.getenv("PROVIDER")
# COUNTRY = os.getenv("COUNTRY")
SFTP_PATH="/"
SFTP_HOST =  "sftp.globalgetnet.com",
SFTP_USERNAME="ant_group"
SFTP_PORT = 9525
SFTP_KEY="""-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA3cAlpuqpJv4ujArJKeENyUlivEbI0Mld/EfJHWyUSG+Szle/
Xs1eNNpIm624wkdsbUVKqI9SzFYa9bZwX1nyhawTg7obvD/rSdHDY4P5EXTJRjIg
gbDHew93kjPIQ1Ww9n1NLj6+rPZ6S7PwN5AkiYdRV15Ni7eHlHXxRuAFUuk/8YvE
103XMFYbydJi2H3HEk+uBY3pHcGeScRijCQDwPwKKxFGffYvXKB1TSf5HKYk3uxx
KY6+xbNXOCB3z0IcipoBemMe4DlKljzUz3LrQxyHPiydj52lnJE7w3ZIVStf35Mw
XqNkvCYYzQwfXFutNbmQ+oIFtwMyU+r8xm2BMQIDAQABAoIBAEA1ArHyAEhqENA7
z0NxBqzhstURKdRKegwyPOloJwdSRw+4GJE6paxoB94LzxNx2tNI3PUxiqffxq6e
xKrXQIGz8XKS0LURTO9y7UBDVjrXte+9U+w5Y4keUWDj3XihtzunzFE3mb47H+4L
i+KKugmYRNUnWQy7d2ZlQBdlhiUbGo4wkPzdfIjlcnrUFFYMc4wn0+gnpXBbh27G
/JTWpw3vx3Qa88jyByult6cGD/zk/k7Ho2KW38MDzbUeqIU5qLJ95381f+nD8+SC
ajiSe8tNS6uwQWo1+Bq0nQrWhM76vWqxU1M7eVdQFhNNZyWRjbrCPb2ykw1yJq2J
Vr6wrIECgYEA710wBbgK+bHeCpIwWCdjcHWTDn5CSFEnGhO2N0jaM5VyzcNFEK1Y
XooDrVYRD5aFqSDYR8QQT+vicfOyEL5hfKrZhp6+mM7DppNO9YH+2bS+cRwJjqon
JCb9AACLiAscDo3JhI7AdSTy8w258PX9+/0j+DAXnasqoeViI+Aw1McCgYEA7SmT
4Qujp+BwW+Xz3Fzo/qUAZlP7lGNBQ7+S+vfpmUgm82UszidPdcPCufqS7qobXh6z
NxKvLwqM5H/W6BfBWqM5cBq2PEHCFW9q3hM3yX3XFcvZ7G9K31h7vNkaBwOyxBRJ
e2ZZ6pakErTpyLGUsJ+LxNNC5T1r72kjVtkvkkcCgYBp06p6rM71bGU+CTokj22Q
d/sHal0FuhNunQ5vzN7j9YwnWtD7OZibW6uahDXQzXzUtLfKqu2HWEPqm5K7gmB5
jNPVh/O+fZPU3sYHF21EdXvJaFr1X1ckzbQHvzXxdO/3o0pYOADxCd/8A7KUzT14
noe7oA+g3t9fapoEQId2WwKBgDPAd+mK3ap7emlDU6SJjbpLjTvHJcXqpso+2rbz
NEFjkkRYlp9hyqAbGLn2qOt1qUUvk9H3vMyaE8ak8uNwk5vQtG73FT8u5khBKOPO
88R/NlkmQ6apXoBAUbgS8/AF6ZOKDcLkwchEGQeP/NfzkEu+dQR9SUK21X/HxJNm
D1BvAoGABMy3WwLRyk6SZfmQv00MmCc0EJNYDx38EcynX1RTHUv1aIfTbABAveEJ
fKUWmxE7AoEYrR0eRuCV8zDd6KKRz7ZosBE4D8KwpX9AxGFAF7iqfQ9WL9Wchl+s
JFAXvFo63maZbm4eCKGp53zzg1MwVqrrrI919XA3dflODn2vrqA=
-----END RSA PRIVATE KEY-----"""

# def s3_connection():
#     """
#     Opens s3 connection.
#     :return: connection object.
#     """
#     return boto3.client(
#         "s3",
#         aws_access_key_id=AWS_ACCESS_KEY,
#         aws_secret_access_key=AWS_SECRET_KEY,
#         region_name=AWS_REGION_NAME,
#     )


def listdir_r(ftp_connection, days_back, path=SFTP_PATH):
    """
    Check new files into SFTP with metadata last_modified
    :param ftp_connection: SFTP connection object
    :param days_back: Número de días a considerar
    :param path: Directorio base en el SFTP
    """
    if not path.startswith(SFTP_PATH):
        path = f"{SFTP_PATH}/{path}".replace("//", "/")

    days_back = int(days_back)

    start_timestamp = DS_DATE_TIME.timestamp()
    end_timestamp = (DS_DATE_TIME + timedelta(days=days_back)).timestamp()

    try:
        for entry in ftp_connection.listdir_attr(path):
            remotepath = f"{path}/{entry.filename}".replace("//", "/")
            mode = entry.st_mode

            if S_ISDIR(mode):
                try:
                    ftp_connection.listdir_attr(remotepath)
                    listdir_r(ftp_connection, days_back, remotepath)
                except FileNotFoundError:
                    print(f"⚠️  Directorio no encontrado: {remotepath}, saltando...")
                except PermissionError:
                    print(
                        f"⚠️  No tienes permisos para acceder a: {remotepath}, saltando..."
                    )
            elif S_ISREG(mode):
                file_date_utc = datetime.utcfromtimestamp(entry.st_mtime)
                print(f"File: {entry.filename}, Date: {file_date_utc} UTC")

                if start_timestamp <= entry.st_mtime < end_timestamp:
                    print(f"✅ Archivo dentro del rango: {entry.filename}")
                    files_list.append(remotepath)
    except FileNotFoundError:
        print(f"❌ Error: Directorio no encontrado en SFTP: {path}")
    except PermissionError:
        print(f"❌ Error: No tienes permisos para acceder a {path}")


# def transfer_file_from_ftp_to_s3(sftp_file_path, sftp_connection, s3_connection):
#     """
#     Check if new files in sftp dont exists in s3, if not chunk the file and streaming from ftp to s3 on the fly
#     :param ftp_file_path:
#     :return:
#     """
#     ftp_file_name = sftp_file_path.split("/")[-1]

#     s3_file_path_prefix = f"settlement/organization_code={ORGCODE}/partner={PROVIDER}/connection_id={CONNECTION_ID}/country={COUNTRY}/date={DS_DATE}/audit_date={DS_DATE}/"
#     s3_file_path = s3_file_path_prefix + ftp_file_name
#     logger.info(f"START_COPY_FTP_FILE_{sftp_file_path}_TO_S3{s3_file_path}")
#     if s3_file_path_prefix not in xcom_data_dict:
#         xcom_data_dict[s3_file_path_prefix] = [ftp_file_name]
#     else:
#         xcom_data_dict[s3_file_path_prefix].append(ftp_file_name)
#     transfer_sftp_2_s3(
#         sftp_connection,
#         s3_connection,
#         sftp_file_path,
#         s3_file_path,
#         LANDING_BUCKET_NAME,
#     )


if __name__ == "__main__":
    with open("tasks/config/logging.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logging.getLogger("paramiko.transport").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)
    sftp_conn = open_ftp_connection_by_private_key(SFTP_HOST, SFTP_USERNAME, SFTP_KEY, SFTP_PORT)
    xcom_data_dict = {}
    files_list = []
    listdir_r(sftp_conn, DAYS_BACK)
    print(f"Files to transfer: {files_list}")
    # for i in files_list:
    #     transfer_file_from_ftp_to_s3(i, sftp_conn, s3_connection())
    # logger.info("COMPLETED_PROCESS")
    # with open("/airflow/xcom/return.json", "w") as outfile:
    #     json.dump(xcom_data_dict, outfile)
