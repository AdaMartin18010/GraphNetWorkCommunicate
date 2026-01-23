# YANG网络管理知识图谱专题

Knowledge Graphs for YANG-based Network Management Topic 2024-2025

## 📊 **概述 / Overview**

**文档版本**: v1.0  
**创建时间**: 2025年1月  
**最后更新**: 2025年1月  
**状态**: ✅ 完成  
**质量等级**: ⭐⭐⭐⭐⭐ 五星级  
**国际对标**: ✅ IETF标准对齐

本文档基于IETF Internet-Draft `draft-marcas-nmop-knowledge-graph-yang-05`（2024年10月），详细阐述知识图谱在YANG网络管理中的应用，解决YANG数据模型的异构性问题，实现网络数据的语义集成和智能分析。

---

## 🎯 **一、引言 / Introduction**

### 1.1 背景

网络规模和复杂性的持续增长，推动着自主网络的发展。这需要结合网络遥测机制，从传统协议（如SNMP）到基于YANG语言的模型驱动遥测（MDT）和网络管理协议（如NETCONF、RESTCONF、gNMI）。

MDT特别受到网络行业的关注，因为它能够使用YANG等正式数据建模语言对网络的配置和状态数据进行建模。然而，自YANG诞生以来，网络行业经历了YANG数据模型的大规模创建，这些模型由供应商、标准开发组织（如IETF）和联盟（如OpenConfig）开发。

### 1.2 问题陈述

#### 1.2.1 YANG数据模型的异构性

**挑战**:
- YANG数据模型针对网络的不同抽象层（网络元素层和网络服务层）
- YANG数据模型可能增强（或偏离）其他模型，根据实现定义新功能
- 结果：大量独立的YANG数据模型，形成数据孤岛

**示例**:
- IETF `ietf-interface` [RFC8343] 和 OpenConfig `openconfig-interfaces` 遵循不同的结构和语法，但都引用相同的"接口"概念
- 不同的YANG模型以不同方式引用相同概念

#### 1.2.2 语义关系的隐式表示

**问题**:
- YANG模型通过标识符传达语义关系
- 例如，Service Assurance [RFC9418] 中的子服务增强，其中叶子"device"暗示"subservice"概念与"device"概念之间的关系
- 这种关系是隐式的，难以自动提取和利用

**YANG树示例**:
```
module: ietf-service-assurance-device

 augment /sain:subservices/sain:subservice/sain:parameter:
 +--rw parameters
 +--rw device string
```

### 1.3 知识图谱解决方案

**核心价值**:
- 从YANG模型中提取隐藏知识，实现概念级别的数据孤岛集成
- 独立于物理实现（YANG模式、语法、编码格式）
- 将YANG数据转换为图结构，将关系作为图中的一等公民表示
- 基于本体中的共同概念（如"device"）链接数据孤岛

---

## 📚 **二、知识图谱基础 / Knowledge Graph Fundamentals**

### 2.1 什么是知识图谱？

**定义**:
知识图谱包含事实集合以及我们对它们的了解，并以图结构表示。知识图谱使数据能够被上下文化理解，因为数据（如个体、实例）与数据本身的含义（如概念、知识）一起传播。

**示例**:
- 知识图谱可能包含关于接口"eth0"的数据
- 同时包含：接口可以是物理的或虚拟的，属于网络设备，具有名称、描述和MTU

### 2.2 本体（Ontology）的作用

**定义**:
本体是对特定领域中概念化的显式表示。本体可以被视为遵循形式逻辑的概念模型表示，允许机器理解和推理。

**关系**:
- 概念模型（信息模型）可能根据数据源技术转换为不同的数据模型 [RFC3444]
- 通过将数据模型（物理层）与本体中表示的概念（概念层）映射，可以找到网络中引用共同概念（如"interface"或"device"）的异构数据集

### 2.3 关键图标准

#### 2.3.1 RDF（资源描述框架）

