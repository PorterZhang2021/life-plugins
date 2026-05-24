# Life Plugins

个人 AI 助手配置仓库，沉淀日常可复用的 Skills，支持 Kimi Code CLI 等工具。

当前仓库主要面向 Kimi 生态，用于沉淀和管理个人自定义 skill。

## Repository Layout

| 目录 | 内容 |
| --- | --- |
| `skills/` | 自定义工作流 Skill，可被 Kimi 识别和调用。 |

## Skills

| Skill | 说明 |
| --- | --- |
| `daily-time-block` | 帮助在 Obsidian 日记中管理基于时间块的任务记录。适用于 `M/每日日记/` 目录下的 Markdown 文件，支持多段时间块结构、Todo 顺延、时间计算等功能。 |

## Skill 安装方式

### Kimi Code CLI

Kimi Code CLI 支持从本地目录加载自定义 skill。

1. 将本仓库克隆到本地（已完成）
2. 在 Kimi Code CLI 配置中引用 `skills/` 目录下的 skill
3. 重启 Kimi Code CLI 使 skill 生效

### 手动复制

也可以直接复制单个 skill 目录到 Kimi 的 skill 配置目录：

```bash
# 示例：复制 daily-time-block skill
cp -r skills/daily-time-block ~/.config/agents/skills/
```

复制后重启 Kimi Code CLI。

## Skill 开发规范

- 每个 skill 一个目录，目录名使用 kebab-case
- 目录下必须包含 `SKILL.md` 作为主入口
- 辅助脚本放在 `scripts/` 子目录
- 模板资源放在 `assets/` 子目录
- `SKILL.md` 顶部包含 YAML frontmatter：
  ```yaml
  ---
  name: skill-name
  description: 简短的 skill 描述
  ---
  ```

## 新增 Skill 流程

1. 在 `skills/` 下新建目录（kebab-case 命名）
2. 编写 `SKILL.md` 和相关辅助文件
3. 本地测试验证
4. 更新本 README 的 Skills 表格
5. 提交到 git

## Git 规范

- 分支：功能分支开发，合并后删除
- 提交：简洁描述变更内容
