-- ----------------------------
-- 1、部门表
-- ----------------------------
drop table if exists sys_dept;
create table sys_dept (
  `id`                BIGINT(20)   NOT NULL AUTO_INCREMENT COMMENT '部门id',
  `parent_id`         BIGINT(20)   DEFAULT 0               COMMENT '父部门id',
  `dept_name`         VARCHAR(30)  DEFAULT NULL            COMMENT '部门名称',
  `order_num`       INT(4)       DEFAULT 0               COMMENT '显示顺序',
  `leader`          VARCHAR(20)  DEFAULT NULL            COMMENT '负责人',
  `phone`           VARCHAR(20)  DEFAULT NULL            COMMENT '联系电话',
  `email`           VARCHAR(128) DEFAULT NULL            COMMENT '邮箱',
  `status`          TINYINT(1)   DEFAULT 1               COMMENT '部门状态(0停用 1正常)',
  `deleted`         TINYINT(1)   DEFAULT 0               COMMENT '删除标志(0代表存在 1代表删除)',
  `create_by`       VARCHAR(64)  DEFAULT NULL            COMMENT '创建者',
  `create_time`     DATETIME                             COMMENT '创建时间',
  `update_by`       VARCHAR(64)  DEFAULT NULL            COMMENT '更新者',
  `update_time`     DATETIME                             COMMENT '更新时间',
  `remark`          VARCHAR(255) DEFAULT NULL            COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT=100 COMMENT = '部门表';

-- ----------------------------
-- 2、用户表
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
  `id`              BIGINT(20)   NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username`        VARCHAR(30)  NOT NULL                COMMENT '用户账号',
  `nickname`        VARCHAR(30)  NOT NULL                COMMENT '用户昵称',
  `sex`             TINYINT(1)   DEFAULT 1               COMMENT '性别(0女 1男 2未知)',
  `password`        VARCHAR(100) DEFAULT NULL            COMMENT '密码',
  `avatar`          VARCHAR(255) DEFAULT NULL            COMMENT '用户头像',
  `phone`           VARCHAR(20)  DEFAULT NULL            COMMENT '手机号码',
  `status`          TINYINT(1)   DEFAULT 1               COMMENT '账号状态(0停用 1正常)',
  `email`           VARCHAR(128) DEFAULT NULL            COMMENT '用户邮箱',
  `deleted`         TINYINT(1)   DEFAULT 0               COMMENT '删除标志(0代表存在 1代表删除)',
  `create_by`       VARCHAR(64)  DEFAULT NULL            COMMENT '创建者',
  `create_time`     DATETIME                             COMMENT '创建时间',
  `update_by`       VARCHAR(64)  DEFAULT NULL            COMMENT '更新者',
  `update_time`     DATETIME                             COMMENT '更新时间',
  `remark`          VARCHAR(255) DEFAULT NULL            COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 100 COMMENT = '用户表';


-- ----------------------------
-- 3、角色表
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role` (
  `id`              BIGINT(20)   NOT NULL AUTO_INCREMENT  COMMENT '角色ID',
  `name`            VARCHAR(64)  NOT NULL                 COMMENT '角色名称',
  `code`            VARCHAR(32)  NOT NULL                 COMMENT '角色编码',
  `status`          TINYINT(1)   DEFAULT 1                COMMENT '角色状态(0停用 1正常)',
  `deleted`         TINYINT(1)   DEFAULT 0                COMMENT '删除标志(0代表存在 1代表删除)',
  `create_by`       VARCHAR(64)  DEFAULT NULL             COMMENT '创建者',
  `create_time`     DATETIME                              COMMENT '创建时间',
  `update_by`       VARCHAR(64)  DEFAULT NULL             COMMENT '更新者',
  `update_time`     DATETIME                              COMMENT '更新时间',
  `remark`          VARCHAR(255) DEFAULT NULL             COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name`)
) ENGINE = InnoDB AUTO_INCREMENT = 100 COMMENT = '角色表';


-- ----------------------------
-- 4、菜单权限表
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu` (
  `id`              BIGINT(20)   NOT NULL AUTO_INCREMENT   COMMENT '菜单ID',
  `parent_id`       BIGINT(20)   DEFAULT 0                 COMMENT '父菜单ID',
  `name`            VARCHAR(50)  DEFAULT NULL              COMMENT '路由名称',
  `title`           VARCHAR(64)  NOT NULL                  COMMENT '菜单名称/标题',
  `path`            VARCHAR(128) DEFAULT NULL              COMMENT '路由路径',
  `component`       VARCHAR(128) DEFAULT NULL              COMMENT '组件路径',
  `auths`           VARCHAR(100) DEFAULT NULL              COMMENT '权限标识',
  `icon`            VARCHAR(64)  DEFAULT '#'               COMMENT '菜单图标',
  `rank`            INT          DEFAULT 0                 COMMENT '排序',
  `type`            TINYINT(1)   NOT NULL DEFAULT 0        COMMENT '菜单类型 (0:目录/页面 1:菜单 2:接口 3:按钮 4:外链)',
  `show_link`       TINYINT(1)   DEFAULT 1                 COMMENT '是否在菜单中显示',
  `frame_src`       VARCHAR(255) DEFAULT NULL              COMMENT '内嵌 链接',
  `keep_alive`      TINYINT(1)   DEFAULT 1                 COMMENT '缓存标识 (0:不缓存 1:缓存)',
  `redirect`        VARCHAR(128) DEFAULT NULL              COMMENT '重定向路径',
  `extra_icon`      VARCHAR(100) DEFAULT NULL              COMMENT '额外图标',
  `enter_transition` VARCHAR(100) DEFAULT NULL             COMMENT '进入过渡动画',
  `leave_transition` VARCHAR(100) DEFAULT NULL             COMMENT '离开过渡动画',
  `active_path`     VARCHAR(128) DEFAULT NULL              COMMENT '激活路径',
  `frame_loading`   TINYINT(1)   DEFAULT 1                 COMMENT '内嵌加载状态 (0:不加载 1:加载)',
  `hidden_tag`      TINYINT(1)   DEFAULT 0                 COMMENT '隐藏标签 (0:不隐藏 1:隐藏)',
  `fixed_tag`       TINYINT(1)   DEFAULT 0                 COMMENT '固定标签 (0:不固定 1:固定)',
  `show_parent`     TINYINT(1)   DEFAULT 0                 COMMENT '显示父菜单 (0:不显示 1:显示)',
  `create_by`       VARCHAR(64)  DEFAULT NULL              COMMENT '创建者',
  `create_time`     DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by`       VARCHAR(64)  DEFAULT NULL              COMMENT '更新者',
  `update_time`     DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark`          VARCHAR(255) DEFAULT NULL              COMMENT '备注',
  PRIMARY KEY (`id`),
  INDEX idx_parent_id (`parent_id`) -- 为父菜单ID创建索引，便于查询子菜单
) ENGINE = InnoDB AUTO_INCREMENT = 1000 COMMENT = '菜单管理';


-- ----------------------------
-- 5、用户和角色关联表  用户N-1角色
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role` (
  `user_id`         BIGINT(20)   NOT NULL COMMENT '用户ID',
  `role_id`         BIGINT(20)   NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`, `role_id`)
) ENGINE = InnoDB COMMENT = '用户角色关联表';

