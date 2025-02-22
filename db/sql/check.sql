CREATE TABLE quiz.check_question (
    id VARCHAR(32) NOT NULL PRIMARY KEY, 
    content TEXT NOT NULL,
    options VARCHAR(1000) NOT NULL, --- split with \; formtat： ’A:选项1\;B:选项2\;C:选项3\;D:选项4’
    answer VARCHAR(20) NOT NULL, ---split with \; format: 'A\;B'
    type VARCHAR(1) NOT NULL --values: 'S' for single choice, 'M' for multiple choice
);

GRANT SELECT ON quiz.check_question TO quiz_check_u;

INSERT INTO quiz.check_question (id, content, options, answer, type) VALUES
('1', '<h4>什么是云计算？<h4>A:一种通过互联网提供计算资源和服务的技术模式。<br/>B:仅指软件即服务(SaaS)。<br/>C:仅限于存储解决方案。<br/>D:以上都不正确。<br/>', 'A:A\;B:B\;C:C\;D:D', 'A', 'S'),
('2', '<h4>云计算的哪个模型允许用户通过互联网访问应用程序？<h4>A:IaaS<br/>B:PaaS<br/>C:SaaS<br/>D:DaaS<br/>', 'A:A\;B:B\;C:C\;D:D', 'C', 'S'),
('3', '<h4>云计算的历史发展可以追溯到哪个年代？<h4>A:1950s<br/>B:1960s<br/>C:1970s<br/>D:1980s<br/>', 'A:A\;B:B\;C:C\;D:D', 'B', 'S'),
('4', '<h4>哪一年亚马逊推出了Elastic Compute Cloud (EC2)？<h4>A:2004<br/>B:2006<br/>C:2008<br/>D:2010<br/>', 'A:A\;B:B\;C:C\;D:D', 'B', 'S'),
('5', '<h4>云计算中哪种部署模型适用于特定行业或组织间共享？<h4>A:公有云<br/>B:私有云<br/>C:社区云<br/>D:混合云<br/>', 'A:A\;B:B\;C:C\;D:D', 'C', 'S'),
('6', '<h4>下列哪些是云计算的服务模型？<h4>A:IaaS<br/>B:PaaS<br/>C:SaaS<br/>D:DaaS<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B\;C', 'M'),
('7', '<h4>以下哪些公司是早期推动现代云计算发展的主要参与者？<h4>A:Amazon<br/>B:Google<br/>C:Microsoft<br/>D:IBM<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B\;C', 'M'),
('8', '<h4>云计算的主要优势包括哪些？<h4>A:成本节约<br/>B:灵活性<br/>C:可访问性<br/>D:安全性<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B\;C', 'M'),
('9', '<h4>AWS全球基础设施由什么组成？<h4>A:数据中心<br/>B:边缘位置<br/>C:区域(Regions)<br/>D:以上全部<br/>', 'A:A\;B:B\;C:C\;D:D', 'D', 'S'),
('10', '<h4>Amazon EC2属于哪种云计算服务模型？<h4>A:IaaS<br/>B:PaaS<br/>C:SaaS<br/>D:DaaS<br/>', 'A:A\;B:B\;C:C\;D:D', 'A', 'S'),
('11', '<h4>以下哪个不是AWS的核心服务？<h4>A:Amazon S3<br/>B:Amazon RDS<br/>C:Amazon DynamoDB<br/>D:Azure Blob Storage<br/>', 'A:A\;B:B\;C:C\;D:D', 'D', 'S'),
('12', '<h4>在AWS上启动一个实例时，你需要选择什么？<h4>A:AMI (Amazon Machine Image)<br/>B:EBS (Elastic Block Store)<br/>C:VPC (Virtual Private Cloud)<br/>D:SNS (Simple Notification Service)<br/>', 'A:A\;B:B\;C:C\;D:D', 'A', 'S'),
('13', '<h4>Amazon S3主要用于什么？<h4>A:存储对象数据<br/>B:运行虚拟机<br/>C:提供数据库服务<br/>D:发送电子邮件<br/>', 'A:A\;B:B\;C:C\;D:D', 'A', 'S'),
('14', '<h4>以下哪些是AWS提供的PaaS服务？<h4>A:AWS Elastic Beanstalk<br/>B:AWS Lambda<br/>C:Amazon S3<br/>D:Amazon RDS<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B', 'M'),
('15', '<h4>以下哪些服务可以帮助您在AWS上构建高可用的应用程序？<h4>A:Auto Scaling<br/>B:Elastic Load Balancing<br/>C:Amazon Route 53<br/>D:Amazon SES<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B\;C', 'M'),
('16', '<h4>使用AWS Direct Connect的好处有哪些？<h4>A:更稳定的连接<br/>B:更低的延迟<br/>C:更高的安全性<br/>D:更快的数据传输速度<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B\;C\;D', 'M'),
('17', '<h4>以下哪些是AWS的安全管理工具？<h4>A:IAM (Identity and Access Management)<br/>B:VPC (Virtual Private Cloud)<br/>C:KMS (Key Management Service)<br/>D:S3<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B\;C', 'M'),
('18', '<h4>在AWS中，如何确保不同账户之间的资源隔离？<h4>A:使用IAM角色<br/>B:使用VPC<br/>C:使用S3桶策略<br/>D:使用CloudFormation模板<br/>', 'A:A\;B:B\;C:C\;D:D', 'B', 'S'),
('19', '<h4>以下哪些服务支持AWS上的无服务器架构？<h4>A:AWS Lambda<br/>B:AWS Fargate<br/>C:Amazon ECS<br/>D:Amazon S3<br/>', 'A:A\;B:B\;C:C\;D:D', 'A\;B', 'M'),
('20', '<h4>在AWS中，用于管理和跟踪费用及使用情况的工具是什么？<h4>A:CloudWatch<br/>B:CloudTrail<br/>C:Cost Explorer<br/>D:Trusted Advisor<br/>', 'A:A\;B:B\;C:C\;D:D', 'C', 'S');


