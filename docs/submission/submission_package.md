# Paper 2 投稿材料包（用户人工投稿用）— 2026-10-03

> 目标刊：**IET Science, Measurement & Technology**（主投，SCIE，订阅型免版面费）
> 备投链：COMPEL → CES TEMS → Russian Electrical Engineering（Pleiades）
> 状态：内容零阻塞，以下材料备齐即可在 ScholarOne（mc.manuscriptcentral.com/iet-smt，
> 需浏览器过 Cloudflare）人工注册+提交。

## 0. 文件清单

| 文件 | 位置 | 用途 |
|---|---|---|
| main.pdf（6 页 A4，行号版） | `sci/paper02_torque/manuscript/main.pdf` | 主稿（Main Document 上传） |
| main.tex + figures/*.pdf | `sci/paper02_torque/manuscript/` | 源文件（如需 LaTeX 源上传） |
| 复现数据包 | github.com/daheix/paper02-torque-arbitration（tag v0.3.0） | 数据可用性声明指向 |
| 本文件 + cover letter 正文 | 本目录 | 提交系统逐栏填写参照 |

## 1. 作者信息（逐栏照抄）

- 姓名：**Shouchun Wu**（拼音姓 Wu，名 Shouchun；ScholarOne 姓/名分栏时 Family=Wu, Given=Shouchun）
- 邮箱：**daheix@163.com**
- ORCID：**0009-0007-3577-2552**
- 单位：**Independent Researcher**（独立研究者；Country=China）
- 作者数：1（单作者，无共同作者）

## 2. Cover Letter（全文可粘）

Dear Editor,

We are pleased to submit our manuscript entitled "Root Causes of Finite-Element
Torque Formulation Discrepancies and a Reference-Free Referee Criterion" for
consideration in IET Science, Measurement & Technology.

Finite-element torque values routinely disagree across the three classical
formulations on identical meshes, and practitioners have no principled
tie-breaker. Using a four-level mesh-refinement sequence (7,489-187,600 nodes)
on a frozen surface-PM model with a standalone open FE solver, we show that
(1) the integral formulations are structurally stable - the virtual-work slope,
co-energy amplitude, and formula torque agree to a constant 1.15% across all
refinements; (2) the Maxwell stress ring is pathological - its value wanders
15-43% across levels and up to 77% between evaluation radii on the same mesh,
because a point-sampled BnBt integral over piecewise-constant fields carries no
convergence meaning; and (3) these observations yield a one-sentence, reference-
free referee criterion - admit the mean torque when the integral trio is
self-consistent within 1.5%, reject the stress ring when its same-mesh
three-radius band exceeds 5% - which passed a blind eccentric-rotor hold-out
(0/10/20% of the air gap) with zero re-tuning. An analytic ladder (0.92% and
0.66% error) anchors the solver, and a negative result on the energy-balance
identity probe is reported explicitly.

We believe this fits the scope of IET SMT on measurement and computation
methodology for electrical machines. All data, drivers, and analysis scripts
are released as a tagged replication package (v0.3.0,
github.com/daheix/paper02-torque-arbitration) so that reviewers can verify
every number in the paper.

This manuscript is original, has not been published previously, and is not
under consideration elsewhere. The sole author has approved the submission.

Sincerely,
Shouchun Wu (daheix@163.com, ORCID 0009-0007-3577-2552)

## 3. Highlights（逐条粘贴）

1. Four-level mesh sequence (7.5k-187.6k nodes) traces FEM torque discrepancy
   to its discrete origin.
2. Integral formulations agree to a constant 1.15%; the Maxwell stress ring
   wanders 15-43% across meshes and 77% within one mesh.
3. A reference-free referee criterion (trio ≤1.5%; ring band >5%) is frozen
   and validated blind on an eccentric hold-out.
4. Energy-balance identity residual is shown to be non-discriminative - a
   negative result reported explicitly.
5. Full replication package (v0.3.0) released for reviewer verification.

## 4. 关键词（提交系统 Keywords 栏）

finite element analysis; torque computation; Maxwell stress tensor; virtual
work; mesh refinement; verification and validation; electrical machines;
open-source simulation

## 5. 数据声明（Data Availability 栏可粘）

All data, scripts, and frozen releases supporting this study are openly
available at https://github.com/daheix/paper02-torque-arbitration (tags
v0.1.0-v0.3.0; CITATION.cff included). Series index:
https://github.com/daheix/daheix.

## 6. 资金/利益冲突声明

- Funding: none（无资助）
- Conflicts of interest: none
- 如系统要求 AI 使用披露：论文文本由 AI 辅助起草（LLM），作者全程验证数据与结论，
  复现包可独立核查全部数值。（Wiley 政策要求披露 AI 写作工具使用——如实勾选/填写）

## 7. 提交步骤备忘（ScholarOne）

1. 浏览器打开 mc.manuscriptcentral.com/iet-smt → "Create Account"（用 daheix@163.com，
   收激活邮件激活）
2. 登录 → Author Center → "Submit a Manuscript" → 选 Regular Paper
3. 逐栏粘贴 §1-§5 内容；Main Document 传 main.pdf；如需源文件再传 main.tex+图
4. 复现包链接填在 Data Availability / Footnotes
5. 确认 PDF 构建无乱码 → Approve Submission
6. 收到提交确认邮件（Manuscript ID）→ 记入 sci/pipeline/01_已投稿记录.md

## 8. 备投（如 IET SMT 拒稿）

| 顺位 | 刊 | 系统 | 备注 |
|---|---|---|---|
| 1 | COMPEL (Emerald) | ScholarOne | 订阅型免费；scope 计算电磁学完美对口 |
| 2 | CES TEMS | ScholarOne (mc03/tems) | 免费 OA；电机对口 |
| 3 | Russian Electrical Eng. (Pleiades) | 官网/email | 订阅型；俄刊兜底 |

## 9. 预判审稿人 5 条质疑与回复预案（2026-10-04 复审补）

| # | 质疑 | 回复要点 |
|---|---|---|
| Q1 | 单模型单工况，结论普适性？ | 设计如此：最小仪器固定除 formulation 外一切变量（Scope 段明示）；跨拓扑/高阶元是 re-calibration 问题非逻辑问题；判据只需 published 量，跨求解器复制列为 future work |
| Q2 | C1/C2 阈值 1.5%/5% 任意？ | 由 §4 观测 a posteriori 冻结、hold-out 前不再调（Methods 明示）；hold-out 零重调通过；阈值按元件阶数重标定已写入 Threats |
| Q3 | 负结果（能量平衡恒零）价值？ | 方法论澄清：该 probe 在共享离散场的实现中恒等成立，任何用它筛解的文献结论都需重审；明确 delineate 何者可替代 |
| Q4 | stress ring 病理已知（folklore），增量何在？ | 已知的是定性敏感；本文给出定量签名（15–43% 跨水平/77% 同网格）+离散机制（P1 分片常数 BnBt 逐元跳变）+可操作判据——folklore→referee criterion 是增量 |
| Q5 | P1 求解器自研，可信度？ | 双重锚：解析阶梯（0.917%/0.661%，阈 1%/3%）+生产 Gmsh–GetDP 链交叉验证（Bn 0.7588 vs 0.7585 T）；复现包 v0.3.0 全量可核 |

## 10. 推荐审稿人 3 名（真实学者；邮箱投稿时在系统/主页核实补全）

| 学者 | 机构 | 理由 |
|---|---|---|
| C. Geuzaine | University of Liège | Gmsh 一作；网格生成与 FE 数值方法论权威，可判 verify 方法学 |
| J.A. Malagoli | UFU (Brazil) | Gmsh/GetDP 电机转矩优化直接先例作者（ITEES 2021），熟悉开源栈误差特性 |
| Z. Goryca | Lublin University of Technology | PM 电机 FE 转矩/齿槽转矩实测对比作者（Energies 2020），电机测量口径对口 |

回避列表：无。
