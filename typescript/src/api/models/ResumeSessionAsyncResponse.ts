// -*- coding: utf-8 -*-
// This file is auto-generated, don't edit it. Thanks.
import * as $dara from '@darabonba/typescript';
import * as main_models from './model';
import { ResumeSessionAsyncResponseBody } from './ResumeSessionAsyncResponseBody';

export class ResumeSessionAsyncResponse extends $dara.Model {
  body?: ResumeSessionAsyncResponseBody;
  headers?: { [key: string]: string };
  statusCode?: number;

  static names(): { [key: string]: string } {
    return {
      body: 'body',
      headers: 'headers',
      statusCode: 'statusCode',
    };
  }

  static types(): { [key: string]: any } {
    return {
      body: ResumeSessionAsyncResponseBody,
      headers: { 'type': 'map', 'keyType': 'string', 'valueType': 'string' },
      statusCode: 'number',
    };
  }

  validate() {
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }

  toMapRecursive(): { [key: string]: any } {
    const map: { [key: string]: any } = {};
    if (this.body !== undefined) {
      map['body'] = this.body?.toMap();
    }
    if (this.headers !== undefined) {
      map['headers'] = this.headers;
    }
    if (this.statusCode !== undefined) {
      map['statusCode'] = this.statusCode;
    }
    return map;
  }

  fromMapRecursive(map: { [key: string]: any }): ResumeSessionAsyncResponse {
    if (map['body'] !== undefined) {
      const temp_model = new main_models.ResumeSessionAsyncResponseBody();
      this.body = temp_model.fromMap(map['body']);
    }
    if (map['headers'] !== undefined) {
      this.headers = map['headers'];
    }
    if (map['statusCode'] !== undefined) {
      this.statusCode = map['statusCode'];
    }
    return this;
  }
}