**特点**:
- W3C语义网的标准图数据模型
- 成熟度高，大多数知识图谱实现依赖RDF标准
- 相关标准：RDF Schema (RDFS)、Web Ontology Language (OWL)、Shapes Constraint Language (SHACL)、SPARQL

#### 2.3.2 LPG（标记属性图）

**特点**:
- Neo4j等图数据库的成功证明了LPG作为知识图谱实现的替代方案
- W3C RDF-Star工作组正在研究RDF的演进，以促进关于语句的语句表示

#### 2.3.3 NGSI-LD标准

**定义**:
ETSI ISG CIM定义的NGSI-LD标准 [ETSI-GS-CIM-009] 基于：
- NGSI-LD信息模型：从标记属性图（LPG）模型派生，基于RDF进行数据语义注释
- NGSI-LD API：定义用于构建和与图交互的REST API

### 2.4 知识对象（Knowledge Objects）

**定义**:
知识对象是任意大小的知识图子集（从单个原子到数十或数百个三元组），用元数据装饰以促进其上下文化。

**应用**:
- 使使用知识图谱的实体能够相互通信知识片段
- 从知识图谱获得或从其他源（如监控）新创建的知识
- 在 [SECDEP] 中得到了证明

---

## 🔧 **三、知识图谱构建（KGC）/ Knowledge Graph Construction**

知识图谱的构建可以分为两个主要活动：本体开发（第4.1节）和知识图谱构建管道（第4.2节）。

### 3.1 本体开发 / Ontology Development

本体提供概念模型的形式表示，捕获数据的语义，并在此基础上实现知识图谱中的数据集成。本体可以根据数据特征（如格式或模式）使用不同的技术开发，从手动到完全自动化。

#### 3.1.1 从YANG模型自动提取知识

**YANG Identity的作用**:
- [RFC7950] 将YANG identity定义为"全局唯一、抽象、无类型的身份"
- YANG identity与概念之间的关系是直接的
- YANG identity可以通过"base"语句从其他YANG identity继承
- 这些思想与分类法的概念一致，其中概念与其他概念层次链接

**SKOS（简单知识组织系统）**:
- W3C标准化了SKOS以支持创建知识结构（如分类法或词表）
- 在SKOS本体中，概念方案包括一组概念，可以通过层次和关联关系与其他概念链接

**转换规则**:
1. 包含YANG identity的YANG模型可以表示为`skos:ConceptScheme`类的实例
2. YANG模型中包含的所有YANG identity可以表示为包含在概念方案中的`skos:Concept`实例
3. 包含"base"语句的YANG identity，相应的SKOS概念将包括关系`skos:broader`，其范围是表示父YANG identity的SKOS概念

#### 3.1.2 标准开发方法论

**LOT（Linked Open Terms）方法**:
- 采用敏捷软件开发最佳实践的本体开发方法论
- 在欧洲项目和ETSI SAREF本体的创建中广泛使用
- SAREF本体解决了IoT领域的类似问题，存在异构的标准数据模型和协议

**LOT工作流程**:
1. **本体需求规范**: 收集领域专家知识，分析数据源和模式
   - 方法：能力问题（CQs）、自然语言语句、表格信息（受METHONTOLOGY启发）
2. **本体实现**: 基于需求规范实现本体
3. **本体发布**: 发布和共享本体
4. **本体维护**: 持续更新和维护本体

### 3.2 知识图谱构建管道 / Knowledge Graph Construction Pipeline

知识图谱的构建由遵循典型提取-转换-加载（ETL）的数据管道支持，其中原始数据从源收集、转换，最后存储以供消费。

**管道架构**:
```
+-----------+ +---------+ +-----------------+
|           | |         | |                 |
| Ingestion +------>| Mapping +------>| Materialization |
|           | Raw     | | RDF   |         |
+-----------+ data    +---------+ data   +--------+--------+
 ^ (YANG)   |         |         |        |        |
 Raw        |         | RDF     |        |        |
 data       |         | data    |        |        |
(YANG)      |         |         |        |        |
 |          v         v         v        |        |
+-----+----+ +-----------+ +-----------+
| Data |    | Knowledge  |
| Source |  | Graph      |
| (device) | +-----------+
+----------+
```

