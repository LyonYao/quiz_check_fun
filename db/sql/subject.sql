CREATE TABLE quiz.subject_summary (
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    activity_id VARCHAR(32) NOT NULL,
    title VARCHAR(255) NOT NULL, 
    status VARCHAR(1) NOT NULL, --values: 'D' for draft, 'V' for visible, 'H' for hidden,'C' for can check.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    updated_by VARCHAR(255)
);
GRANT SELECT ON quiz.subject_summary TO quiz_check_u;


CREATE TABLE quiz.subject_content (
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    subject_id VARCHAR(32) NOT NULL,
    content TEXT NOT NULL
);

GRANT SELECT ON quiz.subject_content TO quiz_check_u;

INSERT INTO quiz.subject_summary(
        id, activity_id, title, status, description, created_at, updated_at, created_by, updated_by)
    VALUES 
        ('000000002', '0001', '模块1: 云计算基础概念与演变历史', 'C', '什么是云计算？\n云计算的历史发展\n云计算的优势与挑战', now(), now(), 'system', 'system'),
        ('000000003', '0001', '模块2: AWS入门与核心服务概览', 'C', 'AWS简介\nAWS的核心服务概览（EC2, S3, RDS等）\n如何开始使用AWS', now(), now(), 'system', 'system'),
        ('000000004', '0001', '模块3: 安全、合规性与管理工具', 'C', '介绍AWS安全最佳实践（IAM, VPC安全组）,监控与日志管理（CloudWatch, CloudTrail）,成本监控工具', now(), now(), 'system', 'system'),
        ('000000005', '0001', '模块4: 计算服务', 'C', '第1课：Amazon EC2相关服务介绍，自动扩展组及负载均衡器\n第2课：Lambda无服务器计算及容器服务ECS与Kubernetes(EKS)', now(), now(), 'system', 'system'),
        ('000000006', '0001', '模块5: 数据存储与数据库解决方案', 'C', '第1课：数据存储基础（存储的重要性、不同类型的数据存储）\nAmazon S3,EBS,EFS\n第2课：数据库服务\nRDS支持的数据库引擎（MySQL, PostgreSQL, Oracle等）\nNoSQL数据库', now(), now(), 'system', 'system'),
        ('000000007', '0001', '模块6: 虚拟网络', 'C', '第1课：VPC及相关服务介绍\n第2课：Route 53 DNS服务与CloudFront', now(), now(), 'system', 'system');


INSERT INTO quiz.subject_content(
	id, subject_id, content)
	VALUES ('000000001', '000000002', ' 

<h2>什么是云计算？</h2>
<p>云计算是一种通过互联网提供计算资源和服务（如服务器、存储、数据库、网络、软件等）的技术模式。用户可以通过按需付费的方式使用这些资源，而无需购买和维护物理硬件或软件。</p>
<ul>
  <li><strong>服务模型：</strong> 包括基础设施即服务(IaaS)、平台即服务(PaaS)和软件即服务(SaaS)。
    <ul>
      <li><em>IaaS</em> 示例：Amazon EC2 提供虚拟服务器实例。</li>
      <li><em>PaaS</em> 示例：AWS Elastic Beanstalk 支持开发人员快速部署和管理应用程序，无需担心底层基础设施。</li>
      <li><em>SaaS</em> 示例：Amazon WorkSpaces 允许用户通过浏览器访问桌面应用,gitHub。</li>
    </ul>
  </li>
  <li><strong>部署模型：</strong> 可以是公有云、私有云、社区云或混合云。
    <ul>
      <li><em>公有云</em> 示例：阿里云为个人和企业提供公共可用的服务。</li>
      <li><em>私有云</em> 示例：企业内部数据中心专用于自身业务需求。</li>
      <li><em>社区云</em> 示例：政府机构间共享的安全云环境。</li>
      <li><em>混合云</em> 示例：公司利用公有云进行非敏感数据处理，同时在私有云上运行核心业务应用。</li>
    </ul>
  </li>
</ul>

<h2>云计算的历史发展</h2>
<p>云计算的概念可以追溯到20世纪60年代的大型机分时系统，但现代云计算的起源通常与2006年亚马逊推出其Elastic Compute Cloud (EC2)服务相关联。随着技术的进步和互联网带宽的增长，云计算逐渐成为主流，并且今天它已成为IT基础设施的重要组成部分。</p>
<ul>
  <li><strong>早期阶段（1960s-1990s）：</strong> 概念源于大型计算机时期的分时系统。</li>
  <li><strong>发展阶段（1990s-2000s）：</strong> 虚拟化技术的发展为云计算奠定了基础。</li>
  <li><strong>成熟阶段（2000s-至今）：</strong> Amazon Web Services (AWS) 的发布标志着现代云计算的开始；例如，AWS S3 和 EC2 的发布推动了云计算的广泛应用。</li>
</ul>

<h2>云计算的优势与挑战</h2>

<h3>优势</h3>
<ul>
  <li><strong>成本节约：</strong> 减少了购买硬件和维护的成本。
    <ul>
      <li>初创公司可以利用AWS免费层开始其业务，避免初期的大额投资。</li>
    </ul>
  </li>
  <li><strong>灵活性：</strong> 可以根据需要快速扩展或缩减资源。
    <ul>
      <li>电商网站可以在促销活动期间通过Auto Scaling快速增加服务器容量。</li>
    </ul>
  </li>
  <li><strong>可访问性：</strong> 可以通过互联网从任何地方访问应用和服务。
    <ul>
      <li>员工可以使用AWS WorkSpaces从家中远程访问公司的办公环境。</li>
    </ul>
  </li>
  <li><strong>灾难恢复：</strong> 提高了数据的安全性和恢复能力。
    <ul>
      <li>AWS Backup提供了简单且统一的备份解决方案，确保关键数据的安全。</li>
    </ul>
  </li>
  <li><strong>自动更新：</strong> 供应商负责软件和安全更新。
    <ul>
      <li>AWS Lambda允许您运行代码而无需考虑服务器管理，包括自动更新和补丁。</li>
    </ul>
  </li>
</ul>

<h3>挑战</h3>
<ul>
  <li><strong>安全性：</strong> 数据保护和隐私问题是对云服务的主要担忧之一。
    <ul>
      <li>AWS Identity and Access Management (IAM) 帮助控制谁可以访问您的资源，但这需要正确配置。</li>
    </ul>
  </li>
  <li><strong>可靠性：</strong> 尽管大多数提供商都有很高的服务水平协议(SLA)，但仍有可能出现停机。
    <ul>
      <li>2017年，Amazon S3 服务中断影响了大量依赖该服务的网站。</li>
    </ul>
  </li>
  <li><strong>兼容性：</strong> 将现有系统迁移到云端可能会遇到兼容性问题。
    <ul>
      <li>某些老旧的应用程序可能不完全支持在AWS上的直接迁移。</li>
    </ul>
  </li>
  <li><strong>供应商锁定：</strong> 一旦选择了特定的云供应商，迁移到另一个供应商可能会很复杂且成本高昂。
    <ul>
      <li>迁移数据和重新配置服务可能导致额外的时间和金钱投入，例如从AWS迁移到Azure。</li>
    </ul>
  </li>
</ul> ');