-- ----------------------------
-- 6、角色和菜单关联表  角色1-N菜单
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu` (
  `role_id`         BIGINT(20)   NOT NULL COMMENT '角色ID',
  `menu_id`         BIGINT(20)   NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`, `menu_id`)
) ENGINE = InnoDB COMMENT = '角色和菜单关联表';


-- ----------------------------
-- 6、用户和部门关联表 用户1-1部门
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_dept`;
CREATE TABLE `sys_user_dept` (
  `user_id`         BIGINT(20)   NOT NULL COMMENT '用户ID',
  `dept_id`         BIGINT(20)   NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`user_id`, `dept_id`)
) ENGINE = InnoDB COMMENT = '用户和部门关联表';


-- ----------------------------
-- 7、系统登陆日志表
-- ----------------------------
DROP TABLE IF EXISTS `sys_login_log`;
CREATE TABLE `sys_login_log` (
  `id`           BIGINT(20)     NOT NULL AUTO_INCREMENT  COMMENT '访问ID',
  `username`     VARCHAR(50)    NOT NULL DEFAULT ''      COMMENT '用户账号',
  `ip`           VARCHAR(128)   NOT NULL DEFAULT ''      COMMENT '登录IP地址',
  `address`      VARCHAR(255)   NOT NULL DEFAULT ''      COMMENT '登录地点',
  `browser`      VARCHAR(50)    NOT NULL DEFAULT ''      COMMENT '浏览器类型',
  `system`       VARCHAR(50)    NOT NULL DEFAULT ''      COMMENT '操作系统',
  `status`       TINYINT(1)     NOT NULL DEFAULT 1       COMMENT '登录状态（1成功 0失败）',
  `behavior`     VARCHAR(255)   NOT NULL DEFAULT ''      COMMENT '提示消息',
  `login_time`   DATETIME       NULL     DEFAULT NULL    COMMENT '访问时间',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 154 COMMENT = '系统登陆记录';

-- ----------------------------
-- 7、系统操作日志表
-- ----------------------------
DROP TABLE IF EXISTS `sys_operation_log`;
CREATE TABLE `sys_operation_log` (
  `id`            BIGINT(20)     NOT NULL AUTO_INCREMENT  COMMENT '主键ID',
  `username`      VARCHAR(50)    NOT NULL                 COMMENT '用户名',
  `ip`            VARCHAR(45)    NULL     DEFAULT NULL    COMMENT '操作者IP地址',
  `address`       VARCHAR(255)   NULL     DEFAULT NULL    COMMENT '地理位置',
  `browser`       VARCHAR(50)    NULL     DEFAULT NULL    COMMENT '浏览器',
  `system`        VARCHAR(50)    NULL     DEFAULT NULL    COMMENT '操作系统',
  `status`        TINYINT(1)     NOT NULL                 COMMENT '操作状态 (1 成功, 0 失败)',
  `summary`       TEXT           NULL                     COMMENT '操作概要',
  `module`        VARCHAR(100)   NULL     DEFAULT NULL    COMMENT '所属模块',
  `operating_time` DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`),
  KEY `idx_username` (`username`) -- 为 username 添加索引，提高查询性能
) ENGINE = InnoDB AUTO_INCREMENT = 1 COMMENT = '系统操作记录';


