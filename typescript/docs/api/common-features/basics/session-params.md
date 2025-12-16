# Class: CreateSessionParams

CreateSessionParams provides a way to configure the parameters for creating a new session
in the AgentBay cloud environment.

## Implements

- ``CreateSessionParamsConfig``

## Table of contents


### Properties

- [browserContext](#browsercontext)
- [enableBrowserReplay](#enablebrowserreplay)
- [extraConfigs](#extraconfigs)
- [framework](#framework)
- [imageId](#imageid)
- [policyId](#policyid)

### Methods

- [addContextSync](#addcontextsync)
- [addContextSyncConfig](#addcontextsyncconfig)
- [fromJSON](#fromjson)
- [toJSON](#tojson)
- [withBrowserContext](#withbrowsercontext)
- [withContextSync](#withcontextsync)
- [withEnableBrowserReplay](#withenablebrowserreplay)
- [withEnableRecord](#withenablerecord)
- [withExtraConfigs](#withextraconfigs)
- [withFramework](#withframework)
- [withImageId](#withimageid)
- [withIsVpc](#withisvpc)
- [withLabels](#withlabels)
- [withPolicyId](#withpolicyid)

## Properties

```typescript
contextSync: [`ContextSync`](context-sync.md)[]
isVpc: `boolean`
labels: `Record`<`string`, `string`>
```


### browserContext

• `Optional` **browserContext**: ``BrowserContext``

Optional configuration for browser data synchronization.

#### Implementation of

`CreateSessionParamsConfig`.`browserContext`

___

#### Implementation of

`CreateSessionParamsConfig`.`contextSync`

___

### enableBrowserReplay

• `Optional` **enableBrowserReplay**: `boolean`

Whether to enable browser recording for the session. Defaults to undefined (use default behavior, enabled by default).

#### Implementation of

`CreateSessionParamsConfig`.`enableBrowserReplay`

___

### extraConfigs

• `Optional` **extraConfigs**: ``ExtraConfigs``

Extra configuration settings for different session types (e.g., mobile)

#### Implementation of

`CreateSessionParamsConfig`.`extraConfigs`

___

### framework

• `Optional` **framework**: `string`

Framework name for SDK statistics tracking

#### Implementation of

`CreateSessionParamsConfig`.`framework`

___

### imageId

• `Optional` **imageId**: `string`

Image ID to use for the session.

#### Implementation of

`CreateSessionParamsConfig`.`imageId`

___

#### Implementation of

`CreateSessionParamsConfig`.`isVpc`

___

#### Implementation of

`CreateSessionParamsConfig`.`labels`

___

### policyId

• `Optional` **policyId**: `string`

Policy id to apply when creating the session.

#### Implementation of

`CreateSessionParamsConfig`.`policyId`

## Methods

### addContextSync

▸ **addContextSync**(`contextId`, `path`, `policy?`): [`CreateSessionParams`](session-params.md)

AddContextSync adds a context sync configuration to the session parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `contextId` | `string` |
| `path` | `string` |
| `policy?` | ``SyncPolicy`` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### addContextSyncConfig

▸ **addContextSyncConfig**(`contextSync`): [`CreateSessionParams`](session-params.md)

AddContextSyncConfig adds a pre-configured context sync to the session parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `contextSync` | [`ContextSync`](context-sync.md) |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### fromJSON

▸ **fromJSON**(`config`): [`CreateSessionParams`](session-params.md)

Create from plain object

#### Parameters

| Name | Type |
| :------ | :------ |
| `config` | ``CreateSessionParamsConfig`` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### toJSON

▸ **toJSON**(): ``CreateSessionParamsConfig``

Convert to plain object for JSON serialization

#### Returns

``CreateSessionParamsConfig``

___

### withBrowserContext

▸ **withBrowserContext**(`browserContext`): [`CreateSessionParams`](session-params.md)

WithBrowserContext sets the browser context for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `browserContext` | ``BrowserContext`` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withContextSync

▸ **withContextSync**(`contextSyncs`): [`CreateSessionParams`](session-params.md)

WithContextSync sets the context sync configurations for the session parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `contextSyncs` | [`ContextSync`](context-sync.md)[] |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withEnableBrowserReplay

▸ **withEnableBrowserReplay**(`enableBrowserReplay`): [`CreateSessionParams`](session-params.md)

WithenableBrowserReplay sets the browser recording flag for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `enableBrowserReplay` | `boolean` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withEnableRecord

▸ **withEnableRecord**(`enableRecord`): [`CreateSessionParams`](session-params.md)

Alias for withEnableBrowserReplay for backward compatibility.

#### Parameters

| Name | Type |
| :------ | :------ |
| `enableRecord` | `boolean` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withExtraConfigs

▸ **withExtraConfigs**(`extraConfigs`): [`CreateSessionParams`](session-params.md)

WithExtraConfigs sets the extra configurations for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `extraConfigs` | ``ExtraConfigs`` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withFramework

▸ **withFramework**(`framework`): [`CreateSessionParams`](session-params.md)

WithFramework sets the framework name for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `framework` | `string` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withImageId

▸ **withImageId**(`imageId`): [`CreateSessionParams`](session-params.md)

WithImageId sets the image ID for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `imageId` | `string` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withIsVpc

▸ **withIsVpc**(`isVpc`): [`CreateSessionParams`](session-params.md)

WithIsVpc sets the VPC flag for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `isVpc` | `boolean` |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withLabels

▸ **withLabels**(`labels`): [`CreateSessionParams`](session-params.md)

WithLabels sets the labels for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `labels` | `Record`\<`string`, `string`\> |

#### Returns

[`CreateSessionParams`](session-params.md)

___

### withPolicyId

▸ **withPolicyId**(`policyId`): [`CreateSessionParams`](session-params.md)

WithPolicyId sets the policy id for the session parameters and returns the updated parameters.

#### Parameters

| Name | Type |
| :------ | :------ |
| `policyId` | `string` |

#### Returns

[`CreateSessionParams`](session-params.md)
