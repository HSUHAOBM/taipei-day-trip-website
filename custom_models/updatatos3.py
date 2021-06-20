import boto3, botocore 
import configparser
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from pypinyin import lazy_pinyin


config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

S3_KEY=config.get('main', 'S3_KEY')   
S3_SECRET=config.get('main', 'S3_SECRET')   

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e
    # return "{}{}".format("https://husanhaoawsbucket.s3.amazonaws.com/", file.filename)

    return "http://d3uk1zhmxdtlrt.cloudfront.net/" + file.filename


#檢查檔案格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) 
def allowed_file(filename):
    filename=filename.lower()
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file_to_s3_main(file):
    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        # 轉編碼
        # file.filename = secure_filename(''.join(lazy_pinyin(file.filename)))

        # print("圖片連結網址",str(output))
        # interimgsrc=output
        return str(upload_file_to_s3(file, "husanhaoawsbucket"))
    else:
        return "上傳失敗"