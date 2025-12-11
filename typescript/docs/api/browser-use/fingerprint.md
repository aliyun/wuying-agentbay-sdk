# Class: FingerprintFormat

Complete fingerprint format including fingerprint data and headers.

## Table of contents


### Properties


### Methods

- [create](#create)
- [fromDict](#fromdict)
- [fromJson](#fromjson)
- [load](#load)
- [toDict](#todict)
- [toJson](#tojson)

## Properties

```typescript
fingerprint: ``Fingerprint``
headers: `Record`<`string`, `string`>
```


## Methods

### create

▸ **create**(`screen`, `navigator`, `videoCard`, `headers`, `videoCodecs?`, `audioCodecs?`, `pluginsData?`, `battery?`, `multimediaDevices?`, `fonts?`, `mockWebRTC?`, `slim?`): [`FingerprintFormat`](fingerprint.md)

Create FingerprintFormat directly using component interfaces.

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `screen` | ``ScreenFingerprint`` | `undefined` |
| `navigator` | ``NavigatorFingerprint`` | `undefined` |
| `videoCard` | ``VideoCard`` | `undefined` |
| `headers` | `Record`\<`string`, `string`\> | `undefined` |
| `videoCodecs?` | `Record`\<`string`, `string`\> | `undefined` |
| `audioCodecs?` | `Record`\<`string`, `string`\> | `undefined` |
| `pluginsData?` | `Record`\<`string`, `string`\> | `undefined` |
| `battery?` | `Record`\<`string`, `string`\> | `undefined` |
| `multimediaDevices?` | `string`[] | `undefined` |
| `fonts?` | `string`[] | `undefined` |
| `mockWebRTC` | `boolean` | `false` |
| `slim?` | `boolean` | `undefined` |

#### Returns

[`FingerprintFormat`](fingerprint.md)

___

### fromDict

▸ **fromDict**(`data`): [`FingerprintFormat`](fingerprint.md)

Create FingerprintFormat from dictionary data.
Note: Used internally by SDK modules.

#### Parameters

| Name | Type |
| :------ | :------ |
| `data` | `Record`\<`string`, `any`\> |

#### Returns

[`FingerprintFormat`](fingerprint.md)

___

### fromJson

▸ **fromJson**(`jsonStr`): [`FingerprintFormat`](fingerprint.md)

Create FingerprintFormat from JSON string.

#### Parameters

| Name | Type |
| :------ | :------ |
| `jsonStr` | `string` |

#### Returns

[`FingerprintFormat`](fingerprint.md)

___

### load

▸ **load**(`data`): [`FingerprintFormat`](fingerprint.md)

Load fingerprint format from dict or JSON string.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `data` | `string` \| `Record`\<`string`, `any`\> | Dictionary or JSON string containing fingerprint data |

#### Returns

[`FingerprintFormat`](fingerprint.md)

FingerprintFormat instance

**`Example`**

```typescript
// From dict
const fp = FingerprintFormat.load({fingerprint: {...}, headers: {...}});
// From JSON file
const data = fs.readFileSync('fingerprint.json', 'utf8');
const fp2 = FingerprintFormat.load(data);
```

___

### toDict

▸ **toDict**(): `Record`\<`string`, `any`\>

Convert to dictionary format.
Note: Used internally by SDK modules.

#### Returns

`Record`\<`string`, `any`\>

___

### toJson

▸ **toJson**(`indent?`): `string`

Convert to JSON string format.
Note: Used internally by SDK modules.

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `indent` | `number` | `2` |

#### Returns

`string`