#### 3.2.1 摄取（Ingestion）

**定义**:
知识图谱创建的第一步，通过收集器从选定的数据源摄取原始数据。

**数据访问协议**:
- NETCONF [RFC6241]
- RESTCONF [RFC8040]
- gNMI

**数据源类型**:

1. **批处理数据源**:
   - 数据从数据源拉取（一次或定期）
   - 示例：发送到YANG服务器（如SDN控制器）的查询以获取网络拓扑 [RFC8345]

2. **流数据源**:
   - 收集器订阅YANG服务器以接收YANG数据的通知
   - 定期或在数据源发生变化时（如网络设备接口关闭）
   - 机制：YANG Push [RFC8641]
   - 消息代理系统：Apache Kafka用于解耦YANG数据流的摄取 [I-D.netana-nmop-yang-message-broker-integration]

#### 3.2.2 映射（Mapping）

**定义**:
接收来自摄取步骤的原始数据，将原始数据映射到捕获在一个或多个本体中的概念。

**映射语言**:
- RDF映射语言（RML）[Iglesias-Molina2023]
- 声明性语言，当前正在W3C知识图谱构建社区组 [W3C-KGC] 中标准化
- 允许定义半结构化格式（如XML或JSON）编码的原始数据的映射规则

**RML的优势**:
1. **解耦**: 实现RML规则的引擎是通用的，映射规则与代码解耦
2. **数据血缘**: 映射和转换规则的显式表示作为知识图谱的一部分，提供数据血缘洞察，可以大大提高数据质量并简化数据管道的故障排除

**挑战**:
- RML正在向标准发展，但支持其他YANG编码格式（如CBOR [RFC8949] 或Protobuf）仍然是一个挑战
- CBOR和/或Protobuf携带的知识负载组织为知识对象，由映射实体传输并由物化实体接收
- 知识对象的使用允许轻松地将知识图谱"切割"成更小的片段，传输它们，并将片段"粘贴"和/或"粘合"到目标知识图谱上
- 通过使用相同的本体与特定的知识对象来保持一致性

#### 3.2.3 物化（Materialization）

**定义**:
知识图谱创建的最后一步，接收包含在映射步骤中生成的RDF数据的知识对象作为输入。

**存储选项**:

1. **RDF三元存储**:
   - Apache Jena Fuseki [Fuseki]
   - 通过SPARQL消费

2. **图数据库（LPG）**:
   - 将RDF数据转换为LPG结构
   - 存储在Neo4j [Neo4j] 等图数据库中

3. **NGSI-LD上下文代理**:
   - 将RDF数据转换为ETSI NGSI-LD标准
   - 存储在NGSI-LD上下文代理中

---

## 💡 **四、知识图谱应用 / Knowledge Graph Applications**

### 4.1 网络性能KPI

**应用场景**:
- 集成网络中不同抽象层的数据，便于计算网络性能KPI（如吞吐量或丢包率）
- 集成数据孤岛（如网络拓扑与网络接口状态）

**示例**:
- 网络分析应用程序可以要求知识图谱计算网络中特定链路的吞吐量或丢包率
- 通过查询知识图谱，结合拓扑和接口状态数据，自动计算性能指标

### 4.2 异常检测和事件管理

**应用场景**:
- 链接来自不同数据孤岛的数据（网络基础设施、日志、告警、工单）
- 检测网络系统中的异常

**示例**:
- NORIA项目 [Tailhardat2023] 展示了知识图谱如何帮助检测网络系统中的异常
- 结合网络拓扑数据与网络接口状态数据，检测网络异常（如链路故障）
- 检测场景：网络接口意外禁用但配置为启用

### 4.3 服务保障

**应用场景**:
- 实现基于意图的网络架构的服务保障 [RFC9417]
- 集成RFC 9418中定义的YANG数据模型

