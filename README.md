# 喵琴师 · CatKeys

一个不依赖任何框架、不依赖构建工具的单文件 Web 钢琴节奏跟弹游戏，主角是开源动效吉祥物 **哈士喵**。双击 `index.html` 即玩，可离线运行。

在原「网页钢琴入门」基础上新增三块系统：

- **成就系统**：10 项挑战，进度存本机，结算/通关时自动解锁并提示
- **体力系统**：每局消耗 1 点体力，每 60 秒自动恢复 1 点，每日游玩上限 20 局，离线按时间戳补算
- **转发得体力**：分享链接并回到页面停留 ≥5 秒即可领取体力，每日最多 3 次、两次间隔 ≥15 秒

> **仓库**：<https://github.com/604665656/catkeys>
> **开发看板**：<https://github.com/users/604665656/projects/10>
> **B 站 Toy**：提交审核中（`catkeys-toy.zip` + `cover_1200x900.png`）
>
> 如需自行改名，改 `index.html` 里的 `<title>`、`品牌`、`哈士喵` 文案，并重新跑 `tools/build_catkeys.py` 即可。

---

## 特性

### 原版玩法（保留）
- 65 首分级公有领域曲目，Lv.1~Lv.10 + 演奏级，跟弹打分给 ★，熟练度逐级解锁
- 4 种模式：自由弹 / 跟弹打分 / 🎯 演练 / 🐱 跳跃（哈士喵死亡跑酷）
- 自适应键位：手机 13 键、平板 25/37 键、电脑 61 键；📐 横竖屏方向锁定
- 真钢采样（联网懒加载，CC BY 3.0）+ 离线合成双音色，WebAudio 混响
- 🎨 自定义画面：6 套主题、配色、背景图、音符彩虹模式、特效开关
- 哈士喵开源 2D 动效：闭式阻尼弹簧 + 分部位骨骼 + 6 块刚体部件，双脚零变换永远站着

### 新增：成就系统（10 项）

| 图标 | 名称 | 解锁条件 |
|---|---|---|
| 🐾 | 初遇 | 完成第一首跟弹曲目 |
| 🔗 | 全连 | 单局零 MISS（≥20 音符） |
| 💎 | 完美主义 | 单局准确率 100%（全 PERFECT） |
| 🔥 | 百连 | 单局最大连击 ≥ 100 |
| ⭐ | 三星演奏家 | 任意曲目拿到 ★★★ |
| 🎼 | 钢琴大师 | 累计 ★ 达到 30 |
| 🏛️ | 演奏级 | 解锁 Lv.10 演奏级 |
| 🐱 | 哈士喵通关 | 跳跃模式整首零踩空 CLEAR |
| 👑 | 跳跃王者 | 跳跃最远连跳 ≥ 50 |
| ⚡ | 极速指法 | ≥120% 速度下完成一首（准确率≥55%） |

点击右上角 **🏆 成就** 查看全部进度（锁定/已达成）。进度与考级熟练度一起存本机 `localStorage`（`piano_grade_v1` 内的 `ach` 字段）。

### 新增：体力与转发系统

- **体力上限 5 点**，每 **60 秒** 恢复 1 点；**每日游玩上限 20 局**；离线按时间戳补算恢复量
- 进入「跟弹打分 / 🐱 跳跃」会消耗 1 点体力；演练 / 自由弹不消耗
- 体力为 0 时，右下角开始键显示「⚡ 体力不足」，需先分享回体力
- **转发得体力**：点右上角 **📤 分享得体力** → 复制分享链接 → 去分享给好友 → 回到本页停留 **≥5 秒** 自动领取 +1 体力
- 限流：每日最多 **3 次** 分享领取，两次间隔 **≥15 秒**，时间戳去重（均存本机 `catkeys_stamina_v1`）

> 单文件离线版用「复制链接 + 回到页面」模拟分享回流；若接入 B 站 Toy 等宿主，把 `doShare()` / `onReturn()` 换成宿主 SDK 的分享回调即可，逻辑不变。

### 平台层（Toy / 微信小游戏适配点）
- 体力、分享、成就、每日上限均为纯前端实现，不依赖后端
- 分享回流当前用 `visibilitychange` + `focus` 检测「回到页面 ≥5 秒」；真实宿主可替换为 SDK `onShareSuccess` 回调
- 结算/解锁数据走本机 `localStorage`；需要云存档时按宿主 SDK 的 `getCloudStorage` / `setCloudStorage` 合并即可

---

## 目录

