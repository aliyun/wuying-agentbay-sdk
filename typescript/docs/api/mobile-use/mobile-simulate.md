# Class: MobileSimulateService

Provides methods to manage persistent mobile dev info and sync to the mobile device.

## Table of contents


### Methods

- [hasMobileInfo](#hasmobileinfo)
- [setSimulateContextId](#setsimulatecontextid)
- [setSimulateEnable](#setsimulateenable)
- [setSimulateMode](#setsimulatemode)
- [uploadMobileInfo](#uploadmobileinfo)

## Methods

### hasMobileInfo

▸ **hasMobileInfo**(`contextSync`): `Promise`\<`boolean`\>

Check if the mobile dev info file exists in one context sync. (Only for user provided context sync)

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `contextSync` | [`ContextSync`](../common-features/basics/context-sync.md) | The context sync to check. |

#### Returns

`Promise`\<`boolean`\>

True if the mobile dev info file exists, False otherwise.

**`Throws`**

Error if context_sync is not provided or context_sync.context_id or context_sync.path is not provided.

**`Remarks`**

This method can only be used when mobile simulate context sync is managed by user side. For internal mobile simulate
context sync, this method will not work.

___

### setSimulateContextId

▸ **setSimulateContextId**(`contextId`): `void`

Set a previously saved simulate context id. Please make sure the context id is provided by MobileSimulateService
but not user side created context.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `contextId` | `string` | The context ID of the previously saved mobile simulate context. |

#### Returns

`void`

___

### setSimulateEnable

▸ **setSimulateEnable**(`enable`): `void`

Set the simulate enable flag.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `enable` | `boolean` | The simulate feature enable flag. |

#### Returns

`void`

___

### setSimulateMode

▸ **setSimulateMode**(`mode`): `void`

Set the simulate mode.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `mode` | ``MobileSimulateMode`` | The simulate mode. - PropertiesOnly: Simulate only device properties. - SensorsOnly: Simulate only device sensors. - PackagesOnly: Simulate only installed packages. - ServicesOnly: Simulate only system services. - All: Simulate all aspects of the device. |

#### Returns

`void`

___

### uploadMobileInfo

▸ **uploadMobileInfo**(`mobileDevInfoContent`, `contextSync?`): `Promise`\<``MobileSimulateUploadResult``\>

Upload the mobile simulate dev info.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `mobileDevInfoContent` | `string` | The mobile simulate dev info content to upload. |
| `contextSync?` | [`ContextSync`](../common-features/basics/context-sync.md) | Optional - If not provided, a new context sync will be created for the mobile simulate service and this context id will be returned by the MobileSimulateUploadResult. User can use this context id to do persistent mobile simulate across sessions. - If provided, the mobile simulate dev info will be uploaded to the context sync in a specific path. |

#### Returns

`Promise`\<``MobileSimulateUploadResult``\>

The result of the upload operation.

**`Throws`**

Error if mobile_dev_info_content is not provided or not a valid JSON string.

**`Throws`**

Error if context_sync is provided but context_sync.context_id is not provided.

**`Remarks`**

If context_sync is not provided, a new context sync will be created for the mobile simulate.
If context_sync is provided, the mobile simulate dev info will be uploaded to the context sync.
If the mobile simulate dev info already exists in the context sync, the context sync will be updated.
If the mobile simulate dev info does not exist in the context sync, the context sync will be created.
If the upload operation fails, the error message will be returned.