**保障图**:
- 捕获网络服务之间的依赖关系及其相关的健康状态和症状
- 所有这些数据可以进一步与其他数据孤岛（如网络拓扑或网络接口状态）链接
- 自然集成并表示在知识图谱中

### 4.4 网络数字孪生

**应用场景**:
- 知识图谱被认为是实现网络数字孪生的有前途的候选技术 [I-D.irtf-nmrg-network-digital-twin-arch]
- 使用知识图谱构建专门用于检测网络故障的网络数字孪生的好处在 [ANSA] 中得到了证明

**优势**:
- 集成异构数据孤岛的能力
- 数据的显式语义表示
- 通过本体表示概念，产生网络数字孪生的抽象表示，无论底层技术的复杂性如何

**示例**:
- 知识图谱中网络拓扑数字地图 [I-D.havel-nmop-digital-map] 的抽象表示可以转换为特定于所用技术的描述符或数据模型（如KNE、ContainerLab或OSM）

### 4.5 YANG Catalog的演进

**应用场景**:
- 知识图谱的灵活性和可扩展性使其成为实现数据目录的热门选择
- 数据目录的目的是为消费者提供数据源暴露的数据集注册表，以查找感兴趣的数据

**演进方向**:
- YANG Catalog可以演变为数据目录，其中YANG模块代表感兴趣的数据集
- YANG模型之间的依赖关系（导入、偏差、增强）可以在知识图谱中自然表示
- YANG模型可以与本体中表示的概念链接
- 可以结合网络设备的实现细节（yang lib augment [I-D.lincla-netconf-yang-library-augmentation]），这些可能是清单的一部分 [I-D.ietf-ivy-network-inventory-yang]

### 4.6 上下文化遥测数据

**应用场景**:
- 了解YANG遥测数据 [I-D.ietf-opsawg-collected-data-manifest] 如何收集可以改善网络分析或闭环自动化的数据理解

**实现方式**:
- 知识图谱可以通过将收集的数据与以下内容链接来帮助完成此任务：
  1. 表征产生数据的平台的元数据
  2. 表征如何以及何时计量数据的元数据

**优势**:
- 如 [TKDP] 所示，将知识图谱和知识对象应用于遥测数据管理有助于降低多个任务和整体操作的耦合水平
- 通过不同利益相关者的协作，能够解决当前的网络问题

### 4.7 人工智能在网络管理中的具体化

**应用场景**:
- 将知识图谱应用于遥测数据对于将人工智能（AI）方法应用于网络管理特别必要，如 [AINEMA] 所支持

**实现方式**:
- 多个AI元素可以在以下情况下连贯地互操作：
  1. 它们使用相同的本体
  2. 它们管理更大知识图谱的几个子图
  3. 它们使用知识对象相互通信基于知识的消息

**优势**:
- 如 [EERVC] 中讨论的典型网络场景中证明了这一好处

---

## ⚠️ **五、挑战 / Challenges**

### 5.1 本体开发

**挑战**:
- 耗时的任务，需要知识管理和概念建模技能
- 本体开发者应与领域所有者和本体用户保持紧密协调
- 遵循标准方法论（如LOT）提供指导，但本体开发仍需要手动工作

**解决方案**:
- 需要能够从现有YANG数据模型半自动或甚至自动生成或引导本体的工具
- YANG语言的未来版本可以在设计时扩展以促进此任务
- YANG数据模型可以包括数据模型中的显式语义，类似于JSON-LD [JSON-LD] 或CSVW [CSVW] 包含元数据，指示数据引用的概念
- 在当前版本的YANG中，可以使用YANG元数据扩展 [RFC7952] 在运行时实现
- 使用此扩展，YANG数据模型可以包括额外的元数据，以指示YANG数据节点引用的本体概念，尽管这种方法仅在运行时有效，并且需要增强现有的YANG数据模型

### 5.2 管道性能

**挑战**:
- 将原始数据从原始源集成到知识图谱中需要多个步骤
- 这些步骤在数据存储在知识图谱中供消费之前增加了额外的延迟
- 对于实时分析用例，此延迟可能是一个重要的限制

