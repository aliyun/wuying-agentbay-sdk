// This file is auto-generated, don't edit it
import * as $dara from '@darabonba/typescript';


export class HandleAIEngineMessageRequest extends $dara.Model {
  data?: string;
  msgType?: string;
  sessionToken?: string;
  static names(): { [key: string]: string } {
    return {
      data: 'Data',
      msgType: 'MsgType',
      sessionToken: 'SessionToken',
    };
  }

  static types(): { [key: string]: any } {
    return {
      data: 'string',
      msgType: 'string',
      sessionToken: 'string',
    };
  }

  validate() {
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}

