// This file is auto-generated, don't edit it
import * as $dara from '@darabonba/typescript';


export class CreateMcpSessionResponseBodyData extends $dara.Model {
  appInstanceId?: string;
  errMsg?: string;
  resourceId?: string;
  resourceUrl?: string;
  sessionId?: string;
  success?: boolean;
  static names(): { [key: string]: string } {
    return {
      appInstanceId: 'AppInstanceId',
      errMsg: 'ErrMsg',
      resourceId: 'ResourceId',
      resourceUrl: 'ResourceUrl',
      sessionId: 'SessionId',
      success: 'Success',
    };
  }

  static types(): { [key: string]: any } {
    return {
      appInstanceId: 'string',
      errMsg: 'string',
      resourceId: 'string',
      resourceUrl: 'string',
      sessionId: 'string',
      success: 'boolean',
    };
  }

  validate() {
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}