**影响**:
- 实时分析和自动化场景的响应时间受限
- 需要优化管道性能

### 5.3 可扩展性

**挑战**:
- 知识图谱必须能够集成从网络收集的大量数据
- 分布式和联邦架构可以改善全局、可组合知识图谱的可扩展性
- 但这些架构增加了知识图谱管理的复杂性，以及在联邦请求时的额外延迟

**解决方案**:
- 分布式架构设计
- 联邦知识图谱架构
- 性能优化技术

### 5.4 虚拟化

**挑战**:
- 数据集成的常见方法是在知识图谱中物化数据，这需要复制数据
- 这种方法在数据治理和数据节奏方面存在多个限制

**数据治理问题**:
- 拥有原始数据的副本阻碍了跟踪所有可用数据

**数据节奏问题**:
- 对于批处理数据源，数据以特定频率定期从源拉取，这可能不是最优的，取决于用例

**解决方案**:
- 数据虚拟化引入了一种新的数据访问技术，可以克服这些限制
- 使用此技术，知识图谱定义指向原始源数据的指针
- KGC管道仅在按需请求时执行数据的摄取和映射，并最终将数据交付给消费者

### 5.5 网络配置

**当前焦点**:
- 本文档专注于在知识图谱中集成遥测数据以用于监控目的

**扩展方向**:
- 知识图谱也可以用于集成与网络中设备和服务的配置相关的数据
- 这种方法可以实现闭环网络管理，因为配置和操作数据都存储在知识图谱中

---

## 🔒 **六、安全考虑 / Security Considerations**

### 6.1 数据访问控制

**要求**:
- 知识图谱成为数据的集成器，在许多情况下是敏感的
- 必须存在数据访问控制机制，以确保只有授权的消费者才能发现和访问知识图谱中的数据

**方法**:
- 基于角色或属性的访问控制策略是常见方法
- 但可以包括其他方面，如数据的敏感性

### 6.2 映射的完整性和真实性

**重要性**:
- 将原始数据映射到本体中的概念的声明是知识图谱构建中的关键步骤
- 未经授权的映射，甚至被篡改的映射，可能导致安全漏洞和异常，对消费知识图谱数据的分析和机器学习应用程序产生重大影响

**保护机制**:
- 知识图谱必须包括验证用于构建图的映射的正确性、真实性和完整性的机制
- 只有数据所有者，作为其数据的责任人，应该被授权定义和部署用于知识图谱构建的映射

### 6.3 数据来源（Data Provenance）

**价值**:
- 跟踪数据在知识图谱构建管道中的历史可以改善知识图谱数据的质量

**实现**:
- 作为知识图谱构建的一部分，可以将签名附加到数据 [I-D.lopez-opsawg-yang-provenance]
- 这有助于验证此类数据来自黄金数据源，因此可以信任数据

---

## 🔬 **七、实施案例 / Implementation Cases**

### 7.1 故障诊断案例

**场景**:
使用知识图谱和SPARQL查询进行网络故障诊断。

**SPARQL查询示例**:
```sparql
PREFIX net: <http://example.org/network#>
PREFIX yang: <http://example.org/yang#>

SELECT ?device ?interface ?status ?alarm
WHERE {
  ?device yang:hasInterface ?interface .
  ?interface yang:status ?status .
  ?interface yang:hasAlarm ?alarm .
  FILTER (?status = "down" || ?alarm = "critical")
}
```

**优势**:
- 跨多个数据源自动关联故障信息
- 快速定位问题根源

### 7.2 配置自动化案例

**场景**:
基于知识图谱的语义理解，自动生成和验证网络配置。

**流程**:
1. 从知识图谱查询设备能力和当前配置
2. 基于意图和策略生成配置
3. 使用本体验证配置一致性
4. 自动部署配置

### 7.3 性能优化案例

**场景**:
通过知识图谱关联拓扑、流量和性能数据，优化网络性能。

