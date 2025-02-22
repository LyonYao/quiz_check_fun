zip -r activity.zip lambda/activity/  common/
zip -r function2.zip function2/ .dependencies/function2/ common/

mkdir -p .dependencies/function1
cd function1
pip install -r requirements.txt -t ../.dependencies/function1
cd ..

mkdir -p .dependencies/function2
cd function2
pip install -r requirements.txt -t ../.dependencies/function2
cd ..


Compress-Archive -Path "lambda\activity", "lambda\comm","lambda\subject","lambda\checker" -DestinationPath "activity.zip"  

tar -czvf activity.zip -C lambda/activity . -C ../../common .

Compress-Archive -Path "dependencies\*"  -DestinationPath "layer.zip"  

python -m activity.app

# 创建一个临时目录用于存放Layer内容
mkdir layer && cd layer
mkdir python

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# 或者 Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install flask --target ./python

# 停用虚拟环境
deactivate

pip install flask-cors


FROM amazonlinux:2

# 安装pip
RUN yum -y update && \
    yum -y install python38 python38-pip zip && \
    pip3.8 install --upgrade pip

# 设置工作目录
WORKDIR /build

# 复制requirements.txt到容器中
COPY requirements.txt .

# 安装Python包
RUN pip3.8 install --target ./python -r requirements.txt

# 打包为zip文件
RUN cd python && zip -r ../layer.zip .

https://layers.market/?spm=5176.28103460.0.0.4d775d27nJWxKV

docker run -it python:3.11-slim /bin/bash
pip install psycopg2 --target ./python
docker run -it amazonlinux:2 /bin/bash
yum update -y && \
    yum install -y amazon-linux-extras && \
    amazon-linux-extras enable postgresql14 && \
    yum install -y postgresql-deve

docker run -it public.ecr.aws/lambda/python:3.11 /bin/bash

pip install psycopg2-binary==2.9.10 --target ./python
pip install pytz==2024.1 --target ./python




WITH deleted_a AS (
    DELETE FROM a WHERE updated_at < now() - interval '3 months' RETURNING id
)
DELETE FROM b WHERE a_id IN (SELECT id FROM deleted_a);
DELETE FROM c WHERE a_id IN (SELECT id FROM deleted_a);

CREATE OR REPLACE FUNCTION delete_stale_records()
RETURNS void AS $$
DECLARE
    r RECORD;
BEGIN
    -- 开始事务
    BEGIN;

    -- 循环遍历所有超过3个月未更新的记录
    FOR r IN 
        SELECT id FROM a WHERE updated_at < now() - interval '3 months'
    LOOP
        -- 删除关联表 c 中的记录
        DELETE FROM c WHERE a_id = r.id;
        
        -- 删除关联表 b 中的记录
        DELETE FROM b WHERE a_id = r.id;
        
        -- 删除主表 a 中的记录
        DELETE FROM a WHERE id = r.id;
    END LOOP;

    -- 提交事务
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        -- 如果出现任何错误，回滚事务
        ROLLBACK;
        RAISE;
END;
$$ LANGUAGE plpgsql;

SELECT cron.schedule('0 0 1 * *', 'SELECT delete_stale_records();');
CREATE EXTENSION pg_cron;