/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50529
 Source Host           : localhost:3306
 Source Schema         : py_blog

 Target Server Type    : MySQL
 Target Server Version : 50529
 File Encoding         : 65001

 Date: 17/10/2025 18:21:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of categories
-- ----------------------------
INSERT INTO `categories` VALUES (2, '技术分享', '2025-10-17 09:28:46');
INSERT INTO `categories` VALUES (3, '生活随笔', '2025-10-17 09:28:46');
INSERT INTO `categories` VALUES (4, '旅行日记', '2025-10-17 09:28:46');
INSERT INTO `categories` VALUES (5, '读书笔记', '2025-10-17 09:28:46');

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `author_name` varchar(80) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `author_email` varchar(120) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `is_approved` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `post_id` int(11) NOT NULL,
  `author_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `post_id`(`post_id`) USING BTREE,
  INDEX `author_id`(`author_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comments
-- ----------------------------
INSERT INTO `comments` VALUES (1, '这篇文章写得很好，对我学习Flask帮助很大！', NULL, NULL, 1, '2025-10-17 09:28:46', 1, 2);
INSERT INTO `comments` VALUES (2, '感谢分享，MySQL优化确实很重要。', NULL, NULL, 1, '2025-10-17 09:28:46', 2, 2);
INSERT INTO `comments` VALUES (3, '生活需要这样的慢时光，很治愈。', '游客', 'visitor@example.com', 1, '2025-10-17 09:28:46', 3, NULL);

-- ----------------------------
-- Table structure for post_tags
-- ----------------------------
DROP TABLE IF EXISTS `post_tags`;
CREATE TABLE `post_tags`  (
  `post_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`post_id`, `tag_id`) USING BTREE,
  INDEX `tag_id`(`tag_id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Fixed;

-- ----------------------------
-- Records of post_tags
-- ----------------------------
INSERT INTO `post_tags` VALUES (1, 1);
INSERT INTO `post_tags` VALUES (1, 2);
INSERT INTO `post_tags` VALUES (1, 4);
INSERT INTO `post_tags` VALUES (2, 3);
INSERT INTO `post_tags` VALUES (2, 4);
INSERT INTO `post_tags` VALUES (3, 5);
INSERT INTO `post_tags` VALUES (4, 6);
INSERT INTO `post_tags` VALUES (5, 1);
INSERT INTO `post_tags` VALUES (5, 7);

-- ----------------------------
-- Table structure for posts
-- ----------------------------
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `summary` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `is_published` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `author_id` int(11) NOT NULL,
  `category_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `author_id`(`author_id`) USING BTREE,
  INDEX `category_id`(`category_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of posts
-- ----------------------------
INSERT INTO `posts` VALUES (1, 'Flask入门教程', '<p>Flask是一个使用Python编写的轻量级Web应用框架。基于Werkzeug WSGI工具箱和Jinja2模板引擎。</p><p>Flask被称为\"microframework\"，因为它使用简单的核心，用extension增加其他功能。Flask没有默认使用的数据库、窗体验证工具。</p>', 'Flask是一个使用Python编写的轻量级Web应用框架。本文介绍了Flask的基本概念和使用方法。', 1, '2025-10-17 09:28:46', '2025-10-17 09:28:46', 1, 2);
INSERT INTO `posts` VALUES (2, 'MySQL数据库优化技巧', '<p>MySQL是世界上最流行的开源关系型数据库管理系统之一。在实际应用中，数据库性能优化是非常重要的。</p><p>本文将介绍几种常见的MySQL优化技巧：</p><ul><li>索引优化</li><li>查询优化</li><li>表结构设计</li><li>配置参数调整</li></ul>', 'MySQL是世界上最流行的开源关系型数据库管理系统之一。本文介绍了几种常见的MySQL优化技巧。', 1, '2025-10-17 09:28:46', '2025-10-17 09:28:46', 1, 2);
INSERT INTO `posts` VALUES (3, '周末的悠闲时光', '<p>忙碌了一周，终于迎来了周末。阳光透过窗帘洒在桌面上，一切都显得那么宁静美好。</p><p>泡一壶茶，拿起一本喜欢的书，享受这难得的悠闲时光。生活不只有工作，还有诗和远方。</p>', '忙碌了一周，终于迎来了周末。享受这难得的悠闲时光，感受生活的美好。', 1, '2025-10-17 09:28:46', '2025-10-17 09:28:46', 2, 3);
INSERT INTO `posts` VALUES (4, '春天的旅行计划', '<p>春天是旅行的好季节，万物复苏，景色宜人。计划一次说走就走的旅行，去感受大自然的美好。</p><p>推荐几个适合春季旅行的地方：</p><ol><li>江南水乡</li><li>云南大理</li><li>桂林山水</li><li>杭州西湖</li></ol>', '春天是旅行的好季节，推荐几个适合春季旅行的地方，计划一次说走就走的旅行。', 1, '2025-10-17 09:28:46', '2025-10-17 09:28:46', 2, 4);
INSERT INTO `posts` VALUES (5, '《Python编程：从入门到实践》读后感', '<p>最近读完了《Python编程：从入门到实践》这本书，收获颇丰。这本书非常适合Python初学者，内容循序渐进，实例丰富。</p><p>书中主要涵盖了以下几个方面的内容：</p><ul><li>Python基础知识</li><li>数据可视化</li><li>Web开发</li><li>项目实战</li></ul><p>通过这本书的学习，我对Python有了更深入的理解，也激发了我继续深入学习的兴趣。</p>', '《Python编程：从入门到实践》是一本非常适合Python初学者的书籍，内容循序渐进，实例丰富。', 1, '2025-10-17 09:28:46', '2025-10-17 09:28:46', 1, 5);

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tags
-- ----------------------------
INSERT INTO `tags` VALUES (1, 'Python', '2025-10-17 09:28:46');
INSERT INTO `tags` VALUES (2, 'Flask', '2025-10-17 09:28:46');
INSERT INTO `tags` VALUES (3, 'MySQL', '2025-10-17 09:28:46');
INSERT INTO `tags` VALUES (4, 'Web开发', '2025-10-17 09:28:46');
INSERT INTO `tags` VALUES (5, '生活', '2025-10-17 09:28:46');
INSERT INTO `tags` VALUES (6, '旅行', '2025-10-17 09:28:46');
INSERT INTO `tags` VALUES (7, '读书', '2025-10-17 09:28:46');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(120) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `is_admin` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', 'admin@example.com', 'pbkdf2:sha256:260000$PavnyEBczoqB42Vz$9e3b91990700e8ce83e875a9f6b3d2f0645507c1bae621ecfce5cf18485bfd5c', 1, '2025-10-17 09:24:02');
INSERT INTO `users` VALUES (2, 'user1', 'user1@example.com', 'pbkdf2:sha256:260000$mfh5lUWeylexFXh9$41104bd9d40271ba67de698e34d9b737225286bd835d8280c0a7f9dd8233fbdc', 0, '2025-10-17 09:28:46');

SET FOREIGN_KEY_CHECKS = 1;
