# Class: BrowserAgent

## Table of contents


### Methods

- [act](#act)
- [actAsync](#actasync)
- [close](#close)
- [extract](#extract)
- [extractAsync](#extractasync)
- [navigate](#navigate)
- [observe](#observe)
- [observeAsync](#observeasync)
- [screenshot](#screenshot)

## Methods

### act

▸ **act**(`options`, `page?`): `Promise`\<``ActResult``\>

------------------ ACT ------------------ *

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ActOptions`` |
| `page?` | `any` |

#### Returns

`Promise`\<``ActResult``\>

___

### actAsync

▸ **actAsync**(`options`, `page?`): `Promise`\<``ActResult``\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ActOptions`` |
| `page?` | `any` |

#### Returns

`Promise`\<``ActResult``\>

___

### close

▸ **close**(): `Promise`\<`boolean`\>

------------------ CLOSE ------------------ *

#### Returns

`Promise`\<`boolean`\>

___

### extract

▸ **extract**\<`TSchema`\>(`options`, `page?`): `Promise`\<[`boolean`, ``null`` \| `TypeOf`\<`TSchema`\>]\>

------------------ EXTRACT ------------------ *

#### Type parameters

| Name | Type |
| :------ | :------ |
| `TSchema` | extends `ZodType`\<`any`, `any`, `any`, `TSchema`\> |

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ExtractOptions``\<`TSchema`\> |
| `page?` | `any` |

#### Returns

`Promise`\<[`boolean`, ``null`` \| `TypeOf`\<`TSchema`\>]\>

___

### extractAsync

▸ **extractAsync**\<`TSchema`\>(`options`, `page?`): `Promise`\<[`boolean`, ``null`` \| `TypeOf`\<`TSchema`\>]\>

#### Type parameters

| Name | Type |
| :------ | :------ |
| `TSchema` | extends `ZodType`\<`any`, `any`, `any`, `TSchema`\> |

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ExtractOptions``\<`TSchema`\> |
| `page?` | `any` |

#### Returns

`Promise`\<[`boolean`, ``null`` \| `TypeOf`\<`TSchema`\>]\>

___

### navigate

▸ **navigate**(`url`): `Promise`\<`string`\>

------------------ NAVIGATE ------------------ *

#### Parameters

| Name | Type |
| :------ | :------ |
| `url` | `string` |

#### Returns

`Promise`\<`string`\>

___

### observe

▸ **observe**(`options`, `page?`): `Promise`\<``boolean`, [`ObserveResult``[]]\>

------------------ OBSERVE ------------------ *

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ObserveOptions`` |
| `page?` | `any` |

#### Returns

`Promise`\<``boolean`, [`ObserveResult``[]]\>

___

### observeAsync

▸ **observeAsync**(`options`, `page?`): `Promise`\<``boolean`, [`ObserveResult``[]]\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ObserveOptions`` |
| `page?` | `any` |

#### Returns

`Promise`\<``boolean`, [`ObserveResult``[]]\>

___

### screenshot

▸ **screenshot**(`page?`, `full_page?`, `quality?`, `clip?`, `timeout?`): `Promise`\<`string`\>

------------------ SCREENSHOT ------------------ *

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `page` | `any` | `null` |
| `full_page` | `boolean` | `true` |
| `quality` | `number` | `80` |
| `clip?` | `Record`\<`string`, `number`\> | `undefined` |
| `timeout?` | `number` | `undefined` |

#### Returns

`Promise`\<`string`\>
