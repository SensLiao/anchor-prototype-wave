<div align="right"><a href="README.md">English</a></div>

<p align="center"><img src="docs/hero.png" alt="anchor-prototype-wave banner" width="100%"></p>

<p align="center"><b>锁定一个视觉锚点，并行铺开多张高保真页面，并逐张把关。</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-f472b6?style=flat-square" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/version-3.0.0-f472b6?style=flat-square" alt="Version 3.0.0">
  <img src="https://img.shields.io/badge/status-stable-f472b6?style=flat-square" alt="Status: stable">
  <img src="https://img.shields.io/badge/pipeline-14_stages-f472b6?style=flat-square" alt="14-stage pipeline">
  <img src="https://img.shields.io/badge/Python-3-3776ab?style=flat-square" alt="Python 3">
  <img src="https://img.shields.io/badge/License-MIT-2dd4bf?style=flat-square" alt="License: MIT">
</p>

## 概述

`anchor-prototype-wave` 是一个 Claude Code skill，它把一个锁定的视觉锚点加上一份页面清单，在单次运行中产出一整波高保真 HTML 原型。它会并行铺开逐个 surface 的子代理（subagent），再用确定性校验器、一个 LLM 评分器以及跨模型（Codex）复审对每个 surface 把关——在汇总成一份总画廊（master gallery）之前，先对失败项进行重试。它面向那些需要大量页面、且这些页面都要忠实于同一个参考的设计师与工程师，免去逐张检查漂移或残留样板代码的工作。

**关键术语**（面向零背景读者）：

- **Surface（页面单元）**——原型中的一屏/一页。
- **Anchor（锚点）**——所有 surface 都必须匹配的、被锁定的视觉参考。
- **Scaffold leak（脚手架泄漏）**——溜进成品页面里的占位内容或样板代码。

## ✨ 亮点

- **一条 14 阶段流水线（Stage 0–13）**，在单次运行中把一波原型从锁定锚点带到汇总画廊。
- **并行的 surface 子代理**，以 ≤10 为一批，超出则自动拆分，因此大页面清单无需手工分块即可铺开。
- **一个确定性校验器**，包含 9 项检查，聚合成 5 道硬性闸门（hard gate）——这是每个 surface 都必须通过、与 LLM 无关的客观下限。
- **6 个带权重的软性维度（soft dimension）**，配有随成熟度调整的分数下限，最终归结为四种判定：`PASS_9PLUS`、`FIX_NEEDED`、`REDO`、`ESCALATE_HUMAN`。
- **一个失败即修复（fix-on-fail）循环**，每个 surface 最多重试 3 次，让失败在原地被修复，而不是被悄悄放行。
- **跨模型复审**覆盖全部失败项，外加对通过项的 15% 抽样，完全与具体模型无关——具体模型由环境变量选择。
- **12 种 surface 形态类型与 10 条枚举的反模式（anti-pattern）**，为评分词汇提供锚定，并捕捉 scaffold leak。

## 🏗 工作原理

整波原型作为一条确定性流程运行：

1. **锁定锚点**，并把页面清单展开为一个个独立的 surface。
2. **铺开**并行的逐 surface 子代理（以 ≤10 为一批，超出则自动拆分）。
3. **校验**每个 surface，通过 9 项确定性检查，聚合成 5 道硬性闸门。
4. **评分**6 个带权重的软性维度，配随成熟度调整的下限，产出四种判定之一。
5. **失败即修复**，每个 surface 最多重试 3 次。
6. **跨模型复审**每个失败项，外加对通过项的 15% 抽样。
7. **汇总**存活下来的 surface，形成一份总画廊。

## 🔗 与 prototyping-ui-directions 的配合

[`prototyping-ui-directions`](https://github.com/SensLiao/prototyping-ui-directions) 是它的上游对应部分：它从一个模糊的想法和几张参考图中探索出设计方向。随后，`anchor-prototype-wave` 把选定的方向作为锁定锚点，据此批量产出高保真页面。

## 🧰 技术栈

- **Skill 规范**——单个 Markdown skill 定义。
- **脚本**——两个 Python 3 标准库脚本（约 640 行，无第三方依赖）。
- **配套 skill**——`codex-dispatch`（用于跨模型复审）。

## 🚀 快速上手

将该 skill 安装到单个项目，或全局安装以供所有项目使用：

```bash
# 项目级安装
git clone https://github.com/SensLiao/anchor-prototype-wave .claude/skills/anchor-prototype-wave

# ……或全局安装
git clone https://github.com/SensLiao/anchor-prototype-wave ~/.claude/skills/anchor-prototype-wave
```

随后以对话方式调用它，给它一个锚点和一份页面清单。两个 Python 脚本也可以直接运行——例如，校验单个 surface：

```bash
python validate_surface.py <surface-dir>
```

## 📌 项目状态

**v3.0.0，稳定版（stable）。**

## 📄 许可证

基于 MIT 许可证发布——参见 [`LICENSE`](LICENSE)。

<p align="center"><sub>Built by <a href="https://github.com/SensLiao">Ruixuan "Sens" Liao</a> · USYD Advanced Computing (Honours)</sub></p>