**分析**:
- 识别瓶颈链路
- 分析流量模式
- 优化路由策略
- 预测性能问题

### 7.4 安全分析案例

**场景**:
集成安全事件、配置和拓扑数据，进行安全威胁分析。

**能力**:
- 关联安全事件与网络拓扑
- 识别攻击路径
- 评估安全策略有效性
- 自动响应安全威胁

---

## 🚀 **八、未来方向 / Future Directions**

### 8.1 标准化进展

**RML映射**:
- RML映射是否应该使用XPath或子树过滤器在YANG级别引用数据？
- 或者引用应该基于网络管理协议使用的实际编码格式，例如JSON、XML

**URI生成**:
- 本文档是否应该提供生成知识图谱中节点/主题的URI的指南？
- 考虑有多个抽象级别（设备vs网络/服务级别）
- 例如，标识网络接口的URI不能仅从接口名称生成，因为可能与其他网络设备的其他接口发生冲突

**数据源定义**:
- 使用形式词汇定义YANG数据源，类似于Web of Things本体为MQTT或REST API所做的，或D2RQ本体为关系数据库所做的
- 在知识图谱中指定数据源可以改善来源，并将配置与实现解耦，例如通过自定义INI配置文件

### 8.2 实施参考

**开源实现**:
- 需要基于开源实现的示例参考
- 与YANG-Push-Kafka架构集成
- 目标未来的hackathons

### 8.3 范围扩展

**当前焦点**:
- 本文档专注于YANG数据源

**扩展考虑**:
- 文档是否应该将范围扩展到其他类型的数据源，如IPFIX？

---

## 📚 **九、相关标准与规范 / Related Standards and Specifications**

### 9.1 IETF标准

- **RFC 7950**: YANG 1.1数据建模语言
- **RFC 6241**: NETCONF协议
- **RFC 8040**: RESTCONF协议
- **RFC 8343**: 接口管理的YANG数据模型
- **RFC 8345**: 网络拓扑的YANG数据模型
- **RFC 8641**: YANG Push订阅
- **RFC 9417**: 基于意图的网络的服务保障架构
- **RFC 9418**: 服务保障的YANG数据模型
- **RFC 9232**: 网络遥测框架

### 9.2 W3C标准

- **RDF**: 资源描述框架
- **RDFS**: RDF模式
- **OWL**: Web本体语言
- **SHACL**: 形状约束语言
- **SPARQL**: SPARQL查询语言
- **SKOS**: 简单知识组织系统

### 9.3 ETSI标准

- **ETSI-GS-CIM-009**: NGSI-LD API
- **SAREF**: 智能应用参考本体

### 9.4 相关IETF草案

- **draft-mackey-nmop-kg-for-netops-03**: 网络操作的知识图谱框架
- **draft-irtf-nmrg-network-digital-twin-arch**: 网络数字孪生参考架构
- **draft-havel-nmop-digital-map**: 基于RFC 8345的数字地图建模
- **draft-ietf-ivy-network-inventory-yang**: 网络清单的YANG数据模型
- **draft-ietf-opsawg-collected-data-manifest**: 上下文化遥测数据的数据清单
- **draft-lopez-opsawg-yang-provenance**: YANG数据来源的COSE签名应用
- **draft-netana-nmop-yang-message-broker-integration**: YANG-Push到消息代理集成的架构
- **draft-pedro-nmrg-ai-framework**: 网络管理的人工智能框架

---

## 📊 **十、总结 / Summary**

### 10.1 核心价值

知识图谱为YANG网络管理提供了强大的解决方案，通过：

1. **语义集成**: 解决YANG数据模型的异构性问题，实现概念级别的数据集成
2. **关系显式化**: 将隐式关系转换为图结构中的显式关系
3. **智能分析**: 支持高级网络分析和自动化应用
4. **标准化**: 基于成熟的W3C语义网标准和IETF网络管理标准

### 10.2 关键技术

