# Class: BrowserAgent

## Table of contents


### Methods

- [act](#act)
- [actAsync](#actasync)
- [extract](#extract)
- [extractAsync](#extractasync)
- [observe](#observe)
- [observeAsync](#observeasync)

## Methods

### act

▸ **act**(`options`, `page`): `Promise`\<``ActResult``\>

------------------ ACT ------------------ *

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ActOptions`` |
| `page` | `any` |

#### Returns

`Promise`\<``ActResult``\>

___

### actAsync

▸ **actAsync**(`options`, `page`): `Promise`\<``ActResult``\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ActOptions`` |
| `page` | `any` |

#### Returns

`Promise`\<``ActResult``\>

___

### extract

▸ **extract**\<`T`\>(`options`, `page`): `Promise`\<[`boolean`, ``null`` \| `T`]\>

------------------ EXTRACT ------------------ *

#### Type parameters

| Name |
| :------ |
| `T` |

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ExtractOptions``\<`T`\> |
| `page` | `any` |

#### Returns

`Promise`\<[`boolean`, ``null`` \| `T`]\>

___

### extractAsync

▸ **extractAsync**\<`T`\>(`options`, `page`): `Promise`\<[`boolean`, ``null`` \| `T`]\>

#### Type parameters

| Name |
| :------ |
| `T` |

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ExtractOptions``\<`T`\> |
| `page` | `any` |

#### Returns

`Promise`\<[`boolean`, ``null`` \| `T`]\>

___

### observe

▸ **observe**(`options`, `page`): `Promise`\<``boolean`, [`ObserveResult``[]]\>

------------------ OBSERVE ------------------ *

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ObserveOptions`` |
| `page` | `any` |

#### Returns

`Promise`\<``boolean`, [`ObserveResult``[]]\>

___

### observeAsync

▸ **observeAsync**(`options`, `page`): `Promise`\<``boolean`, [`ObserveResult``[]]\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `options` | ``ObserveOptions`` |
| `page` | `any` |

#### Returns

`Promise`\<``boolean`, [`ObserveResult``[]]\>
