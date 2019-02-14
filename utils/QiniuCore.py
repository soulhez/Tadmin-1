'''七牛云组件'''

from qiniu import Auth,put_file

access_key='iRiXjQYnn5FIlXjyXXT8Vld64Sv9dDjIc9eLr7fB'
secret_key='ogdt7kQAyCb7xKEH953q5P6UCUUt6YSvROWUEopz'
bucket_name='public'
domian_url='http://phv6x08jc.bkt.clouddn.com/'
q = Auth(access_key, secret_key)
token = q.upload_token(bucket_name)