1. **本体开发**: 从YANG模型自动提取知识，使用LOT方法论
2. **ETL管道**: 摄取、映射、物化的完整流程
3. **多种存储**: 支持RDF三元存储、LPG图数据库、NGSI-LD上下文代理
4. **知识对象**: 支持知识图谱的分布式处理和通信

### 10.3 应用场景

1. 网络性能KPI计算
2. 异常检测和事件管理
3. 服务保障
4. 网络数字孪生
5. YANG Catalog演进
6. 上下文化遥测数据
7. AI驱动的网络管理

### 10.4 挑战与方向

**主要挑战**:
- 本体开发需要时间和专业知识
- 管道性能优化
- 可扩展性设计
- 数据虚拟化
- 网络配置集成

**未来方向**:
- RML映射标准化
- URI生成指南
- 数据源形式化定义
- 开源实现参考
- 扩展到其他数据源类型

---

## 📖 **参考文献 / References**

### 标准文档

- [RFC7950] Bjorklund, M., Ed., "The YANG 1.1 Data Modeling Language", RFC 7950, DOI 10.17487/RFC7950, August 2016
- [RFC6241] Enns, R., Ed., Bjorklund, M., Ed., Schoenwaelder, J., Ed., and A. Bierman, Ed., "Network Configuration Protocol (NETCONF)", RFC 6241, DOI 10.17487/RFC6241, June 2011
- [RFC8040] Bierman, A., Bjorklund, M., and K. Watsen, "RESTCONF Protocol", RFC 8040, DOI 10.17487/RFC8040, January 2017
- [RFC8343] Bjorklund, M., "A YANG Data Model for Interface Management", RFC 8343, DOI 10.17487/RFC8343, March 2018
- [RFC8345] Clemm, A., Medved, J., Varga, R., Bahadur, N., Ananthakrishnan, H., and X. Liu, "A YANG Data Model for Network Topologies", RFC 8345, DOI 10.17487/RFC8345, March 2018
- [RFC8641] Clemm, A. and E. Voit, "Subscription to YANG Notifications for Datastore Updates", RFC 8641, DOI 10.17487/RFC8641, September 2019
- [RFC9417] Claise, B., Quilbeuf, J., Lopez, D., Voyer, D., and T. Arumugam, "Service Assurance for Intent-Based Networking Architecture", RFC 9417, DOI 10.17487/RFC9417, July 2023
- [RFC9418] Claise, B., Quilbeuf, J., Lucente, P., Fasano, P., and T. Arumugam, "A YANG Data Model for Service Assurance", RFC 9418, DOI 10.17487/RFC9418, July 2023
- [RFC9232] Song, H., Qin, F., Martinez-Julia, P., Ciavaglia, L., and A. Wang, "Network Telemetry Framework", RFC 9232, DOI 10.17487/RFC9232, May 2022

### IETF草案

- [draft-marcas-nmop-knowledge-graph-yang-05] Martinez-Casanueva, I. D., Cabanillas, L., Martinez-Julia, P. M., "Knowledge Graphs for YANG-based Network Management", Work in Progress, Internet-Draft, draft-marcas-nmop-knowledge-graph-yang-05, October 2024

### 学术论文

- [Tailhardat2023] "Designing NORIA: a Knowledge Graph-based Platform for Anomaly Detection and Incident Management in ICT Systems", KGCW'23: 4th International Workshop on Knowledge Graph Construction, May 2023
- [Iglesias-Molina2023] Iglesias-Molina, A., "The RML Ontology: A Community-Driven Modular Redesign After a Decade of Experience in Mapping Heterogeneous Data to RDF", The Semantic Web – ISWC 2023, October 2023
- [Poveda-Villalon2022] "LOT: An industrial oriented ontology engineering framework", Engineering Applications of Artificial Intelligence, May 2022

---

**文档状态**: ✅ 完成  
**最后更新**: 2025年1月  
**质量等级**: ⭐⭐⭐⭐⭐ 五星级  
**国际对标**: ✅ IETF标准对齐
