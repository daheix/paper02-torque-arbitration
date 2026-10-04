# Paper02 模拟审稿报告（按最新 sci-paper-writing 技能复审，2026-10-04）

- 稿件: manuscript/main.tex（6 页，pdflatex 两遍零 error 零未解析引用）
- 背景: 用户指示"paper02 按照最新的技能重新审核一遍"——以 paper03 建立的 S5/S6 纪律（数字核验脚本/模拟审稿/查重自查/L2 五件套/检查清单 12 项）回审本稿
- 目标刊: IET SMT（电机，体裁匹配 methodology+应用）

## 发现并已真改（本轮）

| # | 问题 | 处置 | 状态 |
|---|---|---|---|
| A1 | 摘要 ~300 词超 250 上限；收尾句无量化 | 压缩至 **223 词**，收尾句改量化（"all verdicts survive the blind hold-out unchanged, thresholds frozen a priori"） | ✅ |
| A2 | `cogg2022` 引用未定义（Related work 引用但 bib 缺条目——历史遗留） | Crossref 验证 doi:10.3390/en13226108（Goryca et al., Energies 13(22):6108, 2020）补 `cogg2020` 条目+改正文 key；重编译 0 undefined | ✅ |
| A3 | `fig:band` 定义 label 但正文从未引用 | RQ2 段补引用（Figure~\ref{fig:band}） | ✅ |
| A4 | fig:trio caption 非结论式（仅描述坐标） | 改结论式 caption（"criterion discriminates in the direction theory predicts, with zero re-tuning"） | ✅ |
| A5 | `10\textsuperscript{$-$6}` 丑写法 | 改数学模式 $\sim$10$^{-6}$ | ✅ |
| A6 | 查重自查未做 | 8-gram 对照 paper03：**0.00%**（0/1611）；paper01 无 tex 稿（EMSE 在审） | ✅ |

## 审核通过项（无需改）

- C-C-C 引言结构 ✅；贡献 3 条粗体名词短语 ✅；无 AI 填充词 ✅
- Threats to Validity 四段齐全（Scope/Construct/Internal/Statistical）✅
- 占位符 0 ✅；负结果明确报告（energy-balance 恒零）✅
- 图 fig:conv caption 结论式 ✅；6→7 条引用全部 DOI 可查 ✅

## 按新技能标准的差距（待办，非本稿文字问题）

| # | 项 | 差距 | 建议 |
|---|---|---|---|
| G1 | 数字核验脚本 | 无 verify_manuscript_numbers 式逐项断言（正文数字 vs 冻结 CSV） | 投稿前补建（数据侧 CSV 在 repo tags v0.1–v0.3） |
| G2 | L2 复现包 | 缺 Dockerfile+requirements.lock+Makefile+expected_results 五件套（仅 README+requirements.txt） | 若 IET SMT 审稿人要求再升级（L1 兜底已就绪），或按 paper03 模式补齐 |
| G3 | 投稿包 | submission_package.md 内容待按 12 项清单刷新（cover letter/highlights/预判质疑/审稿人 3 名） | 投稿前按 paper03 docs/submission/ 模板重建 |
| G4 | 合规声明 | 无 AI 声明/COI 文件 | 投稿系统填报时按 IET 政策补 |

## 结论

**文字层审核通过**：6 处真改后编译干净、摘要达标、查重 0.00%。G1–G4 为投稿前工程待办（数据/复现/投稿包层），不阻塞稿件文字定稿。Paper02 维持"待人工投稿 IET SMT"状态，建议用户先投（G1/G3 可在等待审稿期间并行补齐）。