CREATE TABLE quiz.check_refer (
    ref_id VARCHAR(32) NOT NULL  ,
    question_id VARCHAR(32) NOT NULL, 
    type VARCHAR(10) NOT NULL
);

GRANT SELECT ON quiz.check_refer TO quiz_check_u;
INSERT INTO quiz.check_refer (ref_id, question_id, type) VALUES
('000000003', '1', 'SUBECT'),
('000000003', '2', 'SUBECT'),
('000000003', '3', 'SUBECT'),
('000000003', '4', 'SUBECT'),
('000000003', '5', 'SUBECT'),
('000000003', '6', 'SUBECT'),
('000000003', '7', 'SUBECT'),
('000000003', '8', 'SUBECT'),
('000000003', '9', 'SUBECT'),
('000000003', '10', 'SUBECT'),
('000000003', '11', 'SUBECT'),
('000000003', '12', 'SUBECT'),
('000000003', '13', 'SUBECT'),
('000000003', '14', 'SUBECT'),
('000000003', '15', 'SUBECT'),
('000000003', '16', 'SUBECT'),
('000000003', '17', 'SUBECT'),
('000000003', '18', 'SUBECT'),
('000000003', '19', 'SUBECT'),
('000000003', '20', 'SUBECT');

drop table if exists quiz.check_record;
CREATE TABLE quiz.check_record (
    id VARCHAR(32) NOT NULL PRIMARY KEY, 
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10) NOT NULL , 
    ref_id VARCHAR(32) NOT NULL  ,
    activity_id VARCHAR(32) NOT NULL,
    reg_code VARCHAR(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(1) NOT NULL, --values: 'N' for not completed, 'C' for completed
    score INT,
    current_answer_idx INT DEFAULT 0,
    question_count INT DEFAULT 0
);

GRANT SELECT,INSERT,UPDATE ON quiz.check_record TO quiz_check_u;

drop table if exists quiz.check_answer;

CREATE TABLE quiz.check_answer (
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    question_id VARCHAR(32) ,
    record_id VARCHAR(32) NOT NULL,
    content TEXT NOT NULL,
    options VARCHAR(300) NOT NULL, --- split with ; formtat： ’A:选项1;B:选项2;C:选项3;D:选项4’
    answer VARCHAR(20) NOT NULL, ---split with ; format: 'A;B'
    result VARCHAR(20) , ---split with ; format: 'A;B'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(1) NOT NULL --values: 'S' for single choice, 'M' for multiple choice
);

GRANT SELECT,INSERT,UPDATE  ON quiz.check_answer TO quiz_check_u;