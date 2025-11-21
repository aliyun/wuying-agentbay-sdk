// -*- coding: utf-8 -*-
// This file is auto-generated, don't edit it. Thanks.
import * as $dara from '@darabonba/typescript';

export class PauseSessionAsyncRequest extends $dara.Model {
  authorization?: string;
  sessionId?: string;

  static names(): { [key: string]: string } {
    return {
      authorization: 'Authorization',
      sessionId: 'SessionId',
    };
  }

  static types(): { [key: string]: any } {
    return {
      authorization: 'string',
      sessionId: 'string',
    };
  }

  validate() {
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}