# Legacy Frontend Analysis Templates

Use these templates when the user asks to document a flow, compare variants, or prepare a future agent to modify a legacy frontend safely.

## Flow Analysis Document

````markdown
# <Flow Name> 分析

## 入口和范围
- 入口：
- 代表样例：
- 不在本次范围：

## 正常流程
```text
entry
 -> route guard / config
 -> page wrapper
 -> main component
 -> state/auth checks
 -> API / user action
 -> completion / navigation
```

## 目标流程或变体流程
```text
entry
 -> changed branch
 -> side effects
 -> final state
```

## 组成关系
| 层级 | 文件/模块 | 职责 | 备注 |
|---|---|---|---|
| route |  |  |  |
| page |  |  |  |
| component |  |  |  |
| mixin/composable/hook |  |  |  |
| store/service |  |  |  |

## 调用关系
```text
user action
 -> handler
 -> shared helper / mixin method
 -> API / store / navigation
```

## 隐式契约
| 依赖 | 来源 | 使用位置 | 风险 |
|---|---|---|---|
| this.xxx | page/mixin/store/prop |  |  |
| global callback | store/event bus |  |  |
| module variable | module scope |  |  |
| storage/query | local/session/query |  |  |

## 接口、埋点和跳转
| 类型 | 入口 | 参数来源 | 风险 |
|---|---|---|---|
| API |  |  |  |
| analytics |  |  |  |
| navigation/deep link |  |  |  |

## 公共方法影响面
| 调用方类型 | 调用入口 | 成功分支 | 空数据/异常分支 | 是否允许阻塞 | 兜底归属 |
|---|---|---|---|---|---|
| 展示型 |  |  |  |  |  |
| 点击型 |  |  |  |  |  |
| 提交/支付型 |  |  |  |  |  |

## 降级和阻断边界
- 非核心依赖：
- 允许阻断的强依赖：
- 失败时用户可见行为：
- 重试或继续路径：

## 常见改动定位表
| 要改什么 | 优先看哪里 | 相关风险 |
|---|---|---|
| 文案/配置 |  |  |
| 登录条件 |  |  |
| 提交/保存 |  |  |
| 公共 helper |  |  |
| 第三方 SDK |  |  |
| 支付/跳转 |  |  |
| 埋点 |  |  |

## 风险清单
- 

## 验证清单
- 

## 仍需确认
- 
````

## Variant Difference Document

````markdown
# <Version or Feature> 异同分析

## 背景
<Why this variant exists.>

## 复用逻辑
- 

## 差异点
| 差异 | 普通流程 | 当前变体 | 影响 |
|---|---|---|---|
| 入口 |  |  |  |
| 登录/鉴权 |  |  |  |
| 状态保存 |  |  |  |
| 结束/跳转 |  |  |  |

## 兼容影响
- 对已有页面：
- 对共享模块：
- 对数据/缓存：
- 对埋点/归因：
- 对空数据/异常兜底：

## 风险
- 

## 验证清单
- 
````

## Representative Search Checklist

Use this when the user asks to find the page/module that implements a behavior.

- Search for route comments, route names, and page marks.
- Search for unique query keys, props, constants, API names, and feature flags.
- Search for behavior toggles such as `requiredLogin: false`, `noRequiredLogin`, special redirect targets, or unique status transitions.
- Search for remote-config keys, dictionary values, prototype/design notes, and external-entry query parameters.
- Compare neighboring variants instead of stopping at the first match.
- Verify uniqueness by searching the signature across the repo.
- Confirm the full closure: entry -> state/auth -> business action -> completion/jump.

## Mixin/Implicit Dependency Checklist

- List all direct mixins/composables/hooks.
- Check nested mixins imported by those modules.
- Search each important method name across the page and mixins.
- Build a `this.*` dependency table:
  - field name
  - defined by page, prop, data, computed, store, mixin, lifecycle, or ref
  - read/write sites
  - same-name override risk
- Check lifecycle hooks that register timers, event listeners, store callbacks, or global callbacks.
- Check cleanup on route leave/destroy/unmount.
- Check module-scope variables and whether route changes reset them.

## Shared Helper Impact Checklist

Use this before changing a helper used by multiple pages or components.

- Classify callers by behavior: display-only, user-click, submit/payment, background initialization, route guard.
- For each caller, compare success, empty data, API failure, timeout, and thrown-error branches.
- Confirm every Promise or callback path settles or invokes the caller's continuation intentionally.
- Keep query/read helpers free of navigation side effects unless the helper name and contract clearly say it jumps.
- Preserve caller-owned analytics, attribution, fallback keys, and target route/deep-link parameters in error paths.
- If the old helper mixes callback and Promise styles, verify both styles after the change.

## Third-Party SDK Replacement Checklist

- Identify the adapter layer closest to the old SDK.
- Preserve caller-facing props, events, return fields, and error semantics when possible.
- Move vendor-specific loading, key selection, parsing, and retry behavior into a helper or adapter.
- Search and remove unused old SDK imports, scripts, package dependencies, and stale comments.
- Document the new adapter location, key/config ownership, and known fallback behavior.
