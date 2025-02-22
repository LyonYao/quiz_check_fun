

-- 创建数据库
CREATE DATABASE quiz_check;



-- 更改数据库所有者
ALTER DATABASE quiz_check OWNER TO quiz_check;

create schema quiz;
GRANT USAGE ON SCHEMA quiz TO quiz_check_u;