-- ----------------------------
-- 8、系统日志记录表
-- ----------------------------
DROP TABLE IF EXISTS `sys_system_log`;
CREATE TABLE `sys_system_log` (
  `id`              BIGINT(20)     NOT NULL AUTO_INCREMENT  COMMENT '日志ID',
  `level`           TINYINT(1)     NOT NULL DEFAULT 1       COMMENT '日志级别 (0 debug, 1 info, 2 warn, 3 error, 4 fatal)',
  `module`          VARCHAR(100)   NOT NULL DEFAULT ''      COMMENT '所属模块',
  `url`             VARCHAR(500)   NOT NULL                 COMMENT '请求接口URL',
  `method`          VARCHAR(10)    NOT NULL                 COMMENT '请求方法 (GET, POST, PUT, DELETE 等)',
  `ip`              VARCHAR(45)    NULL     DEFAULT NULL    COMMENT '客户端IP地址',
  `address`         VARCHAR(255)   NULL     DEFAULT NULL    COMMENT '地理位置',
  `system`          VARCHAR(50)    NULL     DEFAULT NULL    COMMENT '操作系统',
  `browser`         VARCHAR(50)    NULL     DEFAULT NULL    COMMENT '浏览器',
  `takes_time`      INT            NULL     DEFAULT NULL    COMMENT '请求耗时 (单位: 毫秒 ms)',
  `request_time`    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '请求时间',
  `response_headers` JSON          NULL                     COMMENT '响应头 (JSON格式)',
  `response_body`   JSON       NULL                     COMMENT '响应体',
  `request_headers` JSON          NULL                     COMMENT '请求头 (JSON格式)',
  `request_body`    JSON       NULL                     COMMENT '请求体',
  `trace_id`        VARCHAR(64)    NULL     DEFAULT NULL    COMMENT '链路追踪ID',
  PRIMARY KEY (`id`),
  INDEX `idx_module` (`module`),                             -- 为模块添加索引
  INDEX `idx_url` (`url`),                                  -- 为URL添加索引
  INDEX `idx_level` (`level`),                              -- 为日志级别添加索引
  INDEX `idx_request_time` (`request_time`)                 -- 为请求时间添加索引，便于按时间查询
) ENGINE = InnoDB AUTO_INCREMENT = 1 COMMENT = '系统日志记录';