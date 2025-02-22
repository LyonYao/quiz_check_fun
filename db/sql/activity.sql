CREATE TABLE quiz.activity_summary (
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    fee VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    updated_by VARCHAR(255),
    visible VARCHAR(1) DEFAULT 'Y',
    can_check VARCHAR(1) DEFAULT 'N',
    can_preview_q  VARCHAR(1) DEFAULT 'N',
    can_reg VARCHAR(1) DEFAULT 'Y',
    question_count INT DEFAULT 10
);
GRANT SELECT ON quiz.activity_summary TO quiz_check_u;

INSERT INTO quiz.activity_summary (id, name, start_time, end_time, status, location, description, fee, created_by, updated_by)
VALUES
    ('0001', '2025 AWS Share', '2025-03-15T09:00:00Z', '2025-03-15T17:00:00Z', '即将开始', '线上活动 - AWS 平台', '深入探讨AWS最新技术和服务，为开发者提供实战技巧。', '免费', 'system', 'system'),
    ('0002', '2024 数据科学研讨会', '2024-04-22T10:00:00Z', '2024-04-22T18:00:00Z', '报名中', '北京市朝阳区某会议中心', '聚焦数据科学前沿话题，与业内专家面对面交流。', '¥200', 'system', 'system'),
    ('0003', '2024 AI 开发者大会1', '2024-06-10T08:30:00Z', '2024-06-12T17:00:00Z', '已满员', '线上活动 - Zoom', '涵盖AI开发的所有方面，从理论到实践，全面覆盖。', '¥500', 'system', 'system'),
    ('0004', '2024 AI 开发者大会2', '2024-06-10T08:30:00Z', '2024-06-12T17:00:00Z', '已满员', '线上活动 - Zoom', '涵盖AI开发的所有方面，从理论到实践，全面覆盖。', '¥500', 'system', 'system'),
    ('0005', '2024 AI 开发者大会3', '2024-06-10T08:30:00Z', '2024-06-12T17:00:00Z', '已满员', '线上活动 - Zoom', '涵盖AI开发的所有方面，从理论到实践，全面覆盖。', '¥500', 'system', 'system'),
    ('0006', '2024 AI 开发者大会4', '2024-06-10T08:30:00Z', '2024-06-12T17:00:00Z', '已满员', '线上活动 - Zoom', '涵盖AI开发的所有方面，从理论到实践，全面覆盖。', '¥500', 'system', 'system');


CREATE TABLE quiz.activity_content (
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    activity_id VARCHAR(32) NOT NULL,
    content TEXT NOT NULL
);
INSERT INTO quiz.activity_content (id, activity_id, content)VALUES
    ('0001', '0001', '<h3>课程系列总览</h3>
<ul>
<li><strong>模块1</strong>: 云计算基础概念与演变历史</li>
<li><strong>模块2</strong>: AWS入门与核心服务概览</li>
<li><strong>模块3</strong>: 计算服务深入探讨</li>
<li><strong>模块4</strong>: 数据存储与数据库解决方案</li>
<li><strong>模块5</strong>: 网络配置与优化策略</li>
<li><strong>模块6</strong>: 虚拟化技术及容器化服务</li>
<li><strong>模块7</strong>: 安全、合规性与管理工具</li>
</ul>

<h4>模块1: 云计算基础概念与演变历史</h4>
<ul>
<li>第1课：什么是云计算？（定义、模型、部署方式）</li>
<li>第2课：云计算的历史发展（从网格计算到现代云）</li>
<li>第3课：云计算的优势与挑战</li>
</ul>

<h4>模块2: AWS入门与核心服务概览</h4>
<ul>
<li>第1课：AWS简介（公司背景、全球基础设施）</li>
<li>第2课：AWS的核心服务概览（EC2, S3, RDS等）</li>
<li>第3课：如何开始使用AWS（账户设置、免费层介绍）</li>
</ul>

<h4>模块3: 计算服务深入探讨</h4>
<ul>
<li>第1课：Amazon EC2详解（实例类型、启动模板）</li>
<li>第2课：自动扩展组与负载均衡器</li>
<li>第3课：Lambda无服务器计算介绍</li>
</ul>

<h4>模块4: 数据存储与数据库解决方案</h4>
<ul>
<li><strong>第1课</strong>：数据存储基础（存储的重要性、不同类型的数据存储）
<ul>
<li>Amazon S3深度解析（存储类、版本控制）</li>
<li>EBS (Elastic Block Store) 使用案例</li>
</ul>
</li>
<li><strong>第2课</strong>：数据库基础与关系型数据库服务RDS入门
<ul>
<li>RDS支持的数据库引擎（MySQL, PostgreSQL, Oracle等）</li>
<li>数据库备份与恢复策略</li>
</ul>
</li>
<li><strong>第3课</strong>：NoSQL数据库DynamoDB及其应用场景
<ul>
<li>DynamoDB的特点与优势</li>
<li>数据迁移服务与Glacier归档存储介绍</li>
</ul>
</li>
<li><strong>第4课</strong>：高级存储选项与最佳实践
<ul>
<li>备份与灾难恢复策略</li>
<li>使用S3进行静态网站托管</li>
</ul>
</li>
</ul>

<h4>模块5: 网络配置与优化策略</h4>
<ul>
<li>第1课：VPC设计原则与最佳实践</li>
<li>第2课：Route 53 DNS服务与流量管理</li>
<li>第3课：CloudFront CDN加速网站访问</li>
</ul>

<h4>模块6: 虚拟化技术及容器化服务</h4>
<ul>
<li>第1课：虚拟化基础与AWS上的实现</li>
<li>第2课：容器服务ECS与Kubernetes(EKS)</li>
<li>第3课：微服务架构与容器编排</li>
</ul>

<h4>模块7: 安全、合规性与管理工具</h4>
<ul>
<li>第1课：AWS安全最佳实践（IAM, VPC安全组）</li>
<li>第2课：监控与日志管理（CloudWatch, CloudTrail）</li>
<li>第3课：成本管理与优化技巧</li>
</ul>');

GRANT SELECT ON quiz.activity_content TO quiz_check_u;

CREATE TABLE quiz.activity_reg (
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    activity_id VARCHAR(32) NOT NULL,
    reg_name VARCHAR(20) NOT NULL,
    reg_code VARCHAR(32) NOT NULL,
    reg_time timestamp without time zone NOT NULL DEFAULT now()
);
ALTER TABLE IF EXISTS quiz.activity_reg
    ADD CONSTRAINT unique_code UNIQUE (reg_code);

GRANT SELECT,INSERT ON quiz.activity_reg TO quiz_check_u;