```
catkeys/
├── index.html          # GitHub 单文件版（~1.1MB，内嵌哈士喵精灵，双击即玩 / 可离线）
├── dist/               # TOY 上架包（index.html ≤1MB + assets/ 外置图，见下方「打包上架 TOY」）
│   ├── index.html
│   └── assets/         # 哈士喵精灵与三视图等 10 张外置图
├── catkeys-toy.zip     # TOY 上架包（dist 打包，根目录含 index.html + assets/）
├── cover_1200x900.png  # TOY 4:3 封面（深空蓝主题 + 哈士喵）
├── tools/
│   ├── build_catkeys.py  # 由原始「网页钢琴入门.html」生成改名后的 index.html
│   └── build_dist.py     # 把内嵌 base64 图外置，产出 ≤1MB 的 dist/
├── README.md
├── LICENSE
└── .gitignore
```

`index.html` 与 `dist/index.html` 都是构建产物：本地改完原始 HTML 后跑 `tools/build_catkeys.py`，再跑 `tools/build_dist.py` 即可同步两份。

---

## 快速开始

```bash
# 方式一：直接双击 index.html（部分浏览器对 file:// 下的音频采样有限制，推荐方式二）

# 方式二：本地 http 服务，手机也能测
cd catkeys
python -m http.server 8080
# 浏览器打开 http://<本机IP>:8080/index.html
```

即使音频真的读不出来，页面也会给出「重试 / 静音试玩」按钮，不会卡在加载页。

---

## 打包上架 GitHub

```bash
cd catkeys
git init
git add -A
git commit -m "喵琴师 · CatKeys：单文件钢琴节奏跟弹 + 成就/体力/转发"
# 把下面的 <你的账号> 换成你的 GitHub 用户名
git remote add origin https://github.com/<你的账号>/catkeys.git
git branch -M main
git push -u origin main
```

> 本仓库已推送至 `604665656/catkeys`（`main` 分支）。如需推到自己的账号，把 `origin` 换成你的仓库地址即可。

---

## 打包上架 TOY（B 站 Toy / 同类小游戏平台）

TOY 有两条硬限制，直接决定产物形态：

- **`index.html` 解压后 ≤ 1MB** → 单文件版内嵌了哈士喵精灵（约 600KB base64），会超 1MB，必须用 `dist/` 分包版
- **不允许内联大体积脚本/样式/图片** → `dist/` 已把 10 张图外置到 `assets/`，`index.html` 仅约 210KB

```bash
python tools/build_dist.py      # 产出 dist/index.html + dist/assets/
# 把 dist/ 内 index.html 与 assets/ 放在同一层压成 zip，根目录必须含 index.html
# 直接投 https://www.bilibili.com/toy/publish/
```

平台层会自动检测宿主：存在 `window.toy` → 云端模式（排行榜/云存档/分享）；否则 → 单机模式，功能自动降级为本地存档与本地体力。

### Toy 合规要点（改动前务必看）
来源：《Toy 开发者 FAQ》。以下几条约束了本项目的实现：

| 约束 | 本项目做法 |
|---|---|
| 不允许用户自建昵称 / 头像 | 哈士喵无自由昵称输入框；昵称走宿主 SDK（如有），否则用系统预置 |
| 禁止 UGC 自由文本输入 | 无自由输入框；弹幕/留言类功能默认关闭 |
| 入口 `index.html` ≤ 1MB | `dist/` 分包版 ~210KB，图外置 |
| 文件包 ≤ 50MB，zip 根目录必须含 index.html | 上架包 ~1MB，根目录直接放 `index.html` + `assets/` |
| 不得跳转站外、不得放广告、不得第三方登录 | 分享仅复制本页链接，不引外链 |
| 必须保留免交互即可见的内容 | 游戏本体无需关注/分享即可完整游玩 |

---

## 版权与授权

- **代码**：MIT，见 `LICENSE`
- **角色形象**：哈士喵为按需求全新绘制的 SVG / 位图矢量插画，未使用任何原始图片素材
- **钢琴采样**：Salamander Grand Piano v3 © Alexander Holm，CC BY 3.0（<https://github.com/sfzinstruments/SalamanderGrandPiano>），联网懒加载并保留署名
- **内置曲目**：65 首均为公有领域旋律的简化单旋律编配，仅作节奏与键位练习用，非考级教材原谱
- **健康游戏忠告**：抵制不良游戏，拒绝盗版游戏。注意自我保护，谨防受骗上当。适度游戏益脑，沉迷游戏伤身。合理安排时间，享受健康生活。
